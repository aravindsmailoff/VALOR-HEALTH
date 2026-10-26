"""Counterfactual What-If Flight Simulator Sandbox for Member Digital Twins."""

import copy
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel

from aegistwin.config.settings import settings
from aegistwin.data.schemas import MedicationDispense, MemberEvent, MemberEventType
from aegistwin.safety.ddi_engine import DDIEngine, SafetyFinding
from aegistwin.safety.dci_engine import DCIEngine
from aegistwin.safety.beers_engine import BeersEngine
from aegistwin.twin.state import MemberDigitalTwin, ActiveMedicationState
from aegistwin.data.ontologies import RXNORM_KNOWLEDGE

class SimulationIntervention(BaseModel):
    discontinue_rxcuis: List[str] = []
    add_or_swap_medications: List[Dict[str, Any]] = [] # [{rxcui, name, class, dose}]
    boost_adherence_to_pdc: Optional[float] = None     # e.g., 0.90
    enroll_care_management: bool = False

class SimulationResult(BaseModel):
    patient_id: str
    baseline_risk_90d: float
    simulated_risk_90d: float
    risk_delta: float
    baseline_tier: str
    simulated_tier: str
    cleared_safety_alerts: List[SafetyFinding]
    new_safety_alerts: List[SafetyFinding]
    projected_90d_cost_savings_usd: float
    plain_english_summary: str
    clinical_rationale: str

