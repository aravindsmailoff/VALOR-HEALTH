"""Tests for Track A Deterministic Safety Oracle (DDI, DCI, Beers Criteria)."""

import pytest
from aegistwin.safety.ddi_engine import DDIEngine
from aegistwin.safety.dci_engine import DCIEngine
from aegistwin.safety.beers_engine import BeersEngine
from aegistwin.evaluation.golden_evals import run_golden_safety_eval

def test_ddi_warfarin_nsaid_detection():
    """Verify Warfarin + Ibuprofen triggers CRITICAL DDI."""
    engine = DDIEngine()
    findings = engine.evaluate({"855332", "5640"})
    assert len(findings) == 1
    assert findings[0].rule_id == "DDI-001-WARFARIN-NSAID"
    assert findings[0].severity == "CRITICAL"

def test_ddi_clopidogrel_omeprazole_detection():
    """Verify Clopidogrel + Omeprazole triggers CRITICAL CYP2C19 DDI."""
    engine = DDIEngine()
    findings = engine.evaluate({"32968", "7646"})
    assert len(findings) == 1
    assert findings[0].rule_id == "DDI-003-CLOPIDOGREL-OMEPRAZOLE"
    assert findings[0].severity == "CRITICAL"

def test_dci_metformin_low_egfr_detection():
    """Verify Metformin with eGFR < 30 triggers CRITICAL lactic acidosis alert."""
    engine = DCIEngine()
    findings = engine.evaluate(
        active_rxcui_set={"6809"},
        active_conditions={"E11.9"},
        recent_labs={"33914-3": 24.5} # eGFR = 24.5 mL/min
    )
    assert len(findings) == 1
    assert findings[0].rule_id == "DCI-RENAL-001-METFORMIN"
    assert findings[0].severity == "CRITICAL"

def test_dci_propranolol_asthma_detection():
    """Verify Non-selective Beta-blocker with asthma triggers CRITICAL bronchospasm alert."""
    engine = DCIEngine()
    findings = engine.evaluate(
        active_rxcui_set={"8703"}, # Propranolol
        active_conditions={"J45.909"}, # Asthma
        recent_labs={}
    )
    assert len(findings) == 1
    assert findings[0].rule_id == "DCI-DISEASE-002-PROPRANOLOL-ASTHMA"
    assert findings[0].severity == "CRITICAL"

def test_beers_criteria_elderly_anticholinergic_and_fall():
    """Verify Diphenhydramine in age >= 65 with fall history triggers CRITICAL Beers alert."""
    engine = BeersEngine()
    findings = engine.evaluate(
        patient_age=74,
        active_rxcui_set={"3498"},
        has_fall_history=True
    )
    assert len(findings) == 1
    assert findings[0].severity == "CRITICAL"
    assert "BEERS" in findings[0].rule_id

def test_golden_safety_benchmark_100pct_pass():
    """Assert 100% sensitivity across 500+ golden edge cases."""
    report = run_golden_safety_eval()
    assert report["critical_sensitivity_pct"] == 100.0
    assert report["golden_eval_passed_100pct"] is True
    assert report["false_positive_count"] == 0
