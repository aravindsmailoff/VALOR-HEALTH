"""American Geriatrics Society (AGS) Beers Criteria Evaluator for Age >= 65."""

from typing import Dict, List, Optional, Set
from aegistwin.safety.ddi_engine import SafetyFinding
from aegistwin.data.ontologies import BEERS_CRITERIA_RXCUI

class BeersEngine:
    """Evaluates medication regimens against AGS Beers Criteria for older adults."""
    
    def evaluate(
        self,
        patient_age: int,
        active_rxcui_set: Set[str],
        has_fall_history: bool = False,
        drug_name_map: Optional[Dict[str, str]] = None
    ) -> List[SafetyFinding]:
        findings: List[SafetyFinding] = []
        name_map = drug_name_map or {}
        
        if patient_age < 65:
            return findings
            
        for cui in active_rxcui_set:
            if cui in BEERS_CRITERIA_RXCUI:
                rule = BEERS_CRITERIA_RXCUI[cui]
                dname = name_map.get(cui, rule["drug"])
                
                # Heighten severity if patient has history of falls
                sev = rule["severity"]
                if has_fall_history and rule["category"] in ["Benzodiazepine", "Anticholinergic"]:
                    sev = "CRITICAL"
                    
                mech = (
                    f"AGS Beers Criteria: {rule['category']} class in patient aged {patient_age}. "
                    f"{rule['rationale']} "
                    + ("Patient has documented prior fall history, elevating hip fracture and mortality hazard." if has_fall_history else "")
                )
                
                plain = (
                    f"Because you are {patient_age} years old, taking {dname} can cause severe dizziness, "
                    f"confusion, and serious falls that could lead to hospital admission."
                )
                
                rec = f"Deprescribe {dname} in this older adult. "
                if rule["category"] == "Benzodiazepine":
                    rec += "Taper gradually to prevent withdrawal seizures; recommend non-pharmacological sleep hygiene or CBT-I."
                elif rule["category"] == "Anticholinergic":
                    rec += "Substitute with second-generation non-sedating antihistamines (e.g., Cetirizine, Loratadine) or nasal saline."
                elif rule["category"] == "Tricyclic_Antidepressant":
                    rec += "Switch to modern SSRI/SNRI with favorable geriatric safety profile (e.g., Sertraline or Escitalopram)."
                elif rule["category"] == "Oral_NSAID":
                    rec += "Use topical NSAID gel (Voltaren) or Acetaminophen."
                    
                findings.append(SafetyFinding(
                    rule_id=f"BEERS-00{cui}-{rule['category'].upper()}",
                    category="BEERS_GERIATRIC",
                    severity=sev,
                    involved_drugs=[f"{cui} ({dname})"],
                    clinical_mechanism=mech,
                    plain_english_explanation=plain,
                    recommended_action=rec
                ))
                
        return findings