class WhatIfSimulator:
    """Clones a Member Digital Twin and evaluates counterfactual clinical interventions."""

    def __init__(
        self,
        risk_scoring_fn=None, # Injected callable: (twin) -> float
        ddi_engine: Optional[DDIEngine] = None,
        dci_engine: Optional[DCIEngine] = None,
        beers_engine: Optional[BeersEngine] = None
    ):
        self.risk_scoring_fn = risk_scoring_fn
        self.ddi_engine = ddi_engine or DDIEngine()
        self.dci_engine = dci_engine or DCIEngine()
        self.beers_engine = beers_engine or BeersEngine()

    def run_safety_oracle(self, twin: MemberDigitalTwin) -> List[SafetyFinding]:
        """Runs Track A Deterministic Safety Oracle across active medications, labs, and conditions."""
        findings: List[SafetyFinding] = []
        active_cuis = set(twin.active_medications.keys())
        active_conditions = set(twin.active_conditions.keys())
        name_map = {cui: med.drug_name for cui, med in twin.active_medications.items()}
        
        # Latest labs
        recent_labs = {}
        for loinc in ["33914-3", "2823-3", "4548-4", "2160-0"]:
            val = twin.get_latest_lab(loinc)
            if val is not None:
                recent_labs[loinc] = val

        # Evaluate Track A
        findings.extend(self.ddi_engine.evaluate(active_cuis, name_map))
        findings.extend(self.dci_engine.evaluate(active_cuis, active_conditions, recent_labs, name_map))
        has_falls = any(c.startswith("R29.6") for c in active_conditions)
        findings.extend(self.beers_engine.evaluate(twin.age, active_cuis, has_falls, name_map))

        return findings

    def _default_surrogate_risk(self, twin: MemberDigitalTwin) -> float:
        """Surrogate calibrated risk estimator used when ML model is not explicitly passed."""
        base = 0.05
        # Conditions
        if any(c.startswith("I50") for c in twin.active_conditions): base += 0.20
        if any(c.startswith("N18") for c in twin.active_conditions): base += 0.14
        if any(c.startswith("E11") for c in twin.active_conditions): base += 0.08
        if any(c.startswith("J44") or c.startswith("J45") for c in twin.active_conditions): base += 0.10
        # SDOH
        if twin.sdoh.area_deprivation_index > 75: base += 0.07
        if twin.sdoh.housing_unstable: base += 0.09
        # Safety findings
        alerts = self.run_safety_oracle(twin)
        critical_count = sum(1 for a in alerts if a.severity == "CRITICAL")
        base += critical_count * 0.18
        # Adherence
        avg_pdc = sum(m.pdc_90d for m in twin.active_medications.values()) / max(1, len(twin.active_medications))
        if avg_pdc < 0.70: base += 0.12
        # Care management offset
        if twin.coverage.care_management_enrolled: base -= 0.14

        return float(min(0.96, max(0.02, base)))

    def simulate(
        self,
        twin: MemberDigitalTwin,
        intervention: SimulationIntervention,
        custom_risk_scorer=None
    ) -> SimulationResult:
        """Executes counterfactual simulation on a deepcopy of the digital twin."""
        scorer = custom_risk_scorer or self.risk_scoring_fn or self._default_surrogate_risk
        
        # 1. Baseline Evaluation
        base_alerts = self.run_safety_oracle(twin)
        base_risk = scorer(twin)
        base_tier = "High" if base_risk >= 0.35 else ("Medium" if base_risk >= 0.18 else "Low")
        
        # 2. Clone Twin
        sim_twin = copy.deepcopy(twin)
        
        # 3. Apply Interventions
        # Discontinue
        for cui in intervention.discontinue_rxcuis:
            if cui in sim_twin.active_medications:
                del sim_twin.active_medications[cui]
                
        # Add / Swap
        for med_spec in intervention.add_or_swap_medications:
            cui = med_spec["rxcui"]
            name = med_spec.get("name", RXNORM_KNOWLEDGE.get(cui, {}).get("name", "Simulated Drug"))
            t_class = med_spec.get("class", RXNORM_KNOWLEDGE.get(cui, {}).get("class", "Therapeutic_Class"))
            dose = float(med_spec.get("dose", 10.0))
            sim_twin.active_medications[cui] = ActiveMedicationState(
                rxnorm_cui=cui,
                drug_name=name,
                therapeutic_class=t_class,
                last_fill_date=date.today(),
                days_supply=30,
                dose_mg_per_day=dose,
                pdc_90d=1.0
            )
            
        # Boost adherence
        if intervention.boost_adherence_to_pdc is not None:
            target_pdc = float(min(1.0, max(0.1, intervention.boost_adherence_to_pdc)))
            for med in sim_twin.active_medications.values():
                med.pdc_90d = target_pdc
                
        # Enroll in Care Management
        if intervention.enroll_care_management:
            sim_twin.coverage.care_management_enrolled = True
            
        # 4. Simulated Re-Evaluation
        sim_alerts = self.run_safety_oracle(sim_twin)
        sim_risk = scorer(sim_twin)
        sim_tier = "High" if sim_risk >= 0.35 else ("Medium" if sim_risk >= 0.18 else "Low")
        risk_delta = round(sim_risk - base_risk, 4)
        
        # Determine Cleared vs New Alerts
        base_rule_ids = {a.rule_id: a for a in base_alerts}
        sim_rule_ids = {a.rule_id: a for a in sim_alerts}
        cleared = [base_rule_ids[rid] for rid in base_rule_ids if rid not in sim_rule_ids]
        new_alerts = [sim_rule_ids[rid] for rid in sim_rule_ids if rid not in base_rule_ids]
        
        # Payer ROI Calculation
        # Expected savings = Risk reduction * cost of acute admission
        avoided_prob = max(0.0, -risk_delta)
        savings = avoided_prob * settings.AVOIDABLE_INPATIENT_ADM_COST_USD
        if intervention.enroll_care_management:
            savings -= settings.CARE_MANAGEMENT_OUTREACH_COST_USD
        savings = max(0.0, round(savings, 2))
        
        # Narratives
        plain_english = (
            f"By implementing this clinical plan, the member's 90-day hospitalization probability drops "
            f"from {base_risk*100:.1f}% down to {sim_risk*100:.1f}% ({risk_delta*100:+.1f}% risk reduction). "
        )
        if cleared:
            plain_english += f"Resolved {len(cleared)} dangerous medication conflict(s). "
        if savings > 0:
            plain_english += f"Projected healthcare cost avoidance: ${savings:,.2f} over the next quarter."
            
        clinical_rationale = (
            f"Intervention modified {len(intervention.discontinue_rxcuis)} discontinued and "
            f"{len(intervention.add_or_swap_medications)} initiated agents. Cleared alerts: {[c.rule_id for c in cleared]}. "
            f"Risk Tier shift: {base_tier} -> {sim_tier}."
        )

        return SimulationResult(
            patient_id=twin.patient_id,
            baseline_risk_90d=round(base_risk, 4),
            simulated_risk_90d=round(sim_risk, 4),
            risk_delta=risk_delta,
            baseline_tier=base_tier,
            simulated_tier=sim_tier,
            cleared_safety_alerts=cleared,
            new_safety_alerts=new_alerts,
            projected_90d_cost_savings_usd=savings,
            plain_english_summary=plain_english,
            clinical_rationale=clinical_rationale
        )
