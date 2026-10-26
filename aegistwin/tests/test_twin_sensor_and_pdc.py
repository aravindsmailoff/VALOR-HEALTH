"""Tests for Member Digital Twin Sensor, Rolling PDC Adherence, and What-If Simulator."""

from datetime import date, datetime, timedelta
import pytest

from aegistwin.data.schemas import (
    Gender, MedicationDispense, MemberEvent, MemberEventType,
    Observation, ObservationCategory, Patient, WearableStream
)
from aegistwin.twin.state import MemberDigitalTwin
from aegistwin.twin.sensor import TwinEventSensor
from aegistwin.twin.simulator import WhatIfSimulator, SimulationIntervention

def test_twin_sensor_new_drug_and_dose_modified():
    p = Patient(
        id="TEST-MEM-2",
        name="Adherence Test Member",
        birth_date=date(1980, 1, 1),
        gender=Gender.MALE,
        race="White",
        zip_code="10001",
        enrollment_start=date(2023, 1, 1)
    )
    twin = MemberDigitalTwin(patient=p)
    sensor = TwinEventSensor()

    # 1. New drug fill
    disp1 = MedicationDispense(
        id="DISP-1",
        patient_id=p.id,
        ndc="00006-0511-54",
        rxnorm_cui="29046",
        drug_name="Lisinopril 10mg",
        therapeutic_class="ACE_Inhibitor",
        dispense_date=date(2024, 1, 1),
        days_supply=30,
        dose_mg_per_day=10.0
    )
    diffs1 = sensor.evaluate_new_fill(twin, disp1)
    assert len(diffs1) == 1
    assert diffs1[0].diff_type == "NEW_DRUG"

    # Apply event
    twin.append_event(MemberEvent(
        event_id="EV-1",
        patient_id=p.id,
        timestamp=datetime(2024, 1, 1),
        event_type=MemberEventType.PRESCRIPTION_FILL,
        payload=disp1.model_dump()
    ))

    # 2. Dose modified fill (titration to 20mg)
    disp2 = MedicationDispense(
        id="DISP-2",
        patient_id=p.id,
        ndc="00006-0511-54",
        rxnorm_cui="29046",
        drug_name="Lisinopril 20mg",
        therapeutic_class="ACE_Inhibitor",
        dispense_date=date(2024, 2, 1),
        days_supply=30,
        dose_mg_per_day=20.0
    )
    diffs2 = sensor.evaluate_new_fill(twin, disp2)
    assert len(diffs2) == 1
    assert diffs2[0].diff_type == "DOSE_MODIFIED"
    assert "changed from 10.0 mg/day to 20.0 mg/day" in diffs2[0].details

def test_rolling_pdc_calculation():
    """Verify true Proportion of Days Covered (PDC) over rolling 90-day window."""
    p = Patient(
        id="TEST-MEM-3",
        name="PDC Member",
        birth_date=date(1970, 1, 1),
        gender=Gender.FEMALE,
        race="Black",
        zip_code="30301",
        enrollment_start=date(2023, 1, 1)
    )
    twin = MemberDigitalTwin(patient=p)
    sensor = TwinEventSensor()

    # Two 30-day fills in a 90-day window -> 60 covered days / 90 days = 0.667 PDC
    as_of = date(2024, 4, 1)
    fill1_date = date(2024, 1, 15)
    fill2_date = date(2024, 2, 20)

    for i, f_date in enumerate([fill1_date, fill2_date]):
        twin.append_event(MemberEvent(
            event_id=f"EV-F-{i}",
            patient_id=p.id,
            timestamp=datetime.combine(f_date, datetime.min.time()),
            event_type=MemberEventType.PRESCRIPTION_FILL,
            payload={
                "id": f"D-{i}", "patient_id": p.id, "ndc": "00000",
                "rxnorm_cui": "6809", "drug_name": "Metformin", "therapeutic_class": "Biguanide",
                "dispense_date": f_date, "days_supply": 30, "dose_mg_per_day": 1000.0
            }
        ))

    pdc_map = sensor.calculate_rolling_pdc(twin, as_of=as_of, lookback_days=90)
    assert "6809" in pdc_map
    assert 0.60 <= pdc_map["6809"] <= 0.70

def test_what_if_simulator_clears_alerts_and_lowers_risk():
    """Verify counterfactual flight simulator resolves DDI and calculates ROI."""
    p = Patient(
        id="TEST-MEM-SIM",
        name="Sim Member",
        birth_date=date(1965, 1, 1),
        gender=Gender.MALE,
        race="White",
        zip_code="02115",
        enrollment_start=date(2023, 1, 1)
    )
    twin = MemberDigitalTwin(patient=p)
    # Add Warfarin + Ibuprofen (DDI)
    twin.active_medications["855332"] = type("Med", (), {"rxnorm_cui": "855332", "drug_name": "Warfarin", "therapeutic_class": "Anticoagulant", "dose_mg_per_day": 5.0, "pdc_90d": 0.95})()
    twin.active_medications["5640"] = type("Med", (), {"rxnorm_cui": "5640", "drug_name": "Ibuprofen", "therapeutic_class": "NSAID", "dose_mg_per_day": 800.0, "pdc_90d": 0.95})()

    simulator = WhatIfSimulator()
    # Baseline should have critical alert
    base_alerts = simulator.run_safety_oracle(twin)
    assert len(base_alerts) >= 1

    # Simulate: Discontinue Ibuprofen, substitute Acetaminophen
    intervention = SimulationIntervention(
        discontinue_rxcuis=["5640"],
        add_or_swap_medications=[{"rxcui": "161", "name": "Acetaminophen", "class": "Analgesic", "dose": 500.0}],
        enroll_care_management=True
    )
    res = simulator.simulate(twin, intervention)

    assert len(res.cleared_safety_alerts) >= 1
    assert res.simulated_risk_90d < res.baseline_risk_90d
    assert res.risk_delta < 0.0
    assert res.projected_90d_cost_savings_usd > 0.0
