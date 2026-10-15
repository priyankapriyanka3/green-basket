"""Audit logging service for GDPR compliance tracking."""
import json
from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def log_audit_event(
    db: Session,
    entity_type: str,
    entity_id: str,
    action: str,
    actor_id: str,
    payload: dict | None = None,
    trace_id: str | None = None
) -> str:
    """
    Create audit log entry for GDPR compliance.
    
    Required domains per REQ-COMPLIANCE-001:
    - Profile changes (entity_type="customer", action="profile_update")
    - Order state transitions (entity_type="order", action="status_change")
    - Payment state changes (entity_type="payment", action="status_change")
    - Promotion changes (entity_type="promotion", action="rule_update")
    - Serviceability rule changes (entity_type="serviceability", action="rule_update")
    
    Retention: >= 180 days
    
    Args:
        db: Database session
        entity_type: Type of entity (customer, order, payment, promotion, serviceability)
        entity_id: Entity identifier
        action: Action performed (profile_update, status_change, rule_update, etc.)
        actor_id: Customer ID or operator ID who performed the action
        payload: Optional payload data (will be serialized to JSON)
        trace_id: Optional trace ID for correlation
    
    Returns:
        audit_id of created log entry
    """
    audit_id = f"aud-{uuid4().hex[:12]}"
    
    if trace_id is None:
        trace_id = f"trc-{datetime.now(UTC).strftime('%Y%m%d')}-{uuid4().hex[:8]}"
    
    payload_json = "{}"
    if payload:
        try:
            payload_json = json.dumps(payload)
        except (TypeError, ValueError):
            payload_json = json.dumps({"error": "failed_to_serialize"})
    
    audit_entry = AuditLog(
        audit_id=audit_id,
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        actor_id=actor_id,
        trace_id=trace_id,
        payload_json=payload_json,
        created_at=datetime.now(UTC).isoformat()
    )
    
    db.add(audit_entry)
    db.commit()
    
    return audit_id
