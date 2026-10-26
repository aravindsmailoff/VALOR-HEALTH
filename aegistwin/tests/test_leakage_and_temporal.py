"""Tests for zero lookahead leakage, temporal cohort splits, and point-in-time reconstruction."""

from datetime import date, datetime, timedelta
import pytest

from aegistwin.data.schemas import (
    Condition, Encounter, EncounterClass, Gender, MedicationDispense,
    MemberEvent, MemberEventType, Observation, ObservationCategory, Patient
)
from aegistwin.data.synthetic_generator import generate_synthetic_cohort
from aegistwin.models.cohort_builder import CohortBuilder
from aegistwin.models.feature_store import FeatureStore
from aegistwin.twin.state import MemberDigitalTwin

def test_point_in_time_reconstruction_prevents_leakage():
    """Verify that events occurring after index_date are strictly invisible in reconstructed state."""
    p = Patient(
        id="TEST-MEM-1",
        name="Test Member",
        birth_date=date(1975, 5, 10),
        gender=Gender.FEMALE,
        race="White",
        zip_code="90210",
        enrollment_start=date(2023, 1, 1)
    )
    twin = MemberDigitalTwin(patient=p)

    # Event 1: Lab at Month 6
    t1 = datetime(2024, 6, 1, 10, 0, 0)
    twin.append_event(MemberEvent(
        event_id="EV-1",
        patient_id=p.id,
        timestamp=t1,
        event_type=MemberEventType.LAB_RESULT,
        payload={
            "id": "OBS-1", "patient_id": p.id, "category": ObservationCategory.LABORATORY,
            "loinc_code": "33914-3", "display": "eGFR", "effective_datetime": t1,
            "value_numeric": 72.0, "unit": "mL/min"
        }
    ))

    # Event 2: Acute Hospitalization at Month 14 (Future)
    t2 = datetime(2024, 12, 1, 10, 0, 0)
    twin.append_event(MemberEvent(
        event_id="EV-2",
        patient_id=p.id,
        timestamp=t2,
        event_type=MemberEventType.ENCOUNTER,
        payload={
            "id": "ENC-2", "patient_id": p.id, "encounter_class": EncounterClass.INPATIENT,
            "start_date": t2, "end_date": t2 + timedelta(days=3),
            "primary_diagnosis_icd10": "I50.9", "total_cost": 15000.0
        }
    ))

    # Point in time index: Month 10 (October 2024)
    index_dt = datetime(2024, 10, 1, 0, 0, 0)
    pit_twin = twin.reconstruct_state_at(index_dt)

    # Assertions
    assert len(pit_twin.observations) == 1
    assert pit_twin.get_latest_lab("33914-3") == 72.0
    # Crucial anti-leakage test: Future inpatient encounter must NOT exist in pit_twin
    assert len(pit_twin.encounters) == 0

    # Test feature extraction at index_dt
    fs = FeatureStore()
    feats = fs.extract_features_at(twin, index_dt)
    assert feats["inpatient_visits_365d"] == 0.0
    assert feats["total_claims_cost_365d"] == 0.0

def test_temporal_cohort_split_integrity():
    """Verify train, validation, and test sets are partitioned strictly by calendar time."""
    data = generate_synthetic_cohort(n_members=50, seed=123)
    builder = CohortBuilder()
    samples = builder.build_cohort(data)

    train_samples = [s for s in samples if s.split == "train"]
    val_samples = [s for s in samples if s.split == "val"]
    test_samples = [s for s in samples if s.split == "test"]

    assert len(train_samples) > 0
    assert len(val_samples) > 0
    assert len(test_samples) > 0

    # Ensure temporal ordering: train_index < val_index < test_index
    max_train_date = max(s.index_date for s in train_samples)
    min_val_date = min(s.index_date for s in val_samples)
    max_val_date = max(s.index_date for s in val_samples)
    min_test_date = min(s.index_date for s in test_samples)

    assert max_train_date < min_val_date
    assert max_val_date < min_test_date
