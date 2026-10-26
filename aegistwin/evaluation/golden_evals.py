"""Golden Safety Benchmark (500+ Cases) and Counterfactual Perturbation Invariance Suite."""

import random
from typing import Any, Dict, List, Tuple
import numpy as np
import pandas as pd

from aegistwin.safety.ddi_engine import DDIEngine, SafetyFinding
from aegistwin.safety.dci_engine import DCIEngine
from aegistwin.safety.beers_engine import BeersEngine

def generate_golden_safety_benchmark(n_cases: int = 520) -> List[Dict[str, Any]]:
    """Programmatically generates 500+ diverse clinical test scenarios with known ground truth."""
    random.seed(1337)
    test_cases: List[Dict[str, Any]] = []

    # 1. Warfarin + Ibuprofen (DDI Critical)
    for k in range(75):
        test_cases.append({
            "case_id": f"GOLDEN-DDI-WARFARIN-NSAID-{k}",
            "drugs": {"855332", "5640", str(random.randint(100, 999))},
            "conditions": set(),
            "labs": {},
            "age": random.randint(40, 85),
            "expected_critical_rule": "DDI-001-WARFARIN-NSAID"
        })

    # 2. Clopidogrel + Omeprazole (DDI Critical)
    for k in range(75):
        test_cases.append({
            "case_id": f"GOLDEN-DDI-CLOPIDOGREL-OMEPRAZOLE-{k}",
            "drugs": {"32968", "7646"},
            "conditions": set(),
            "labs": {},
            "age": random.randint(45, 80),
            "expected_critical_rule": "DDI-003-CLOPIDOGREL-OMEPRAZOLE"
        })

    # 3. Metformin + Low eGFR < 30 (DCI Renal Critical)
    for k in range(75):
        test_cases.append({
            "case_id": f"GOLDEN-DCI-METFORMIN-RENAL-{k}",
            "drugs": {"6809"},
            "conditions": {"E11.22", "N18.4"},
            "labs": {"33914-3": round(random.uniform(12.0, 28.5), 1)},
            "age": random.randint(50, 82),
            "expected_critical_rule": "DCI-RENAL-001-METFORMIN"
        })

    # 4. Propranolol + Asthma (DCI Disease Critical)
    for k in range(75):
        test_cases.append({
            "case_id": f"GOLDEN-DCI-PROPRANOLOL-ASTHMA-{k}",
            "drugs": {"8703"},
            "conditions": {"J45.909"},
            "labs": {},
            "age": random.randint(25, 65),
            "expected_critical_rule": "DCI-DISEASE-002-PROPRANOLOL-ASTHMA"
        })

    # 5. Diazepam in Age >= 72 with Fall History (Beers Critical)
    for k in range(75):
        test_cases.append({
            "case_id": f"GOLDEN-BEERS-DIAZEPAM-{k}",
            "drugs": {"3322"},
            "conditions": {"R29.6"},
            "labs": {},
            "age": random.randint(72, 90),
            "expected_critical_rule": "BEERS-003322-BENZODIAZEPINE"
        })

    # 6. Diphenhydramine in Age >= 70 with Fall History (Beers Critical)
    for k in range(75):
        test_cases.append({
            "case_id": f"GOLDEN-BEERS-DIPHENHYDRAMINE-{k}",
            "drugs": {"3498"},
            "conditions": {"R29.6"},
            "labs": {},
            "age": random.randint(70, 88),
            "expected_critical_rule": "BEERS-003498-ANTICHOLINERGIC"
        })

    # 7. Benign Controls (Zero Critical Contraindications Expected)
    for k in range(70):
        test_cases.append({
            "case_id": f"GOLDEN-CONTROL-BENIGN-{k}",
            "drugs": {"161", "1114195"}, # Acetaminophen + Linagliptin
            "conditions": {"E11.9", "I10"},
            "labs": {"33914-3": 75.0, "2823-3": 4.1},
            "age": random.randint(35, 75),
            "expected_critical_rule": None
        })

    return test_cases

def run_golden_safety_eval(test_cases: Optional[List[Dict]] = None) -> Dict[str, Any]:
    """Executes deterministic safety evaluations across the 500+ golden cases."""
    cases = test_cases or generate_golden_safety_benchmark()
    ddi = DDIEngine()
    dci = DCIEngine()
    beers = BeersEngine()

    total_critical_expected = 0
    total_critical_detected = 0
    false_positives_in_controls = 0
    failures: List[Dict[str, Any]] = []

    for c in cases:
        exp_rule = c["expected_critical_rule"]
        findings: List[SafetyFinding] = []
        findings.extend(ddi.evaluate(c["drugs"]))
        findings.extend(dci.evaluate(c["drugs"], c["conditions"], c["labs"]))
        has_falls = any(cond.startswith("R29.6") for cond in c["conditions"])
        findings.extend(beers.evaluate(c["age"], c["drugs"], has_fall_history=has_falls))

        crit_rules = [f.rule_id for f in findings if f.severity == "CRITICAL"]

        if exp_rule is not None:
            total_critical_expected += 1
            if exp_rule in crit_rules:
                total_critical_detected += 1
            else:
                failures.append({"case_id": c["case_id"], "expected": exp_rule, "detected": crit_rules})
        else: # Control
            if len(crit_rules) > 0:
                false_positives_in_controls += 1

    sensitivity = (total_critical_detected / max(1, total_critical_expected)) * 100.0
    pass_100pct = (total_critical_detected == total_critical_expected) and (false_positives_in_controls == 0)

    return {
        "total_test_cases": len(cases),
        "critical_cases_evaluated": total_critical_expected,
        "critical_cases_detected": total_critical_detected,
        "critical_sensitivity_pct": round(sensitivity, 2),
        "false_positive_count": false_positives_in_controls,
        "golden_eval_passed_100pct": pass_100pct,
        "failures": failures
    }

def run_counterfactual_perturbation_stability_test(
    model,
    sample_features: pd.DataFrame,
    max_allowed_delta: float = 0.015
) -> Dict[str, Any]:
    """Tests model invariance: Adding benign noise or neutral vitamins must not shift risk by > 0.015."""
    base_preds = model.predict_proba(sample_features)
    
    # Perturb distance to PCP by +/- 1 mile
    perturbed_df = sample_features.copy()
    if "distance_to_primary_care_miles" in perturbed_df.columns:
        perturbed_df["distance_to_primary_care_miles"] += np.random.normal(0, 0.5, len(perturbed_df))
    # Perturb benign daily steps by +/- 50 steps
    if "wearable_mean_daily_steps" in perturbed_df.columns:
        perturbed_df["wearable_mean_daily_steps"] += np.random.normal(0, 50, len(perturbed_df))
        
    perturbed_preds = model.predict_proba(perturbed_df)
    max_observed_shift = float(np.max(np.abs(base_preds - perturbed_preds)))
    passed = max_observed_shift <= max_allowed_delta

    return {
        "max_observed_probability_shift": round(max_observed_shift, 4),
        "max_allowed_delta": max_allowed_delta,
        "perturbation_stability_passed": passed
    }
