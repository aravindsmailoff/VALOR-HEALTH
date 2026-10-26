"""Clinician Override Capture and Active Learning Feedback Loop."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from aegistwin.config.settings import settings

OVERRIDE_REASONS = [
    "CLINICAL_BENEFIT_OUTWEIGHS_RISK",
    "SPECIALIST_MONITORING_ALREADY_IN_PLACE",
    "PATIENT_INTOLERANT_TO_ALTERNATIVE_DRUG",
    "FALSE_POSITIVE_CODING_OR_CHRONIC_TOLERANCE",
    "PATIENT_REFUSED_MEDICATION_SUBSTITUTION",
    "PALLIATIVE_OR_HOSPICE_GOALS_OF_CARE"
]

class ClinicianOverrideRecord(BaseModel):
    override_id: str
    alert_id: str
    patient_id: str
    clinician_id: str
    clinician_role: str
    timestamp: datetime = Field(default_factory=datetime.now)
    override_reason: str
    clinical_justification_notes: str
    action_taken: str = "OVERRIDDEN"

class FeedbackLoopManager:
    """Manages human-in-the-loop clinician feedback and active learning audit records."""

    def __init__(self, log_path: Optional[Path] = None):
        self.log_path = log_path or (settings.BASE_DIR / "artifacts" / "clinician_overrides.jsonl")
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log_override(
        self,
        alert_id: str,
        patient_id: str,
        clinician_id: str,
        clinician_role: str,
        override_reason: str,
        notes: str
    ) -> ClinicianOverrideRecord:
        """Captures structured clinician override and appends to immutable feedback log."""
        if override_reason not in OVERRIDE_REASONS:
            override_reason = "CLINICAL_BENEFIT_OUTWEIGHS_RISK"

        record = ClinicianOverrideRecord(
            override_id=f"OVR-{int(datetime.now().timestamp()*1000)}",
            alert_id=alert_id,
            patient_id=patient_id,
            clinician_id=clinician_id,
            clinician_role=clinician_role,
            override_reason=override_reason,
            clinical_justification_notes=notes
        )

        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(record.model_dump_json() + "\n")

        return record

    def get_recent_overrides(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Reads recent clinician overrides for review and retraining audits."""
        if not self.log_path.exists():
            return []
        records = []
        with open(self.log_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    records.append(json.loads(line.strip()))
        return records[-limit:]
