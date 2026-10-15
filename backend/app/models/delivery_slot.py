"""Delivery slot model."""
from sqlalchemy import Column, Index, Integer, String, Text

from app.database import Base


class DeliverySlot(Base):
    """Delivery slots with capacity management."""
    __tablename__ = "delivery_slots"
    
    slot_id = Column(String(50), primary_key=True)
    slot_date = Column(Text, nullable=False)
    start_time = Column(String(10), nullable=False)
    end_time = Column(String(10), nullable=False)
    label = Column(String(100))
    max_capacity = Column(Integer, nullable=False)
    reserved_count = Column(Integer, default=0)
    is_available = Column(Text, default="true")
    service_zone = Column(String(100))
    created_at = Column(Text, nullable=False)
    updated_at = Column(Text, nullable=False)
    
    __table_args__ = (
        Index("idx_delivery_slots_date", "slot_date"),
        Index("idx_delivery_slots_zone", "service_zone"),
        Index("idx_delivery_slots_availability", "is_available"),
    )
