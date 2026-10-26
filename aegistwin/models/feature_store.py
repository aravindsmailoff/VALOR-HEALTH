"""Point-in-Time Feature Store with Zero Lookahead Leakage Guarantees."""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd

from aegistwin.data.ontologies import calculate_charlson_score, calculate_elixhauser_flags
from aegistwin.data.schemas import EncounterClass
from aegistwin.twin.state import MemberDigitalTwin
from aegistwin.safety.ddi_engine import DDIEngine
from aegistwin.safety.dci_engine import DCIEngine
from aegistwin.safety.beers_engine import BeersEngine

FEATURE_COLUMNS = [
    # Demographics
    "age", "is_female", "is_black", "is_hispanic", "is_asian",
    # SDOH
    "area_deprivation_index", "social_vulnerability_index",
    "housing_unstable", "food_insecure", "distance_to_primary_care_miles",
    # Claims History (Lookback 365d & 90d)
    "ed_visits_90d", "inpatient_visits_365d", "outpatient_visits_365d",
    "total_claims_cost_365d",
    # Clinical Comorbidities
    "charlson_comorbidity_index", "has_chf", "has_diabetes",
    "has_renal_disease", "has_copd_asthma", "has_depression",
    # Medications & Adherence
    "active_medication_count", "polypharmacy_flag",
    "avg_rolling_pdc_90d", "non_adherence_flag",
    # Longitudinal Labs (EHR)
    "latest_egfr", "egfr_slope_90d", "latest_hba1c", "latest_potassium",
    # Wearable Telemetry
    "wearable_mean_daily_steps", "wearable_mean_resting_hr",
    "wearable_step_drop_pct",
    # Track A Deterministic Safety Findings
    "active_critical_safety_alert_count",
    # Program Enrollment
    "care_management_enrolled"
]

