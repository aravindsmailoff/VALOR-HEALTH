# Model Card: AegisTwin Enterprise Predictive Risk & Safety Oracle

## Model Details
- **Architecture**: Dual-Track Intelligence Pipeline:
  - **Track A**: Deterministic Knowledge-Graph Safety Oracle (RxNorm, openFDA, AGS Beers Criteria).
  - **Track B**: Multi-Outcome Calibrated Gradient Boosted Trees (HistGradientBoosting / LightGBM) + Cox Proportional Hazards Survival Analysis + T-Learner Causal Uplift.
- **Version**: 1.0.0 (Enterprise Payer Edition)
- **Frameworks**: Python 3.11+, Scikit-Learn, LightGBM, Lifelines, Pydantic v2.

## Intended Use
- **Primary Use Case**: Continuous population risk stratification and proactive clinical decision support (CDS) for health maintenance organizations, commercial insurers, and Medicare Advantage plans.
- **Intended Users**: Clinical Pharmacists, Nurse Care Managers, Medical Directors, and Member Outreach Coordinators.
- **Out of Scope**: Real-time intensive care titration or replacing licensed independent physician diagnostic authority.

## Outcomes Predicted
1. `outcome_90d_acute`: 90-day unplanned acute emergency department visit or inpatient hospitalization.
2. `outcome_30d_readmission`: 30-day post-discharge inpatient readmission.
3. `outcome_12m_progression`: 12-month chronic disease decompensation (CKD stage advancement, acute heart failure exacerbation).
4. `individual_treatment_effect`: Causal uplift score measuring absolute risk reduction from care coordination outreach.

## Anti-Bias Safeguards & Obermeyer Parity
- **Target Label Hygiene**: Strictly forbids financial claim costs as training labels, preventing the Obermeyer et al. (Science 2019) access-disparity bias.
- **Subgroup Parity Audit**: Monitored across race/ethnicity, administrative sex, age brackets, and Area Deprivation Index (ADI) quartiles.
- **Conformal Uncertainty**: Prediction intervals attached at the 90% confidence level; members with sparse lab history or short enrollment (<90d) flagged with `LOW_CONFIDENCE_SPARSE_DATA`.

## Ethical & Clinical Considerations
- High-risk CDS alerts require clinician human-in-the-loop review.
- Any dismissal of a Tier 1 Red Interrupt requires mandatory structured documentation of the clinical rationale.
