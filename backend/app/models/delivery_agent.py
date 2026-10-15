"""Delivery agent model."""
from sqlalchemy import Column, Index, String, Text

from app.database import Base


class DeliveryAgent(Base):
    """Delivery agents for order fulfillment."""
    __tablename__ = "delivery_agents"
    
    agent_id = Column(String(50), primary_key=True)
    name = Column(String(200), nullable=False)
    phone_number = Column(String(20), nullable=False)
    vehicle_type = Column(String(50))
    service_zone = Column(String(100))
    status = Column(String(20), default="active")
    created_at = Column(Text, nullable=False)
    updated_at = Column(Text, nullable=False)
    
    __table_args__ = (
        Index("idx_delivery_agents_zone", "service_zone"),
        Index("idx_delivery_agents_status", "status"),
    )
