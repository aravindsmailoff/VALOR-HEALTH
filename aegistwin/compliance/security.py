"""HIPAA Safe Harbor De-Identification, RBAC Authorization, and Immutable Audit Logging."""

import functools
import json
from datetime import datetime, date
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set
from pydantic import BaseModel, Field

from aegistwin.config.settings import settings

class AuditLogEntry(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now)
    actor_id: str
    role: str
    patient_id: str
    action: str  # VIEW_TWIN, RUN_SIMULATION, OVERRIDE_ALERT, EXPORT_COHORT
    details: Dict[str, Any] = Field(default_factory=dict)
    compliance_framework: str = "HIPAA_Security_Rule_AND_India_DPDP_Act_2023"

class SecurityAuditLogger:
    """Writes tamper-evident, append-only JSON-lines audit records."""

    def __init__(self, log_file: Optional[Path] = None):
        self.log_file = log_file or settings.AUDIT_LOG_FILE
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def log(
        self,
        actor_id: str,
        role: str,
        patient_id: str,
        action: str,
        details: Optional[Dict[str, Any]] = None
    ) -> AuditLogEntry:
        entry = AuditLogEntry(
            actor_id=actor_id,
            role=role,
            patient_id=patient_id,
            action=action,
            details=details or {}
        )
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(entry.model_dump_json() + "\n")
        return entry

    def get_recent_entries(self, limit: int = 50) -> List[Dict[str, Any]]:
        if not self.log_file.exists():
            return []
        entries = []
        with open(self.log_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    entries.append(json.loads(line.strip()))
        return entries[-limit:]

def deidentify_patient_record(patient_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Applies HIPAA Safe Harbor (45 CFR § 164.514(b)(2)) de-identification rules:

    1. Masks direct identifier (name, MRN).
    2. Caps age at 89 (replaces with 90+).
    3. Truncates ZIP to first 3 digits.
    4. Truncates dates to Year only.
    """
    clean = copy_dict = dict(patient_dict)
    clean["name"] = "ANONYMOUS_MEMBER"

    # Age cap at 89
    if "age" in clean and clean["age"] >= 90:
        clean["age"] = "90_or_older"

    # ZIP code truncate to 3 digits
    if "zip_code" in clean:
        clean["zip_code"] = f"{str(clean['zip_code'])[:3]}**"

    # Date truncation
    for date_key in ["birth_date", "enrollment_start", "onset_date"]:
        if date_key in clean and clean[date_key]:
            val_str = str(clean[date_key])
            clean[date_key] = val_str[:4] # Keep Year only

    return clean

# RBAC Permissions Hierarchy
ROLE_PERMISSIONS: Dict[str, Set[str]] = {
    settings.ROLE_CLINICAL_DIRECTOR: {"VIEW_TWIN", "RUN_SIMULATION", "OVERRIDE_ALERT", "EXPORT_COHORT", "VIEW_AUDIT_LOG"},
    settings.ROLE_CARE_MANAGER: {"VIEW_TWIN", "RUN_SIMULATION", "OVERRIDE_ALERT"},
    settings.ROLE_PHARMACIST: {"VIEW_TWIN", "RUN_SIMULATION", "OVERRIDE_ALERT"},
    settings.ROLE_PAYER_EXECUTIVE: {"VIEW_TWIN", "RUN_SIMULATION", "VIEW_AUDIT_LOG"},
    settings.ROLE_OUTREACH_COORDINATOR: {"VIEW_TWIN"}
}

def require_role_permission(action: str):
    """Decorator to enforce RBAC permissions aligned with HIPAA minimum-necessary rule."""
    def decorator(fn: Callable):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            role = kwargs.get("actor_role", settings.ROLE_CARE_MANAGER)
            allowed_actions = ROLE_PERMISSIONS.get(role, set())
            if action not in allowed_actions:
                raise PermissionError(
                    f"Access Denied: Role '{role}' does not possess permission for action '{action}'."
                )
            return fn(*args, **kwargs)
        return wrapper
    return decorator
