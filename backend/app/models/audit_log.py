"""Audit log model."""
from sqlalchemy import Column, Index, String, Text

from app.database import Base


class AuditLog(Base):
    """Audit logs for GDPR compliance and operations tracking."""
    __tablename__ = "audit_logs"
    
    audit_id = Column(String(50), primary_key=True)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(String(50), nullable=False)
    action = Column(String(50), nullable=False)
    actor_id = Column(String(50), nullable=False)
    trace_id = Column(String(50), nullable=False)
    payload_json = Column(Text, nullable=False)
    created_at = Column(Text, nullable=False)
    
    __table_args__ = (
        Index("idx_audit_logs_entity", "entity_type", "entity_id"),
        Index("idx_audit_logs_actor", "actor_id"),
        Index("idx_audit_logs_created", "created_at"),
    )
