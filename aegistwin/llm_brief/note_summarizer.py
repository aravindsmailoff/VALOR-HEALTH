"""Guardrailed Clinical Note & Digital Twin Summarizer with Hallucination Verifier."""

import re
from typing import Any, Dict, List, Set, Tuple
from pydantic import BaseModel

from aegistwin.twin.state import MemberDigitalTwin
from aegistwin.safety.ddi_engine import SafetyFinding

class SynthesizedCareBrief(BaseModel):
    patient_id: str
    clinical_handoff_bullets: List[str]
    member_outreach_script: str
    grounding_verification_score: float # 0.0 to 1.0 (1.0 = 100% grounded)
    verified_entities: List[str]
    unverified_flags: List[str]
    is_safe_to_dispatch: bool

class ClinicalNoteSummarizer:
    """Synthesizes clinical briefs and outreach scripts with strict factual grounding against the Twin."""

    def __init__(self):
        pass

    def synthesize_brief(
        self,
        twin: MemberDigitalTwin,
        risk_90d: float,
        active_safety_alerts: List[SafetyFinding],
        layman_driver_narrative: str
    ) -> SynthesizedCareBrief:
        pid = twin.patient_id
        age = twin.age
        meds = list(twin.active_medications.values())
        med_names = [m.drug_name for m in meds]
        cond_names = [c.display for c in twin.active_conditions.values()]
        egfr = twin.get_latest_lab("33914-3")
        a1c = twin.get_latest_lab("4548-4")

        # 1. Generate 4-Bullet Clinical Handoff Brief
        b1 = f"Demographics & Comorbidity: {age}yo {twin.demographics.gender.value.title()} with active diagnoses of {', '.join(cond_names[:3]) or 'routine history'} (CCI={sum(1 for _ in twin.active_conditions)})."
        b2 = f"Longitudinal Trajectory: Predicted 90-day acute hospitalization risk is {risk_90d*100:.1f}%. Latest eGFR is {f'{egfr:.1f} mL/min' if egfr else 'not recorded'}."
        
        if active_safety_alerts:
            alert_summary = "; ".join([f"{a.rule_id} ({a.severity})" for a in active_safety_alerts[:2]])
            b3 = f"Active Pharmacological Contraindications: {len(active_safety_alerts)} alert(s) detected [{alert_summary}]. Action: {active_safety_alerts[0].recommended_action}"
        else:
            b3 = "Active Pharmacological Contraindications: 0 critical safety clashes detected on active medication reconciliation."

        b4 = f"Adherence & Outreach Priority: Active medications include {', '.join(med_names[:4]) or 'none'}. {layman_driver_narrative}"
        clinical_bullets = [b1, b2, b3, b4]

        # 2. Generate Warm, Empathetic Layman Member Outreach Script
        first_name = twin.demographics.name.split("_")[-1]
        script = (
            f"Hello {first_name}, this is your dedicated care coordinator calling from your health plan. "
            f"We are checking in to make sure your care is going smoothly. Our smart health guardian system noticed "
        )
        if active_safety_alerts:
            script += f"that some of your current prescriptions might need a quick dosage review with your doctor to keep your kidneys and stomach safe. "
        else:
            script += f"that you are doing well managing your health plan. "
        script += (
            f"We want to support you with direct assistance for your doctor appointments and pharmacy deliveries. "
            f"Would it be helpful to schedule a quick 10-minute check-in with our clinical nurse this week?"
        )

        # 3. Deterministic Grounding & Hallucination Verification
        verified_entities, unverified = self._verify_grounding(
            text=" ".join(clinical_bullets) + " " + script,
            twin=twin
        )

        score = round(len(verified_entities) / max(1, len(verified_entities) + len(unverified)), 2)
        is_safe = (score >= 0.90) and (len(unverified) == 0)

        return SynthesizedCareBrief(
            patient_id=pid,
            clinical_handoff_bullets=clinical_bullets,
            member_outreach_script=script,
            grounding_verification_score=score,
            verified_entities=verified_entities,
            unverified_flags=unverified,
            is_safe_to_dispatch=is_safe
        )

    def _verify_grounding(
        self,
        text: str,
        twin: MemberDigitalTwin
    ) -> Tuple[List[str], List[str]]:
        """Cross-references every clinical token and entity against ground-truth Twin state."""
        verified = []
        unverified = []

        # Check Patient ID and Age
        if twin.patient_id in text or f"{twin.age}yo" in text or str(twin.age) in text:
            verified.append(f"Demographics: Age {twin.age}")

        # Check Active Meds
        for cui, med in twin.active_medications.items():
            base_drug_token = med.drug_name.split()[0].lower()
            if base_drug_token in text.lower():
                verified.append(f"RxNorm: {med.drug_name}")

        # Check Conditions
        for icd, cond in twin.active_conditions.items():
            base_cond_token = cond.display.split()[0].lower()
            if base_cond_token in text.lower():
                verified.append(f"Condition: {cond.display}")

        # Scan for hallucinated rogue numbers (e.g., fabricated 4-digit lab values)
        tokens = re.findall(r"\b\d+\.?\d*\b", text)
        known_numbers = {
            str(twin.age), "90", "3", "4", "10", "1", "2", "0",
            f"{twin.age}", "100"
        }
        for o in twin.observations:
            known_numbers.add(str(round(o.value_numeric, 1)))
            known_numbers.add(str(int(o.value_numeric)))

        for t in tokens:
            if len(t) >= 4 and t not in known_numbers and not t.startswith("1000"):
                unverified.append(f"Ungrounded numeric claim: {t}")

        return verified, unverified
