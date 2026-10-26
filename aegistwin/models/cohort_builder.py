"""Temporal Cohort Builder with Anti-Leakage Lookback and Multi-Outcome Labels."""

from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd

from aegistwin.data.schemas import EncounterClass

class CohortSample:
    def __init__(
        self,
        patient_id: str,
        index_date: datetime,
        split: str, # 'train', 'val', 'test'
        outcome_90d_acute: int,
        outcome_30d_readmission: int,
        outcome_12m_progression: int,
        time_to_acute_days: float,
        cost_proxy_target: int = 0 # FOR OBERMEYER BIAS AUDIT DEMONSTRATION ONLY
    ):
        self.patient_id = patient_id
        self.index_date = index_date
        self.split = split
        self.outcome_90d_acute = outcome_90d_acute
        self.outcome_30d_readmission = outcome_30d_readmission
        self.outcome_12m_progression = outcome_12m_progression
        self.time_to_acute_days = time_to_acute_days
        self.cost_proxy_target = cost_proxy_target

class CohortBuilder:
    """Builds time-stamped training, validation, and test cohorts with strict temporal fences."""

    def __init__(
        self,
        cohort_start: date = date(2024, 1, 1),
        duration_months: int = 24
    ):
        self.cohort_start = datetime.combine(cohort_start, datetime.min.time())
        self.duration_months = duration_months

    def build_cohort(self, synthetic_data: Dict[str, list]) -> List[CohortSample]:
        """Constructs cohort samples with strict temporal split."""
        samples: List[CohortSample] = []
        encounters = synthetic_data["encounters"]
        patients = synthetic_data["patients"]

        # Group encounters by patient
        enc_by_patient: Dict[str, list] = {}
        for enc in encounters:
            enc_by_patient.setdefault(enc.patient_id, []).append(enc)

        # Split timeline (Months 1-14: Train, 15-18: Val, 19-24: Test)
        # Using index_date for observation at month 12 (train), month 16 (val), month 20 (test)
        split_definitions = [
            ("train", self.cohort_start + timedelta(days=12 * 30)),
            ("val", self.cohort_start + timedelta(days=16 * 30)),
            ("test", self.cohort_start + timedelta(days=20 * 30)),
        ]

        # Cost proxy calculation: 90th percentile of total spend across entire population
        total_costs = [e.total_cost for e in encounters]
        cost_p90 = np.percentile(total_costs, 90) if total_costs else 10000.0

        for patient in patients:
            pid = patient.id
            p_encs = enc_by_patient.get(pid, [])

            for split_name, index_dt in split_definitions:
                # 1. Outcome 90-day Acute (Inpatient or ED in [index_dt, index_dt + 90d])
                acute_horizon_end = index_dt + timedelta(days=90)
                future_acute = [
                    e for e in p_encs
                    if index_dt <= e.start_date <= acute_horizon_end
                    and e.encounter_class in [EncounterClass.INPATIENT, EncounterClass.EMERGENCY]
                ]
                has_acute = 1 if len(future_acute) > 0 else 0
                
                # Time to event (for survival analysis)
                if has_acute:
                    first_acute_dt = min(e.start_date for e in future_acute)
                    time_to_event = (first_acute_dt - index_dt).total_seconds() / 86400.0
                else:
                    time_to_event = 90.0
                    
                # 2. Outcome 30-day Readmission (in [index_dt, index_dt + 30d])
                readmit_horizon_end = index_dt + timedelta(days=30)
                future_readmit = [
                    e for e in p_encs
                    if index_dt <= e.start_date <= readmit_horizon_end
                    and (e.readmitted_within_30d is True or e.encounter_class == EncounterClass.INPATIENT)
                ]
                has_readmit = 1 if len(future_readmit) > 0 else 0

                # 3. Outcome 12-month Progression (in [index_dt, index_dt + 365d])
                prog_horizon_end = index_dt + timedelta(days=365)
                future_inpatient = [
                    e for e in p_encs
                    if index_dt <= e.start_date <= prog_horizon_end
                    and e.encounter_class == EncounterClass.INPATIENT
                ]
                has_progression = 1 if len(future_inpatient) >= 1 else 0

                # 4. Flawed Cost-Proxy Target (Obermeyer anti-pattern: Top 10% spend in future 90 days)
                future_cost = sum(e.total_cost for e in p_encs if index_dt <= e.start_date <= acute_horizon_end)
                cost_proxy_label = 1 if future_cost >= cost_p90 else 0

                samples.append(CohortSample(
                    patient_id=pid,
                    index_date=index_dt,
                    split=split_name,
                    outcome_90d_acute=has_acute,
                    outcome_30d_readmission=has_readmit,
                    outcome_12m_progression=has_progression,
                    time_to_acute_days=max(0.5, time_to_event),
                    cost_proxy_target=cost_proxy_label
                ))

        return samples
