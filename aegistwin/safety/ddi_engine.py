"""Deterministic Drug-Drug Interaction (DDI) Evaluation Engine."""

from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, model_validator

class SafetyFinding(BaseModel):
    rule_id: str
    category: str  # DDI, DCI_RENAL, DCI_DISEASE, BEERS_GERIATRIC
    severity: str  # CRITICAL, MODERATE, MILD
    involved_drugs: List[str]
    clinical_mechanism: str
    plain_english_explanation: str
    recommended_action: str

    @model_validator(mode="before")
    @classmethod
    def handle_plain_english_alias(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "plain_english_explanation" not in data and "plain_english" in data:
                data["plain_english_explanation"] = data["plain_english"]
        return data

# Deterministic Knowledge Graph of Major Drug-Drug Interactions
DDI_RULES = [
    {
        "rule_id": "DDI-001-WARFARIN-NSAID",
        "pair": {"855332", "5640"},  # Warfarin + Ibuprofen
        "severity": "CRITICAL",
        "mechanism": "NSAIDs cause gastric mucosal erosion, inhibit platelet aggregation via COX-1, and displace warfarin from protein binding, compounding life-threatening gastrointestinal hemorrhage.",
        "plain_english": "Taking Ibuprofen while on blood thinners (Warfarin) dangerously multiplies the risk of severe stomach bleeding.",
        "recommendation": "Discontinue Ibuprofen immediately. Replace with Acetaminophen (Tylenol) for mild-to-moderate pain management; monitor INR within 72 hours."
    },
    {
        "rule_id": "DDI-002-WARFARIN-ASPIRIN",
        "pair": {"855332", "1191"},  # Warfarin + Aspirin
        "severity": "CRITICAL",
        "mechanism": "Dual antiplatelet and anticoagulant synergistic suppression of hemostasis substantially increases major bleeding and intracranial hemorrhage risk.",
        "plain_english": "Combining Aspirin and Warfarin doubles the likelihood of uncontrollable bleeding unless under strict post-cardiac specialist protocol.",
        "recommendation": "Review indication for concomitant antiplatelet therapy. If dual therapy is not clinically justified, discontinue Aspirin."
    },
    {
        "rule_id": "DDI-003-CLOPIDOGREL-OMEPRAZOLE",
        "pair": {"32968", "7646"},  # Clopidogrel + Omeprazole
        "severity": "CRITICAL",
        "mechanism": "Omeprazole competitive inhibition of hepatic CYP2C19 significantly diminishes the metabolic biotransformation of clopidogrel into its active antiplatelet thiol metabolite.",
        "plain_english": "Omeprazole blocks your body from activating Plavix (Clopidogrel), drastically raising the risk of blood clots and recurrent heart attacks.",
        "recommendation": "Switch Omeprazole to Pantoprazole or Famotidine (H2 blocker), which exert negligible CYP2C19 inhibition."
    },
    {
        "rule_id": "DDI-004-ACEI-SPIRONOLACTONE",
        "pair": {"29046", "9997"},  # Lisinopril + Spironolactone
        "severity": "CRITICAL",
        "mechanism": "Dual aldosterone and angiotensin-II suppression decreases renal distal tubular potassium excretion, causing life-threatening severe hyperkalemia (>5.5 mmol/L) and fatal cardiac arrhythmias.",
        "plain_english": "Taking Lisinopril with Spironolactone causes potassium to build up to toxic levels, which can trigger dangerous irregular heartbeats.",
        "recommendation": "Stat serum Potassium and Creatinine check. Re-evaluate dose of Spironolactone (cap at 25mg/day); ensure patient is not on supplemental potassium."
    },
    {
        "rule_id": "DDI-005-SSRI-TRAMADOL",
        "pair": {"36437", "10689"},  # Sertraline + Tramadol
        "severity": "CRITICAL",
        "mechanism": "Concomitant administration elevates synaptic 5-HT concentrations via dual reuptake inhibition, potentially precipitating toxic Serotonin Syndrome (hyperthermia, clonus, autonomic instability).",
        "plain_english": "Mixing Tramadol with your antidepressant (Sertraline) can cause Serotonin Syndrome—a potentially life-threatening buildup of brain chemicals causing confusion and fever.",
        "recommendation": "Avoid combination. Transition patient to a non-serotonergic analgesic or substitute pain regimen with topical NSAIDs/acetaminophen."
    },
    {
        "rule_id": "DDI-006-DIGOXIN-AMIODARONE",
        "pair": {"3616", "435"},  # Digoxin + Amiodarone
        "severity": "CRITICAL",
        "mechanism": "Amiodarone inhibits P-glycoprotein efflux transport, decreasing digoxin renal and biliary clearance by 50%, precipitating lethal digoxin toxicity (AV block, ventricular tachycardia).",
        "plain_english": "Amiodarone slows down how your body gets rid of Digoxin, easily pushing it to poisonous levels that can stop your heart.",
        "recommendation": "Reduce Digoxin dosage by 50% immediately when initiating Amiodarone. Monitor serum digoxin concentrations and ECG."
    },
    {
        "rule_id": "DDI-007-WARFARIN-NAPROXEN",
        "pair": {"855332", "7052"},  # Warfarin + Naproxen
        "severity": "CRITICAL",
        "mechanism": "Synergistic inhibition of coagulation cascade and platelet aggregation with concurrent gastric mucosal barrier disruption.",
        "plain_english": "Taking Aleve (Naproxen) while on Warfarin severely increases the risk of stomach ulcer bleeding.",
        "recommendation": "Discontinue Naproxen. Consider acetaminophen or topical therapies."
    }
]

class DDIEngine:
    """Evaluates active drug regimens against deterministic DDI knowledge graph."""
    
    def __init__(self, rules: Optional[List[Dict]] = None):
        self.rules = rules or DDI_RULES
        
    def evaluate(self, active_rxcui_set: Set[str], drug_name_map: Optional[Dict[str, str]] = None) -> List[SafetyFinding]:
        findings: List[SafetyFinding] = []
        name_map = drug_name_map or {}
        
        for rule in self.rules:
            req_pair: Set[str] = rule["pair"]
            if req_pair.issubset(active_rxcui_set):
                involved = [f"{cui} ({name_map.get(cui, 'Medication')})" for cui in req_pair]
                findings.append(SafetyFinding(
                    rule_id=rule["rule_id"],
                    category="DDI",
                    severity=rule["severity"],
                    involved_drugs=involved,
                    clinical_mechanism=rule["mechanism"],
                    plain_english_explanation=rule["plain_english"],
                    recommended_action=rule["recommendation"]
                ))
        return findings
