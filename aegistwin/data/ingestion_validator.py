"""Schema Validation, Missingness Auditing, and Multi-Format Ingestion Adapters."""

from datetime import datetime, date
from typing import Any, Dict, List, Tuple
import pandas as pd
from pydantic import ValidationError

from aegistwin.data.schemas import (
    Patient, Condition, MedicationDispense, Observation, Encounter,
    EncounterClass, ObservationCategory, Gender
)

class IngestionReport:
    def __init__(self):
        self.total_records: int = 0
        self.valid_records: int = 0
        self.invalid_records: int = 0
        self.missingness_by_field: Dict[str, float] = {}
        self.validation_errors: List[str] = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_records": self.total_records,
            "valid_records": self.valid_records,
            "invalid_records": self.invalid_records,
            "validation_rate_pct": round((self.valid_records / max(1, self.total_records)) * 100, 2),
            "missingness": self.missingness_by_field,
            "error_sample": self.validation_errors[:5]
        }

def validate_patient_records(records: List[Dict[str, Any]]) -> Tuple[List[Patient], IngestionReport]:
    """Validates patient raw dictionaries against the FHIR Patient schema."""
    report = IngestionReport()
    valid_patients: List[Patient] = []
    
    if not records:
        return valid_patients, report
        
    df = pd.DataFrame(records)
    report.total_records = len(df)
    
    for col in df.columns:
        report.missingness_by_field[col] = round(df[col].isna().mean() * 100, 2)
        
    for r in records:
        try:
            p = Patient(**r)
            valid_patients.append(p)
            report.valid_records += 1
        except ValidationError as e:
            report.invalid_records += 1
            if len(report.validation_errors) < 10:
                report.validation_errors.append(str(e))
                
    return valid_patients, report

# Multi-Format Ingestion Adapters

def adapt_synthea_patient(row: Dict[str, Any]) -> Patient:
    """Adapts a standard Synthea CSV patient row to AegisTwin Patient model."""
    gender_map = {"M": Gender.MALE, "F": Gender.FEMALE}
    birth_dt = pd.to_datetime(row.get("BIRTHDATE", "1970-01-01")).date()
    return Patient(
        id=str(row.get("Id", f"SYN-{row.get('SSN', '0000')}")),
        name=f"{row.get('FIRST', 'Member')} {row.get('LAST', 'Synthea')}",
        birth_date=birth_dt,
        gender=gender_map.get(row.get("GENDER", "M"), Gender.UNKNOWN),
        race=str(row.get("RACE", "White")),
        zip_code=str(row.get("ZIP", "02115"))[:5],
        enrollment_start=date(2023, 1, 1)
    )

def adapt_cms_synpuf_claim(row: Dict[str, Any]) -> Encounter:
    """Adapts CMS DE-SynPUF Inpatient/Outpatient claim to Encounter model."""
    claim_id = str(row.get("CLM_ID", "CLM-000"))
    patient_id = str(row.get("DESYNPUF_ID", "SYN-000"))
    from_dt = pd.to_datetime(row.get("CLM_FROM_DT", "2024-01-01"))
    thru_dt = pd.to_datetime(row.get("CLM_THRU_DT", "2024-01-02"))
    
    # Classify inpatient vs outpatient based on claim cost / fields
    is_inpatient = "CLM_UTLZTN_DAY_CNT" in row and float(row.get("CLM_UTLZTN_DAY_CNT", 0)) > 0
    eclass = EncounterClass.INPATIENT if is_inpatient else EncounterClass.OUTPATIENT
    
    primary_dx = str(row.get("PRVDR_NUM", row.get("ICD9_DGNS_CD_1", row.get("ICD10_DGNS_CD_1", "I10"))))
    cost = float(row.get("CLM_PMT_AMT", 250.0))
    
    return Encounter(
        id=claim_id,
        patient_id=patient_id,
        encounter_class=eclass,
        start_date=from_dt,
        end_date=thru_dt,
        primary_diagnosis_icd10=primary_dx,
        total_cost=cost
    )

def adapt_mimic_lab(row: Dict[str, Any]) -> Observation:
    """Adapts MIMIC-IV labevents row to AegisTwin Observation model."""
    charttime = pd.to_datetime(row.get("charttime", datetime.now()))
    itemid = str(row.get("itemid", "50912"))
    val = float(row.get("valuenum", 1.0))
    
    # Mapping MIMIC ItemIDs to standard LOINC
    item_loinc_map = {
        "50912": ("2160-0", "Serum_Creatinine", "mg/dL"),
        "50971": ("2823-3", "Potassium", "mmol/L"),
        "50852": ("4548-4", "HbA1c", "%"),
    }
    loinc, disp, unit = item_loinc_map.get(itemid, ("33914-3", "eGFR", "mL/min/1.73m2"))
    
    return Observation(
        id=f"MIMIC-{row.get('labevent_id', charttime.strftime('%s'))}",
        patient_id=str(row.get("subject_id", "MIMIC-0")),
        category=ObservationCategory.LABORATORY,
        loinc_code=loinc,
        display=disp,
        effective_datetime=charttime,
        value_numeric=val,
        unit=unit
    )
