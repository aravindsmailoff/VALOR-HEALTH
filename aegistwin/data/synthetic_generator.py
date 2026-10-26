"""Longitudinal Multi-Pillar Synthetic Cohort Generator for AegisTwin.

Generates 1,500+ diverse member journeys (24 months) across Claims, EHR, SDOH,
and Wearables with latent physiological trajectories and injected clinical tripwires.
"""

import math
import random
from datetime import date, datetime, timedelta
from typing import Dict, List, Tuple
import numpy as np

from aegistwin.data.schemas import (
    Condition, Coverage, Encounter, EncounterClass, Gender,
    MedicationDispense, Observation, ObservationCategory, Patient,
    SDOHProfile, WearableStream
)

RACES = ["White", "Black", "Hispanic", "Asian", "Native_American", "Other"]
INCOME_BRACKETS = ["Low", "Middle", "High"]

TRIPWIRE_DESCRIPTIONS = [
    "WARFARIN_NSAID_BLEEDING",
    "CLOPIDOGREL_OMEPRAZOLE_CYP2C19",
    "LISINOPRIL_SPIRONOLACTONE_HYPERKALEMIA",
    "SSRI_TRAMADOL_SEROTONIN",
    "METFORMIN_LOW_EGFR_LACTIC_ACIDOSIS",
    "PROPRANOLOL_ASTHMA_BRONCHOSPASM",
    "GERIATRIC_BEERS_BENZO_FALL",
    "GERIATRIC_BEERS_ANTICHOLINERGIC"
]

