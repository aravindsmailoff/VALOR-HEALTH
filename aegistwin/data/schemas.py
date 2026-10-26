"""FHIR R4-Compatible Pydantic v2 Data Models for AegisTwin."""

from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNKNOWN = "unknown"

class EncounterClass(str, Enum):
    INPATIENT = "IMP"
    OUTPATIENT = "AMB"
    EMERGENCY = "EMER"
    URGENT_CARE = "URGENT"
    HOME_HEALTH = "HH"

class ObservationCategory(str, Enum):
    VITAL_SIGNS = "vital-signs"
    LABORATORY = "laboratory"
    WEARABLE = "wearable"
    SDOH = "sdoh"

class MedicationStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    DISCONTINUED = "discontinued"
    ON_HOLD = "on-hold"

class Patient(BaseModel):
    id: str = Field(..., description="Unique FHIR Member/Patient ID")
    name: str = Field(..., description="Full Name")
    birth_date: date = Field(..., description="Date of birth")
    gender: Gender = Field(..., description="Administrative sex")
    race: str = Field(default="White", description="Reported race/ethnicity")
    zip_code: str = Field(..., description="Residential 5-digit or 9-digit ZIP code")
    enrollment_start: date = Field(..., description="Health plan coverage start date")
    enrollment_end: Optional[date] = Field(None, description="Coverage end date if churned")

class Condition(BaseModel):
    id: str
    patient_id: str
    icd10_code: str = Field(..., description="ICD-10-CM diagnosis code (e.g. I10, E11.9)")
    display: str = Field(..., description="Human-readable condition title")
    onset_date: date
    resolution_date: Optional[date] = None
    verification_status: str = "confirmed"

class MedicationDispense(BaseModel):
    id: str
    patient_id: str
    ndc: str = Field(..., description="National Drug Code (11-digit)")
    rxnorm_cui: str = Field(..., description="RxNorm Concept Unique Identifier (RxCUI)")
    drug_name: str = Field(..., description="Brand or generic display name")
    therapeutic_class: str = Field(..., description="Therapeutic class e.g., Anticoagulant, Statin")
    dispense_date: date
    days_supply: int = Field(default=30, ge=1)
    quantity_dispensed: float = Field(default=30.0)
    dose_mg_per_day: float = Field(default=10.0)
    prescriber_id: Optional[str] = None
    claim_cost: float = Field(default=45.0, ge=0.0)

class Observation(BaseModel):
    id: str
    patient_id: str
    category: ObservationCategory
    loinc_code: str = Field(..., description="LOINC code (e.g., 33914-3 for eGFR)")
    display: str = Field(..., description="Observation name (e.g., eGFR, HbA1c)")
    effective_datetime: datetime
    value_numeric: float
    unit: str
    reference_range_low: Optional[float] = None
    reference_range_high: Optional[float] = None

class Encounter(BaseModel):
    id: str
    patient_id: str
    encounter_class: EncounterClass
    start_date: datetime
    end_date: datetime
    primary_diagnosis_icd10: str
    secondary_diagnoses: List[str] = Field(default_factory=list)
    cpt_codes: List[str] = Field(default_factory=list)
    total_cost: float = Field(default=0.0)
    readmitted_within_30d: Optional[bool] = None

class Coverage(BaseModel):
    id: str
    patient_id: str
    plan_type: str = "Commercial_HMO"  # Medicare_Advantage, Medicaid, Commercial_PPO
    care_management_enrolled: bool = False
    enrollment_date: Optional[date] = None

class WearableStream(BaseModel):
    patient_id: str
    date: date
    daily_steps: int
    resting_heart_rate: float
    sleep_efficiency_pct: float

class SDOHProfile(BaseModel):
    patient_id: str
    zip_code: str
    area_deprivation_index: int = Field(..., ge=1, le=100, description="ADI decile/percentile 1-100")
    social_vulnerability_index: float = Field(..., ge=0.0, le=1.0, description="CDC SVI (0=low, 1=high)")
    housing_unstable: bool = False
    food_insecure: bool = False
    income_bracket: str = "Middle"  # Low, Middle, High
    distance_to_primary_care_miles: float = 3.5
    transportation_barrier: bool = False

class MemberEventType(str, Enum):
    PRESCRIPTION_FILL = "PRESCRIPTION_FILL"
    LAB_RESULT = "LAB_RESULT"
    VITAL_SIGN = "VITAL_SIGN"
    ENCOUNTER = "ENCOUNTER"
    DIAGNOSIS_LOGGED = "DIAGNOSIS_LOGGED"
    WEARABLE_DAILY = "WEARABLE_DAILY"
    CARE_OUTREACH = "CARE_OUTREACH"

class MemberEvent(BaseModel):
    event_id: str
    patient_id: str
    timestamp: datetime
    event_type: MemberEventType
    payload: Dict[str, Any]
