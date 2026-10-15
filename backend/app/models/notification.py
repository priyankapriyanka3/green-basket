"""Notification model."""
from sqlalchemy import Column, ForeignKey, Index, String, Text

from app.database import Base


class Notification(Base):
    """Multi-channel notifications for customers."""
    __tablename__ = "notifications"
    
    notification_id = Column(String(50), primary_key=True)
    customer_id = Column(String(50), ForeignKey("customers.customer_id"), nullable=False)
    order_id = Column(String(50), ForeignKey("orders.order_id"))
    type = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    channel = Column(String(20), nullable=False)
    is_read = Column(Text, default="false")
    dispatch_status = Column(String(20), default="pending")
    created_at = Column(Text, nullable=False)
    
    __table_args__ = (
        Index("idx_notifications_customer", "customer_id"),
        Index("idx_notifications_order", "order_id"),
        Index("idx_notifications_type", "type"),
        Index("idx_notifications_channel", "channel"),
        Index("idx_notifications_dispatch_status", "dispatch_status"),
    )