class FeatureStore:
    """Extracts point-in-time clinical features as of an exact index_datetime."""

    def __init__(self):
        self.ddi_engine = DDIEngine()
        self.dci_engine = DCIEngine()
        self.beers_engine = BeersEngine()

    def extract_features_at(
        self,
        twin: MemberDigitalTwin,
        index_datetime: datetime
    ) -> Dict[str, float]:
        """Extracts point-in-time features strictly using historical events up to index_datetime."""
        # 1. Reconstruct historical twin state
        pit_twin = twin.reconstruct_state_at(index_datetime)
        ref_d = index_datetime.date()
        lookback_365 = index_datetime - timedelta(days=365)
        lookback_90 = index_datetime - timedelta(days=90)

        # Demographics
        age = float(pit_twin.age_at(ref_d))
        is_female = 1.0 if pit_twin.demographics.gender.value == "female" else 0.0
        race = pit_twin.demographics.race
        is_black = 1.0 if race == "Black" else 0.0
        is_hispanic = 1.0 if race == "Hispanic" else 0.0
        is_asian = 1.0 if race == "Asian" else 0.0

        # SDOH
        adi = float(pit_twin.sdoh.area_deprivation_index)
        svi = float(pit_twin.sdoh.social_vulnerability_index)
        housing_unstable = 1.0 if pit_twin.sdoh.housing_unstable else 0.0
        food_insecure = 1.0 if pit_twin.sdoh.food_insecure else 0.0
        distance_pcp = float(pit_twin.sdoh.distance_to_primary_care_miles)

        # Claims & Encounters (Lookback strictly between lookback_date and index_datetime)
        p_encs = [e for e in pit_twin.encounters if lookback_365 <= e.start_date <= index_datetime]
        ed_90 = float(sum(1 for e in p_encs if e.start_date >= lookback_90 and e.encounter_class == EncounterClass.EMERGENCY))
        inp_365 = float(sum(1 for e in p_encs if e.encounter_class == EncounterClass.INPATIENT))
        amb_365 = float(sum(1 for e in p_encs if e.encounter_class == EncounterClass.OUTPATIENT))
        spend_365 = float(sum(e.total_cost for e in p_encs))

        # Comorbidities
        icd10_list = list(pit_twin.active_conditions.keys())
        cci = float(calculate_charlson_score(icd10_list))
        elix = calculate_elixhauser_flags(icd10_list)
        has_chf = float(elix.get("CHF", 0))
        has_dm = float(elix.get("DIABETES_COMP", 0) or elix.get("DIABETES_UNCOMP", 0))
        has_ckd = float(elix.get("RENAL_FAILURE", 0))
        has_resp = float(elix.get("COPD", 0) or elix.get("ASTHMA", 0))
        has_dep = float(elix.get("DEPRESSION", 0))

        # Medications & Adherence
        n_meds = float(len(pit_twin.active_medications))
        polypharmacy = 1.0 if n_meds >= 5 else 0.0
        pdc_vals = [m.pdc_90d for m in pit_twin.active_medications.values()]
        avg_pdc = float(sum(pdc_vals) / max(1, len(pdc_vals))) if pdc_vals else 1.0
        non_adh = 1.0 if avg_pdc < 0.80 else 0.0

        # Labs
        egfr = pit_twin.get_latest_lab("33914-3", as_of=index_datetime) or 85.0
        hba1c = pit_twin.get_latest_lab("4548-4", as_of=index_datetime) or 5.4
        k_val = pit_twin.get_latest_lab("2823-3", as_of=index_datetime) or 4.2

        # eGFR 90d slope
        egfr_traj = pit_twin.get_lab_trajectory("33914-3", days=90, as_of=index_datetime)
        if len(egfr_traj) >= 2:
            egfr_slope = float(egfr_traj[-1][1] - egfr_traj[0][1])
        else:
            egfr_slope = 0.0

        # Wearables (Past 14 days)
        w_records = [w for w in pit_twin.wearables if (ref_d - timedelta(days=14)) <= w.date <= ref_d]
        if w_records:
            steps_mean = float(sum(w.daily_steps for w in w_records) / len(w_records))
            hr_mean = float(sum(w.resting_heart_rate for w in w_records) / len(w_records))
            if len(w_records) >= 8:
                first_half_steps = sum(w.daily_steps for w in w_records[:4]) / 4.0
                second_half_steps = sum(w.daily_steps for w in w_records[-4:]) / 4.0
                step_drop = max(0.0, (first_half_steps - second_half_steps) / max(1.0, first_half_steps))
            else:
                step_drop = 0.0
        else:
            steps_mean = 6200.0
            hr_mean = 70.0
            step_drop = 0.0

        # Safety Alerts (Track A)
        active_cuis = set(pit_twin.active_medications.keys())
        active_conds = set(pit_twin.active_conditions.keys())
        recent_labs = {"33914-3": egfr, "2823-3": k_val, "4548-4": hba1c}
        name_map = {cui: med.drug_name for cui, med in pit_twin.active_medications.items()}
        
        alerts = []
        alerts.extend(self.ddi_engine.evaluate(active_cuis, name_map))
        alerts.extend(self.dci_engine.evaluate(active_cuis, active_conds, recent_labs, name_map))
        has_falls = any(c.startswith("R29.6") for c in active_conds)
        alerts.extend(self.beers_engine.evaluate(int(age), active_cuis, has_falls, name_map))
        critical_alerts = float(sum(1 for a in alerts if a.severity == "CRITICAL"))

        care_mgmt = 1.0 if pit_twin.coverage.care_management_enrolled else 0.0

        return {
            "age": age,
            "is_female": is_female,
            "is_black": is_black,
            "is_hispanic": is_hispanic,
            "is_asian": is_asian,
            "area_deprivation_index": adi,
            "social_vulnerability_index": svi,
            "housing_unstable": housing_unstable,
            "food_insecure": food_insecure,
            "distance_to_primary_care_miles": distance_pcp,
            "ed_visits_90d": ed_90,
            "inpatient_visits_365d": inp_365,
            "outpatient_visits_365d": amb_365,
            "total_claims_cost_365d": spend_365,
            "charlson_comorbidity_index": cci,
            "has_chf": has_chf,
            "has_diabetes": has_dm,
            "has_renal_disease": has_ckd,
            "has_copd_asthma": has_resp,
            "has_depression": has_dep,
            "active_medication_count": n_meds,
            "polypharmacy_flag": polypharmacy,
            "avg_rolling_pdc_90d": avg_pdc,
            "non_adherence_flag": non_adh,
            "latest_egfr": egfr,
            "egfr_slope_90d": egfr_slope,
            "latest_hba1c": hba1c,
            "latest_potassium": k_val,
            "wearable_mean_daily_steps": steps_mean,
            "wearable_mean_resting_hr": hr_mean,
            "wearable_step_drop_pct": step_drop,
            "active_critical_safety_alert_count": critical_alerts,
            "care_management_enrolled": care_mgmt
        }