def generate_synthetic_cohort(
    n_members: int = 1500,
    start_date: date = date(2024, 1, 1),
    duration_months: int = 24,
    seed: int = 42
) -> Dict[str, list]:
    """Generates a complete multi-pillar synthetic population."""
    random.seed(seed)
    np.random.seed(seed)
    
    end_date = start_date + timedelta(days=duration_months * 30)
    
    patients: List[Patient] = []
    sdoh_profiles: List[SDOHProfile] = []
    coverages: List[Coverage] = []
    conditions: List[Condition] = []
    medications: List[MedicationDispense] = []
    observations: List[Observation] = []
    encounters: List[Encounter] = []
    wearables: List[WearableStream] = []
    tripwire_registry: Dict[str, str] = {}
    
    for i in range(n_members):
        pid = f"MEM-{100000 + i}"
        
        # Demographics
        age = int(np.clip(np.random.normal(56, 17), 18, 92))
        birth_d = date(end_date.year - age, random.randint(1, 12), random.randint(1, 28))
        gender = random.choice([Gender.MALE, Gender.FEMALE])
        race = random.choices(RACES, weights=[0.58, 0.18, 0.15, 0.06, 0.01, 0.02])[0]
        zip_5 = f"{random.randint(10000, 99999)}"
        enrollment_d = start_date - timedelta(days=random.randint(0, 365))
        
        patient = Patient(
            id=pid,
            name=f"Member_{pid}",
            birth_date=birth_d,
            gender=gender,
            race=race,
            zip_code=zip_5,
            enrollment_start=enrollment_d
        )
        patients.append(patient)
        
        # SDOH Profile
        adi = int(np.clip(np.random.beta(2, 2) * 100, 1, 100))
        svi = round(adi / 100.0 + random.uniform(-0.08, 0.08), 3)
        svi = float(np.clip(svi, 0.0, 1.0))
        is_low_income = adi > 65
        sdoh = SDOHProfile(
            patient_id=pid,
            zip_code=zip_5,
            area_deprivation_index=adi,
            social_vulnerability_index=svi,
            housing_unstable=(adi > 80 and random.random() < 0.35),
            food_insecure=(adi > 70 and random.random() < 0.40),
            income_bracket="Low" if is_low_income else random.choice(["Middle", "High"]),
            distance_to_primary_care_miles=round(random.uniform(0.5, 18.0) * (1.5 if adi > 60 else 1.0), 1),
            transportation_barrier=(adi > 75 and random.random() < 0.30)
        )
        sdoh_profiles.append(sdoh)
        
        # Coverage & Care Management
        coverage = Coverage(
            id=f"COV-{pid}",
            patient_id=pid,
            plan_type="Medicare_Advantage" if age >= 65 else random.choice(["Commercial_HMO", "Commercial_PPO", "Medicaid"]),
            care_management_enrolled=(random.random() < 0.18),
            enrollment_date=enrollment_d
        )
        coverages.append(coverage)
        
        # Latent Health State & Chronic Conditions
        has_htn = random.random() < (0.75 if age > 60 else 0.35)
        has_dm2 = random.random() < (0.40 if age > 50 else 0.15)
        has_chf = has_htn and (random.random() < (0.28 if age > 65 else 0.08))
        has_ckd = (has_htn or has_dm2) and (random.random() < (0.35 if age > 65 else 0.12))
        has_afib = random.random() < (0.20 if age > 68 else 0.04)
        has_asthma = random.random() < 0.12
        has_copd = (random.random() < 0.15) if age > 55 else False
        has_depression = random.random() < 0.22
        has_oa = random.random() < 0.30
        has_falls = (age >= 70 and random.random() < 0.25)
        
        # Assign clinical conditions
        assigned_codes = []
        if has_htn: assigned_codes.append(("I10", "Essential hypertension"))
        if has_dm2:
            if has_ckd:
                assigned_codes.append(("E11.22", "Type 2 diabetes with diabetic CKD"))
                assigned_codes.append(("N18.3", "Chronic kidney disease, stage 3"))
            else:
                assigned_codes.append(("E11.9", "Type 2 diabetes without complications"))
        elif has_ckd:
            assigned_codes.append(("N18.3", "Chronic kidney disease, stage 3"))
        if has_chf: assigned_codes.append(("I50.9", "Heart failure"))
        if has_afib: assigned_codes.append(("I48.91", "Unspecified atrial fibrillation"))
        if has_asthma: assigned_codes.append(("J45.909", "Unspecified asthma"))
        if has_copd: assigned_codes.append(("J44.9", "COPD, unspecified"))
        if has_depression: assigned_codes.append(("F32.9", "Major depressive disorder"))
        if has_oa: assigned_codes.append(("M17.9", "Osteoarthritis of knee"))
        if has_falls: assigned_codes.append(("R29.6", "Repeated falls / Fall history"))
        
        for code, disp in assigned_codes:
            conditions.append(Condition(
                id=f"COND-{pid}-{code}",
                patient_id=pid,
                icd10_code=code,
                display=disp,
                onset_date=enrollment_d + timedelta(days=random.randint(10, 180))
            ))
            
        # Injected Clinical Tripwires Assignment
        assigned_tripwire = None
        if i % 8 == 0 and has_afib:
            assigned_tripwire = "WARFARIN_NSAID_BLEEDING"
        elif i % 8 == 1:
            assigned_tripwire = "CLOPIDOGREL_OMEPRAZOLE_CYP2C19"
        elif i % 8 == 2 and has_chf:
            assigned_tripwire = "LISINOPRIL_SPIRONOLACTONE_HYPERKALEMIA"
        elif i % 8 == 3 and has_depression:
            assigned_tripwire = "SSRI_TRAMADOL_SEROTONIN"
        elif i % 8 == 4 and has_dm2:
            assigned_tripwire = "METFORMIN_LOW_EGFR_LACTIC_ACIDOSIS"
        elif i % 8 == 5 and has_asthma:
            assigned_tripwire = "PROPRANOLOL_ASTHMA_BRONCHOSPASM"
        elif i % 8 == 6 and age >= 72 and has_falls:
            assigned_tripwire = "GERIATRIC_BEERS_BENZO_FALL"
        elif i % 8 == 7 and age >= 70:
            assigned_tripwire = "GERIATRIC_BEERS_ANTICHOLINERGIC"
            
        if assigned_tripwire:
            tripwire_registry[pid] = assigned_tripwire
            
        # Prescriptions & Dispenses (Monthly refills across 24 months)
        # Choose baseline meds
        active_drug_cuis = []
        if has_htn and assigned_tripwire != "LISINOPRIL_SPIRONOLACTONE_HYPERKALEMIA":
            active_drug_cuis.append(("29046", "Lisinopril 10mg", "ACE_Inhibitor", 10.0))
        if has_dm2:
            active_drug_cuis.append(("6809", "Metformin 500mg", "Biguanide", 1000.0))
        if has_afib:
            active_drug_cuis.append(("855332", "Warfarin Sodium 5mg", "Anticoagulant", 5.0))
        if has_depression:
            active_drug_cuis.append(("36437", "Sertraline 50mg", "SSRI", 50.0))
            
        # Inject tripwire drugs
        if assigned_tripwire == "WARFARIN_NSAID_BLEEDING":
            active_drug_cuis.append(("855332", "Warfarin Sodium 5mg", "Anticoagulant", 5.0))
            active_drug_cuis.append(("5640", "Ibuprofen 400mg", "NSAID", 800.0))
        elif assigned_tripwire == "CLOPIDOGREL_OMEPRAZOLE_CYP2C19":
            active_drug_cuis.append(("32968", "Clopidogrel 75mg", "Antiplatelet", 75.0))
            active_drug_cuis.append(("7646", "Omeprazole 20mg", "Proton_Pump_Inhibitor", 20.0))
        elif assigned_tripwire == "LISINOPRIL_SPIRONOLACTONE_HYPERKALEMIA":
            active_drug_cuis.append(("29046", "Lisinopril 20mg", "ACE_Inhibitor", 20.0))
            active_drug_cuis.append(("9997", "Spironolactone 50mg", "Aldosterone_Antagonist", 50.0))
        elif assigned_tripwire == "SSRI_TRAMADOL_SEROTONIN":
            active_drug_cuis.append(("36437", "Sertraline 100mg", "SSRI", 100.0))
            active_drug_cuis.append(("10689", "Tramadol 50mg", "Opioid_Analgesic", 100.0))
        elif assigned_tripwire == "METFORMIN_LOW_EGFR_LACTIC_ACIDOSIS":
            active_drug_cuis.append(("6809", "Metformin 1000mg", "Biguanide", 1000.0))
        elif assigned_tripwire == "PROPRANOLOL_ASTHMA_BRONCHOSPASM":
            active_drug_cuis.append(("8703", "Propranolol 40mg", "Nonselective_Beta_Blocker", 40.0))
        elif assigned_tripwire == "GERIATRIC_BEERS_BENZO_FALL":
            active_drug_cuis.append(("3322", "Diazepam 5mg", "LongActing_Benzodiazepine", 5.0))
        elif assigned_tripwire == "GERIATRIC_BEERS_ANTICHOLINERGIC":
            active_drug_cuis.append(("3498", "Diphenhydramine 25mg", "FirstGen_Antihistamine", 50.0))

        # Adherence profile
        base_pdc = np.clip(np.random.beta(5, 2 if not is_low_income else 3.5), 0.35, 1.0)
        
        for rx_cui, dname, dclass, dose in active_drug_cuis:
            # Generate refills roughly every 30-40 days
            cur_date = start_date + timedelta(days=random.randint(0, 30))
            while cur_date < end_date:
                # Stochastic non-adherence gap
                if random.random() > base_pdc:
                    cur_date += timedelta(days=random.randint(45, 90))
                    continue
                medications.append(MedicationDispense(
                    id=f"DISP-{pid}-{rx_cui}-{cur_date.strftime('%Y%m%d')}",
                    patient_id=pid,
                    ndc=f"00000-{rx_cui[:4]}-01",
                    rxnorm_cui=rx_cui,
                    drug_name=dname,
                    therapeutic_class=dclass,
                    dispense_date=cur_date,
                    days_supply=30,
                    quantity_dispensed=30.0,
                    dose_mg_per_day=dose,
                    claim_cost=round(random.uniform(15.0, 180.0), 2)
                ))
                cur_date += timedelta(days=random.randint(28, 34))
                
        # Longitudinal Labs (eGFR, HbA1c, Potassium)
        # Latent physiological trajectory: baseline + drift*time + noise
        egfr_base = 25.0 if assigned_tripwire == "METFORMIN_LOW_EGFR_LACTIC_ACIDOSIS" else (50.0 if has_ckd else random.uniform(70.0, 105.0))
        egfr_slope = -0.6 if has_ckd else -0.15 # points per month
        
        k_base = 5.3 if assigned_tripwire == "LISINOPRIL_SPIRONOLACTONE_HYPERKALEMIA" else 4.2
        hba1c_base = random.uniform(7.5, 9.8) if has_dm2 else random.uniform(5.1, 5.5)
        
        # Labs logged every 90-120 days
        lab_date = start_date + timedelta(days=random.randint(15, 60))
        month_idx = 0
        while lab_date < end_date:
            cur_egfr = round(float(np.clip(egfr_base + (egfr_slope * month_idx) + random.normalvariate(0, 2.5), 10.0, 120.0)), 1)
            cur_k = round(float(np.clip(k_base + (0.04 * month_idx if assigned_tripwire == "LISINOPRIL_SPIRONOLACTONE_HYPERKALEMIA" else 0.0) + random.normalvariate(0, 0.2), 3.0, 6.8)), 2)
            cur_a1c = round(float(np.clip(hba1c_base + random.normalvariate(0, 0.3), 4.5, 13.5)), 1)
            
            # eGFR
            observations.append(Observation(
                id=f"OBS-{pid}-EGFR-{lab_date.strftime('%Y%m%d')}",
                patient_id=pid,
                category=ObservationCategory.LABORATORY,
                loinc_code="33914-3",
                display="eGFR",
                effective_datetime=datetime.combine(lab_date, datetime.min.time()),
                value_numeric=cur_egfr,
                unit="mL/min/1.73m2",
                reference_range_low=60.0,
                reference_range_high=120.0
            ))
            # Potassium
            observations.append(Observation(
                id=f"OBS-{pid}-K-{lab_date.strftime('%Y%m%d')}",
                patient_id=pid,
                category=ObservationCategory.LABORATORY,
                loinc_code="2823-3",
                display="Potassium",
                effective_datetime=datetime.combine(lab_date, datetime.min.time()),
                value_numeric=cur_k,
                unit="mmol/L",
                reference_range_low=3.5,
                reference_range_high=5.0
            ))
            # HbA1c
            if has_dm2:
                observations.append(Observation(
                    id=f"OBS-{pid}-A1C-{lab_date.strftime('%Y%m%d')}",
                    patient_id=pid,
                    category=ObservationCategory.LABORATORY,
                    loinc_code="4548-4",
                    display="HbA1c",
                    effective_datetime=datetime.combine(lab_date, datetime.min.time()),
                    value_numeric=cur_a1c,
                    unit="%",
                    reference_range_low=4.0,
                    reference_range_high=5.6
                ))
                
            lab_date += timedelta(days=random.randint(85, 130))
            month_idx += 3
            
        # Wearable Telemetry (Sample 90 days of daily readings per member)
        base_steps = 7500 if age < 55 else 4800
        base_hr = 68.0 if not has_chf else 78.0
        wearable_start = end_date - timedelta(days=90)
        for d in range(90):
            day_dt = wearable_start + timedelta(days=d)
            # Decompensation in final 14 days for declining cases
            is_decomp = (has_chf or assigned_tripwire is not None) and (d >= 76)
            steps = int(max(400, np.random.normal(base_steps * (0.6 if is_decomp else 1.0), 900)))
            rhr = round(float(np.clip(np.random.normal(base_hr + (10.0 if is_decomp else 0.0), 3.5), 45.0, 115.0)), 1)
            sleep_eff = round(float(np.clip(np.random.normal(0.82 if not is_decomp else 0.65, 0.08), 0.40, 0.98)), 2)
            
            wearables.append(WearableStream(
                patient_id=pid,
                date=day_dt,
                daily_steps=steps,
                resting_heart_rate=rhr,
                sleep_efficiency_pct=sleep_eff
            ))
            
        # Clinical Encounters (Outpatient, ED, Inpatient)
        # Probability of acute event is a function of physiological risk + tripwires + random shock
        risk_latent = 0.05
        if has_chf: risk_latent += 0.22
        if has_ckd: risk_latent += 0.15
        if base_pdc < 0.6: risk_latent += 0.18
        if assigned_tripwire is not None: risk_latent += 0.35
        if sdoh.housing_unstable: risk_latent += 0.12
        if coverage.care_management_enrolled: risk_latent -= 0.15
        risk_latent = float(np.clip(risk_latent, 0.02, 0.88))
        
        # Outpatient PCP visits (1 to 4 per year)
        n_outpatient = random.randint(2, 6)
        for _ in range(n_outpatient):
            enc_date = start_date + timedelta(days=random.randint(10, duration_months * 30 - 10))
            enc_dt = datetime.combine(enc_date, datetime.min.time()) + timedelta(hours=random.randint(9, 16))
            encounters.append(Encounter(
                id=f"ENC-{pid}-{enc_date.strftime('%Y%m%d')}",
                patient_id=pid,
                encounter_class=EncounterClass.OUTPATIENT,
                start_date=enc_dt,
                end_date=enc_dt + timedelta(minutes=45),
                primary_diagnosis_icd10=assigned_codes[0][0] if assigned_codes else "Z00.00",
                total_cost=round(random.uniform(110.0, 260.0), 2)
            ))
            
        # Acute Events (ED / Inpatient)
        if random.random() < risk_latent:
            n_acute = 1 if random.random() < 0.75 else 2
            for _ in range(n_acute):
                acute_date = start_date + timedelta(days=random.randint(180, duration_months * 30 - 20))
                acute_dt = datetime.combine(acute_date, datetime.min.time()) + timedelta(hours=random.randint(1, 23))
                is_inp = random.random() < 0.45
                eclass = EncounterClass.INPATIENT if is_inp else EncounterClass.EMERGENCY
                los_hours = random.randint(36, 168) if is_inp else random.randint(3, 12)
                
                # Assign diagnosis aligned with risk
                if assigned_tripwire == "WARFARIN_NSAID_BLEEDING":
                    diag = "K92.2" # GI bleed
                elif assigned_tripwire == "LISINOPRIL_SPIRONOLACTONE_HYPERKALEMIA":
                    diag = "E87.5" # Hyperkalemia
                elif assigned_tripwire == "PROPRANOLOL_ASTHMA_BRONCHOSPASM":
                    diag = "J45.901" # Asthma with acute exacerbation
                elif has_chf:
                    diag = "I50.9" # Acute heart failure
                elif has_ckd:
                    diag = "N17.9" # Acute kidney injury
                else:
                    diag = "R07.9" # Chest pain
                    
                cost = round(random.uniform(6500.0, 24000.0) if is_inp else random.uniform(900.0, 3200.0), 2)
                readmit = (is_inp and random.random() < 0.22)
                
                encounters.append(Encounter(
                    id=f"ACUTE-{pid}-{acute_date.strftime('%Y%m%d')}",
                    patient_id=pid,
                    encounter_class=eclass,
                    start_date=acute_dt,
                    end_date=acute_dt + timedelta(hours=los_hours),
                    primary_diagnosis_icd10=diag,
                    total_cost=cost,
                    readmitted_within_30d=readmit
                ))
                
    return {
        "patients": patients,
        "sdoh_profiles": sdoh_profiles,
        "coverages": coverages,
        "conditions": conditions,
        "medications": medications,
        "observations": observations,
        "encounters": encounters,
        "wearables": wearables,
        "tripwires": tripwire_registry
    }
