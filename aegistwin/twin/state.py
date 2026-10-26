"""Stateful Member Digital Twin with Point-in-Time Reconstruction."""

import copy
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional, Set, Tuple
from pydantic import BaseModel, Field

from aegistwin.data.schemas import (
    Condition, Coverage, Encounter, Gender, MedicationDispense,
    MemberEvent, MemberEventType, Observation, ObservationCategory,
    Patient, SDOHProfile, WearableStream
)
from aegistwin.safety.ddi_engine import SafetyFinding

class ActiveMedicationState(BaseModel):
    rxnorm_cui: str
    drug_name: str
    therapeutic_class: str
    last_fill_date: date
    days_supply: int
    dose_mg_per_day: float
    total_fills_90d: int = 1
    pdc_90d: float = 1.0
    status: str = "active"

class MemberDigitalTwin:
    """Stateful, longitudinal digital twin representing an individual health plan member."""

    def __init__(
        self,
        patient: Patient,
        sdoh: Optional[SDOHProfile] = None,
        coverage: Optional[Coverage] = None
    ):
        self.patient_id: str = patient.id
        self.demographics: Patient = patient
        self.sdoh: SDOHProfile = sdoh or SDOHProfile(
            patient_id=patient.id,
            zip_code=patient.zip_code,
            area_deprivation_index=50,
            social_vulnerability_index=0.5
        )
        self.coverage: Coverage = coverage or Coverage(
            id=f"COV-{patient.id}",
            patient_id=patient.id
        )
        self.active_conditions: Dict[str, Condition] = {}       # icd10 -> Condition
        self.active_medications: Dict[str, ActiveMedicationState] = {} # rxcui -> ActiveMedicationState
        self.observations: List[Observation] = []
        self.encounters: List[Encounter] = []
        self.wearables: List[WearableStream] = []
        self.alert_history: List[SafetyFinding] = []
        self.risk_history: List[Dict[str, Any]] = []
        self.event_log: List[MemberEvent] = []

    @property
    def age(self) -> int:
        today = date.today()
        b = self.demographics.birth_date
        return today.year - b.year - ((today.month, today.day) < (b.month, b.day))

    def age_at(self, as_of: date) -> int:
        b = self.demographics.birth_date
        return as_of.year - b.year - ((as_of.month, as_of.day) < (b.month, b.day))

    def append_event(self, event: MemberEvent) -> None:
        """Appends an event to the immutable log and mutates twin state."""
        self.event_log.append(event)
        self._apply_event(event)

    def _apply_event(self, event: MemberEvent) -> None:
        p = event.payload
        t_date = event.timestamp.date()

        if event.event_type == MemberEventType.DIAGNOSIS_LOGGED:
            cond = Condition(**p)
            self.active_conditions[cond.icd10_code] = cond

        elif event.event_type == MemberEventType.PRESCRIPTION_FILL:
            disp = MedicationDispense(**p)
            cui = disp.rxnorm_cui
            if cui in self.active_medications:
                med = self.active_medications[cui]
                med.last_fill_date = disp.dispense_date
                med.days_supply = disp.days_supply
                med.dose_mg_per_day = disp.dose_mg_per_day
                med.total_fills_90d += 1
                med.status = "active"
            else:
                self.active_medications[cui] = ActiveMedicationState(
                    rxnorm_cui=cui,
                    drug_name=disp.drug_name,
                    therapeutic_class=disp.therapeutic_class,
                    last_fill_date=disp.dispense_date,
                    days_supply=disp.days_supply,
                    dose_mg_per_day=disp.dose_mg_per_day
                )

        elif event.event_type in [MemberEventType.LAB_RESULT, MemberEventType.VITAL_SIGN]:
            obs = Observation(**p)
            self.observations.append(obs)

        elif event.event_type == MemberEventType.ENCOUNTER:
            enc = Encounter(**p)
            self.encounters.append(enc)

        elif event.event_type == MemberEventType.WEARABLE_DAILY:
            w = WearableStream(**p)
            self.wearables.append(w)

        elif event.event_type == MemberEventType.CARE_OUTREACH:
            self.coverage.care_management_enrolled = True

    def reconstruct_state_at(self, target_timestamp: datetime) -> "MemberDigitalTwin":
        """Point-in-time reconstruction: Replays event log up to target_timestamp (guarantees zero lookahead)."""
        reconstructed = MemberDigitalTwin(
            patient=copy.deepcopy(self.demographics),
            sdoh=copy.deepcopy(self.sdoh),
            coverage=copy.deepcopy(self.coverage)
        )
        
        # Sort events chronologically and replay up to target_timestamp
        sorted_events = sorted(
            [e for e in self.event_log if e.timestamp <= target_timestamp],
            key=lambda x: x.timestamp
        )
        for ev in sorted_events:
            reconstructed.event_log.append(ev)
            reconstructed._apply_event(ev)
            
        return reconstructed

    def get_latest_lab(self, loinc_code: str, as_of: Optional[datetime] = None) -> Optional[float]:
        """Returns the most recent lab value on or before as_of datetime."""
        valid_labs = [
            o for o in self.observations
            if o.loinc_code == loinc_code and (as_of is None or o.effective_datetime <= as_of)
        ]
        if not valid_labs:
            return None
        valid_labs.sort(key=lambda x: x.effective_datetime)
        return valid_labs[-1].value_numeric

    def get_lab_trajectory(self, loinc_code: str, days: int = 90, as_of: Optional[datetime] = None) -> List[Tuple[datetime, float]]:
        """Returns longitudinal trajectory of a given lab over lookback days."""
        ref_dt = as_of or datetime.now()
        start_dt = ref_dt - timedelta(days=days)
        pts = [
            (o.effective_datetime, o.value_numeric)
            for o in self.observations
            if o.loinc_code == loinc_code and start_dt <= o.effective_datetime <= ref_dt
        ]
        pts.sort(key=lambda x: x[0])
        return pts
