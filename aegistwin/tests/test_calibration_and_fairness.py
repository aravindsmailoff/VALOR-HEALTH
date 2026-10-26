"""Tests for Calibration, Conformal Uncertainty, and Subgroup Fairness Auditing."""

import numpy as np
import pandas as pd
import pytest

from aegistwin.models.calibration_uncertainty import CalibratorAndConformalEngine
from aegistwin.evaluation.metrics import evaluate_clinical_model_metrics, compute_calibration_curve
from aegistwin.evaluation.fairness_audit import run_subgroup_fairness_audit, run_obermeyer_proxy_bias_demonstration

def test_calibration_and_conformal_intervals():
    """Verify calibration fitting and conformal prediction interval coverage."""
    np.random.seed(42)
    n = 200
    # True probabilities and uncalibrated logits
    true_probs = np.random.uniform(0.1, 0.8, n)
    y_val = (np.random.uniform(0, 1, n) < true_probs).astype(int)
    # Distorted/overconfident raw model probabilities
    raw_probs = np.clip(true_probs ** 1.8 + np.random.normal(0, 0.05, n), 0.01, 0.99)

    engine = CalibratorAndConformalEngine(confidence_level=0.90)
    engine.fit_calibration(raw_probs, y_val)

    assert engine.fitted is True

    # Calibrate single sample
    p_cal = float(engine.calibrate(np.array([0.45]), method="isotonic")[0])
    assert 0.01 <= p_cal <= 0.99

    # Conformal interval
    low, high, flag = engine.predict_conformal_interval(p_cal, is_sparse_data=False)
    assert low <= p_cal <= high
    assert flag == "HIGH_CONFIDENCE"

    # Sparse data should widen interval
    low_s, high_s, flag_s = engine.predict_conformal_interval(p_cal, is_sparse_data=True)
    assert (high_s - low_s) >= (high - low)
    assert flag_s == "LOW_CONFIDENCE_SPARSE_DATA"

def test_clinical_metrics_scorecard():
    """Verify AUROC, AUPRC, Brier, and DCA calculations."""
    y_true = np.array([1, 0, 1, 1, 0, 0, 1, 0, 1, 0] * 10)
    y_prob = np.array([0.9, 0.1, 0.8, 0.7, 0.2, 0.3, 0.85, 0.15, 0.65, 0.25] * 10)

    scorecard = evaluate_clinical_model_metrics(y_true, y_prob)
    assert scorecard["auroc"] > 0.85
    assert scorecard["brier_score"] < 0.20
    assert scorecard["precision_at_10pct"] >= 0.70
    assert len(scorecard["calibration_curve"]) == 10
    assert len(scorecard["decision_curve"]) > 0

def test_obermeyer_bias_audit():
    """Verify that the Obermeyer bias audit flags discrepancy between cost and clinical labels."""
    df = pd.DataFrame({
        "adi_quartile": ["Q1_Low", "Q1_Low", "Q4_High", "Q4_High"] * 25,
        "outcome_90d_acute": [0, 0, 1, 1] * 25,
        "cost_proxy_target": [1, 0, 0, 0] * 25,
        "pred_prob_clinical": [0.15, 0.20, 0.65, 0.70] * 25,
        "pred_prob_cost": [0.60, 0.55, 0.25, 0.30] * 25
    })
    demo = run_obermeyer_proxy_bias_demonstration(df)
    assert "quartile_breakdown" in demo
    assert len(demo["quartile_breakdown"]) == 2
    # Verify cost model underestimation gap in high-deprivation quartile
    q4_record = next(r for r in demo["quartile_breakdown"] if r["adi_quartile"] == "Q4_High")
    assert q4_record["cost_model_underestimation_gap"] > 0.30
