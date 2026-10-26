"""Deterministic Drug-Condition and Organ Function Contraindication Engine (DCI)."""

from typing import Dict, List, Optional, Set
from aegistwin.safety.ddi_engine import SafetyFinding

class DCIEngine:
    """Evaluates drug-condition contraindications and renal/hepatic safety boundaries."""
    
    def evaluate(
        self,
        active_rxcui_set: Set[str],
        active_conditions: Set[str], # ICD-10 codes
        recent_labs: Dict[str, float], # loinc -> latest value
        drug_name_map: Optional[Dict[str, str]] = None
    ) -> List[SafetyFinding]:
        findings: List[SafetyFinding] = []
        name_map = drug_name_map or {}
        
        # 1. Metformin + Low eGFR (< 30 mL/min/1.73m2)
        egfr = recent_labs.get("33914-3", 90.0) # eGFR LOINC
        if "6809" in active_rxcui_set and egfr < 30.0:
            findings.append(SafetyFinding(
                rule_id="DCI-RENAL-001-METFORMIN",
                category="DCI_RENAL",
                severity="CRITICAL",
                involved_drugs=[f"6809 ({name_map.get('6809', 'Metformin')})"],
                clinical_mechanism=f"Metformin is cleared almost entirely via renal excretion. When eGFR drops below 30 mL/min/1.73m² (current: {egfr}), systemic drug accumulation drastically impairs mitochondrial lactate metabolism, causing life-threatening Metformin-Associated Lactic Acidosis (MALA) with mortality approaching 50%.",
                plain_english_explanation=f"Your kidney function has dropped significantly (eGFR {egfr}), making Metformin dangerous because it can cause toxic acid buildup in the bloodstream.",
                recommended_action="Discontinue Metformin immediately. Switch to an insulin-based regimen or a renally safe DPP-4 inhibitor (e.g., Linagliptin 5mg daily, which requires no renal dose adjustment)."
            ))
            
        # 2. Non-selective Beta-Blocker (Propranolol) in Active Asthma / COPD
        has_asthma = any(c.startswith("J45") for c in active_conditions)
        has_copd = any(c.startswith("J44") for c in active_conditions)
        if "8703" in active_rxcui_set and (has_asthma or has_copd):
            findings.append(SafetyFinding(
                rule_id="DCI-DISEASE-002-PROPRANOLOL-ASTHMA",
                category="DCI_DISEASE",
                severity="CRITICAL",
                involved_drugs=[f"8703 ({name_map.get('8703', 'Propranolol')})"],
                clinical_mechanism="Non-selective beta-adrenergic antagonism blocks pulmonary beta-2 receptors, overriding endogenous bronchodilation and provoking severe, refractory bronchospasm and respiratory failure in patients with underlying reactive airway disease.",
                plain_english_explanation="Propranolol tightens your lung airways, which can trigger severe, life-threatening asthma attacks or breathing problems.",
                recommended_action="Discontinue Propranolol. Transition to a cardio-selective beta-1 blocker (e.g., Metoprolol Tartrate/Succinate or Bisoprolol) with careful peak-flow monitoring, or consider calcium channel blockers."
            ))
            
        # 3. NSAID (Ibuprofen / Naproxen) in Chronic Kidney Disease (Stage 3b-5) or Heart Failure
        has_ckd = any(c.startswith("N18.3") or c.startswith("N18.4") or c.startswith("N18.5") for c in active_conditions) or egfr < 45.0
        has_chf = any(c.startswith("I50") for c in active_conditions)
        nsaid_present = {"5640", "7052"}.intersection(active_rxcui_set)
        
        if nsaid_present and (has_ckd or has_chf):
            culprits = [f"{cui} ({name_map.get(cui, 'NSAID')})" for cui in nsaid_present]
            context = "severe kidney disease" if has_ckd else "heart failure"
            findings.append(SafetyFinding(
                rule_id="DCI-DISEASE-003-NSAID-CKD-CHF",
                category="DCI_RENAL" if has_ckd else "DCI_DISEASE",
                severity="CRITICAL" if egfr < 30.0 else "MODERATE",
                involved_drugs=culprits,
                clinical_mechanism=f"NSAIDs inhibit renal cyclooxygenase synthesis of vasodilatory prostaglandins (PGE2, PGI2), impairing renal afferent arteriolar blood flow and provoking acute renal decompensation, fluid retention, and heart failure exacerbations in {context}.",
                plain_english_explanation=f"NSAID pain relievers (Ibuprofen/Naproxen) can harm your kidneys and cause dangerous fluid buildup that worsens {context}.",
                recommended_action="Deprescribe oral NSAIDs. Use topical formulations (Diclofenac gel) or Acetaminophen."
            ))
            
        # 4. Severe Hyperkalemia with Potassium-Sparing Diuretics / Aldosterone Antagonists
        potassium = recent_labs.get("2823-3", 4.2)
        k_sparing = {"9997", "10759"}.intersection(active_rxcui_set)
        if k_sparing and potassium > 5.2:
            culprits = [f"{cui} ({name_map.get(cui, 'K-Sparing Agent')})" for cui in k_sparing]
            findings.append(SafetyFinding(
                rule_id="DCI-LAB-004-HYPERKALEMIA-SPIRONOLACTONE",
                category="DCI_DISEASE",
                severity="CRITICAL" if potassium >= 5.5 else "MODERATE",
                involved_drugs=culprits,
                clinical_mechanism=f"Serum potassium is elevated at {potassium} mmol/L. Aldosterone antagonism inhibits distal tubular K+ excretion, creating high risk for peaked T-waves, PR prolongation, and fatal ventricular arrhythmias.",
                plain_english_explanation=f"Your blood potassium level is elevated at {potassium} mmol/L. Continuing water pills like Spironolactone can push potassium to levels that disrupt your heart rhythm.",
                recommended_action=f"Hold potassium-sparing diuretics immediately. Repeat serum electrolytes in 48 hours; order 12-lead ECG if K+ >= 5.5."
            ))
            
        return findings
