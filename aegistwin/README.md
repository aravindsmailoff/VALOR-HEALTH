# AegisTwin (Enterprise Payer Edition)

**Stateful Member Digital Twin, Multi-Outcome Predictive Risk Stratification, Medication Safety Oracle & Clinical Decision Support (CDS) Platform**

AegisTwin replaces monthly batch claims scoring with a **continuous, stateful Member Digital Twin**. When a member fills a prescription, completes a lab, visits urgent care, or logs wearable telemetry, AegisTwin executes a **Dual-Track Intelligence Pipeline**:
1. **Track A — Deterministic Clinical Safety Oracle (The Rulebook):** Evaluates curated medical ontologies (RxNorm, openFDA, AGS Beers Criteria) to detect Drug-Drug Interactions (DDI), Drug-Condition Contraindications (DCI), and organ-function breaches.
2. **Track B — Probabilistic ML Risk, Survival & Uplift Engine (The Forecast):** Calibrated Gradient Boosted Trees, Survival Analysis (time-to-event), Conformal Prediction, and Causal Uplift Modeling to prioritize impactable members for care-team outreach.

---

## Architecture Overview

```
aegistwin/
├── run_pipeline.py                     # Master CLI: setup -> train -> evals -> serve -> app
├── config/settings.py                  # Thresholds, capacity tiers, lookback windows, RBAC
├── data/
│   ├── schemas.py                      # FHIR R4-compatible Pydantic v2 models
│   ├── ontologies.py                   # RxNorm, ICD-10, CCSR, Charlson, Elixhauser, Beers
│   ├── synthetic_generator.py          # 1,500+ members (24 months) across 4 pillars
│   └── ingestion_validator.py          # Validation & adapters (Synthea, CMS, MIMIC-IV)
├── twin/
│   ├── state.py                        # Stateful Member Digital Twin with point-in-time replay
│   ├── sensor.py                       # Medication diffs, rolling 90d PDC, lab slope & wearable drift
│   └── simulator.py                    # Counterfactual What-If Flight Simulator
├── safety/
│   ├── ddi_engine.py                   # Deterministic DDI knowledge graph
│   ├── dci_engine.py                   # Renal (eGFR) and disease contraindications
│   └── beers_engine.py                 # Geriatric (Age >= 65) AGS Beers safety checker
├── models/
│   ├── cohort_builder.py               # Temporal split (Months 1-14, 15-18, 19-24)
│   ├── feature_store.py                # Zero-lookahead point-in-time feature engineering
│   ├── baseline_lr.py                  # L2-regularized Logistic Regression
│   ├── risk_gbm.py                     # Multi-outcome GBDT (90d Acute, Readmit, Progression)
│   ├── survival_model.py               # Time-to-event survival hazard curves
│   ├── uplift_model.py                 # Causal Uplift T-Learner (Individual Treatment Effect)
│   ├── calibration_uncertainty.py      # Isotonic/Platt calibration & Split Conformal bounds
│   └── explainability.py               # Dual Explainability (Clinical Reason Codes + Layman)
├── llm_brief/note_summarizer.py        # Guardrailed brief synthesizer & hallucination verifier
├── triage/
│   ├── router.py                       # 3-Tier CDS Alert Router & Capacity Tiering
│   └── feedback_loop.py                # Clinician override capture & active learning log
├── evaluation/
│   ├── metrics.py                      # AUROC, AUPRC, Brier, ECE, DCA Net Benefit
│   ├── fairness_audit.py               # Subgroup parity & Obermeyer anti-cost-proxy proof
│   └── golden_evals.py                 # 500+ golden test cases (100% sensitivity required)
├── monitoring/drift_detector.py        # PSI feature & score drift detector
├── compliance/security.py              # HIPAA Safe Harbor & immutable audit log
├── serving/api.py                      # FastAPI microservice
└── app/dashboard.py                    # 6-Tab Streamlit Dashboard with Dual-Audience toggle
```

---

## Quickstart

### 1. Run Complete End-to-End Pipeline Setup (< 60s)
Generates data, trains models, runs calibrations, runs 520-case golden safety evals, audits fairness, and saves all artifacts:
```bash
python run_pipeline.py --setup
```

### 2. Launch FastAPI Service
```bash
python run_pipeline.py --serve
# API docs available at: http://localhost:8000/docs
```

### 3. Launch Interactive Streamlit Dashboard
```bash
python run_pipeline.py --app
# Opens dashboard at: http://localhost:8501
```

### 4. Run Test Suite
```bash
pytest tests/ -v
```
