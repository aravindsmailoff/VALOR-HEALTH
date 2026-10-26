"""FastAPI Production Service for Real-Time Event Scoring and CDS Triage."""

from datetime import datetime, date
from typing import Any, Dict, List, Optional
import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT.parent))
sys.path.insert(0, str(REPO_ROOT))
from fastapi import FastAPI, HTTPException, Depends, APIRouter
from pydantic import BaseModel, Field
from aegistwin.config.settings import settings
from aegistwin.data.schemas import (
    MedicationDispense, Observation, Encounter, MemberEvent, MemberEventType
)
from aegistwin.twin.state import MemberDigitalTwin
from aegistwin.twin.sensor import TwinEventSensor
from aegistwin.twin.simulator import WhatIfSimulator, SimulationIntervention, SimulationResult
from aegistwin.safety.ddi_engine import DDIEngine
from aegistwin.safety.dci_engine import DCIEngine
from aegistwin.safety.beers_engine import BeersEngine
from aegistwin.triage.router import TriageRouter, CDSTriageAlert
from aegistwin.triage.feedback_loop import FeedbackLoopManager
from aegistwin.compliance.security import SecurityAuditLogger

app = FastAPI(
    title="AegisTwin Enterprise Payer API",
    description="Stateful Member Digital Twin, Multi-Outcome Predictive Risk Stratification & Clinical Decision Support",
    version="1.0.0"
)

router = APIRouter()

# Global in-memory storage for active twins
TWIN_REGISTRY: Dict[str, MemberDigitalTwin] = {}
audit_logger = SecurityAuditLogger()
feedback_manager = FeedbackLoopManager()
triage_router = TriageRouter()
simulator = WhatIfSimulator()
sensor = TwinEventSensor()

class RealTimeEventRequest(BaseModel):
    patient_id: str
    event_type: str  # PRESCRIPTION_FILL, LAB_RESULT, ENCOUNTER
    payload: Dict[str, Any]
    actor_id: str = "SYS_FHIR_LISTENER"
    actor_role: str = "CARE_MANAGER"

class EventScoringResponse(BaseModel):
    patient_id: str
    calibrated_risk_90d: float
    risk_tier: str
    cds_alert: CDSTriageAlert
    safety_findings_count: int
    medication_diffs_detected: int
    layman_narrative: str
    clinical_reason_code: str

class OverrideRequest(BaseModel):
    alert_id: str
    patient_id: str
    clinician_id: str
    clinician_role: str
    override_reason: str
    notes: str

@router.get("/health")
def health_check():
    return {
        "status": "HEALTHY",
        "service": "AegisTwin Enterprise Payer Platform",
        "active_twins_monitored": len(TWIN_REGISTRY),
        "timestamp": datetime.now().isoformat()
    }

@router.get("/v1/twin/{patient_id}")
def get_member_twin(patient_id: str, actor_id: str = "PORTAL_USER", actor_role: str = "CARE_MANAGER"):
    audit_logger.log(actor_id=actor_id, role=actor_role, patient_id=patient_id, action="VIEW_TWIN")
    if patient_id not in TWIN_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Member twin '{patient_id}' not found.")
    twin = TWIN_REGISTRY[patient_id]
    return {
        "patient_id": twin.patient_id,
        "demographics": twin.demographics.model_dump(),
        "sdoh": twin.sdoh.model_dump(),
        "active_conditions": [c.model_dump() for c in twin.active_conditions.values()],
        "active_medications": [m.model_dump() for m in twin.active_medications.values()],
        "latest_egfr": twin.get_latest_lab("33914-3"),
        "latest_hba1c": twin.get_latest_lab("4548-4")
    }

@router.post("/v1/events/score", response_model=EventScoringResponse)
def score_realtime_event(req: RealTimeEventRequest):
    audit_logger.log(actor_id=req.actor_id, role=req.actor_role, patient_id=req.patient_id, action="SCORE_EVENT")
    if req.patient_id not in TWIN_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Member twin '{req.patient_id}' not found.")
    twin = TWIN_REGISTRY[req.patient_id]

    # Convert to MemberEvent and append
    ev = MemberEvent(
        event_id=f"EV-{int(datetime.now().timestamp()*1000)}",
        patient_id=req.patient_id,
        timestamp=datetime.now(),
        event_type=MemberEventType(req.event_type),
        payload=req.payload
    )
    twin.append_event(ev)

    # Sensor diffs
    med_diffs = []
    if req.event_type == "PRESCRIPTION_FILL":
        disp = MedicationDispense(**req.payload)
        med_diffs = sensor.evaluate_new_fill(twin, disp)

    # Track A: Safety Oracle
    safety_findings = simulator.run_safety_oracle(twin)

    # Track B: Risk Scoring
    risk_90d = simulator._default_surrogate_risk(twin)
    tier = "High" if risk_90d >= 0.35 else ("Medium" if risk_90d >= 0.18 else "Low")

    # CDS Alert Router
    alert = triage_router.route_alert(twin, risk_90d, safety_findings)

    clinical_code = f"Surrogate Log-Odds: risk={risk_90d:.3f}, critical_alerts={len([f for f in safety_findings if f.severity == 'CRITICAL'])}"
    layman_narrative = (
        f"Smart Guardian view: Health indicators evaluated. Risk score is {risk_90d*100:.1f}%. "
        + (f"Immediate attention needed for {safety_findings[0].plain_english_explanation}" if safety_findings else "No critical medication conflicts detected.")
    )

    return EventScoringResponse(
        patient_id=twin.patient_id,
        calibrated_risk_90d=round(risk_90d, 4),
        risk_tier=tier,
        cds_alert=alert,
        safety_findings_count=len(safety_findings),
        medication_diffs_detected=len(med_diffs),
        layman_narrative=layman_narrative,
        clinical_reason_code=clinical_code
    )

@router.post("/v1/simulations/run", response_model=SimulationResult)
def run_simulation(
    patient_id: str,
    intervention: SimulationIntervention,
    actor_id: str = "CLINICIAN_1",
    actor_role: str = "CARE_MANAGER"
):
    audit_logger.log(actor_id=actor_id, role=actor_role, patient_id=patient_id, action="RUN_SIMULATION")
    if patient_id not in TWIN_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Member twin '{patient_id}' not found.")
    twin = TWIN_REGISTRY[patient_id]
    res = simulator.simulate(twin, intervention)
    return res

@router.post("/v1/triage/override")
def record_clinician_override(req: OverrideRequest):
    audit_logger.log(
        actor_id=req.clinician_id,
        role=req.clinician_role,
        patient_id=req.patient_id,
        action="OVERRIDE_ALERT",
        details={"alert_id": req.alert_id, "reason": req.override_reason}
    )
    rec = feedback_manager.log_override(
        alert_id=req.alert_id,
        patient_id=req.patient_id,
        clinician_id=req.clinician_id,
        clinician_role=req.clinician_role,
        override_reason=req.override_reason,
        notes=req.notes
    )
    return {"status": "SUCCESS", "override_record": rec.model_dump()}

# Register routes for both root and /api path prefix
app.include_router(router)
app.include_router(router, prefix="/api")
