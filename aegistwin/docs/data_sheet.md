# Data Sheet: AegisTwin Longitudinal Synthetic Population

*Standardized Dataset Documentation based on Gebru et al. (CACM 2021)*

## 1. Motivation
- **Purpose**: Facilitate robust clinical risk stratification, medication safety evaluation, and causal uplift prioritization for health insurance payers without compromising Protected Health Information (PHI).
- **Creators**: AegisTwin Informaticians & Clinical MLOps Team.

## 2. Composition
- **Population Size**: 1,500+ longitudinal member journeys spanning 24 consecutive months.
- **Data Pillars**:
  1. **Medical & Pharmacy Claims**: Inpatient, ED, and outpatient encounters, ICD-10 diagnosis codes, CPT procedure codes, NDC pharmacy dispenses, days supply, metric doses.
  2. **Electronic Health Records (EHR)**: LOINC laboratory trajectories (eGFR, HbA1c, Serum Creatinine, Potassium, NT-proBNP), vital signs (blood pressure, resting HR).
  3. **Social Determinants of Health (SDOH)**: 9-digit ZIP mapped to Area Deprivation Index (ADI 1–100), Social Vulnerability Index (SVI 0–1), housing stability indicators, food insecurity flags, and transit barriers.
  4. **Behavioral & Wearables**: Rolling Proportion of Days Covered (PDC), refill gaps, and 90-day daily telemetry (daily step count, resting heart rate, sleep efficiency).

## 3. Injected Clinical Tripwires
The synthetic dataset injects explicit pharmacovigilance edge cases:
- Warfarin + high-dose Ibuprofen/Naproxen (Critical GI bleed risk).
- Clopidogrel + Omeprazole (CYP2C19 antiplatelet inhibition).
- Lisinopril + Spironolactone in rising Potassium (Severe hyperkalemia).
- Metformin in eGFR < 30 mL/min/1.73m² (Lactic acidosis).
- Propranolol in active bronchial asthma (Refractory bronchospasm).
- Diazepam & Diphenhydramine in adults aged 70+ with fall history (AGS Beers Criteria).

## 4. Collection Process & Temporal Splitting
- **Chronological Split**:
  - Train: Months 1–14
  - Validation: Months 15–18
  - Test: Months 19–24
- **Anti-Leakage Standard**: All point-in-time features are computed via state reconstruction strictly using information timestamped on or before the index date.
