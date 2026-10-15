"""Audit log schemas."""
from pydantic import BaseModel


class AuditLogEntry(BaseModel):
    """Audit log entry."""
    audit_id: str
    entity_type: str
    entity_id: str
    action: str
    actor_id: str
    trace_id: str
    payload_json: str
    created_at: str
