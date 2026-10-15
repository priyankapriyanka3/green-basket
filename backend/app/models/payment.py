"""Payment model."""
from sqlalchemy import Column, ForeignKey, Index, Numeric, String, Text

from app.database import Base


class Payment(Base):
    """Payment records linked to orders."""
    __tablename__ = "payments"
    
    payment_id = Column(String(50), primary_key=True)
    order_id = Column(String(50), ForeignKey("orders.order_id"), nullable=False)
    payment_method = Column(String(50), nullable=False)
    status = Column(String(50), default="initiated")
    amount = Column(Numeric(10, 2), nullable=False)
    transaction_reference = Column(String(200))
    payment_date = Column(Text, nullable=False)
    
    __table_args__ = (
        Index("idx_payments_order", "order_id"),
        Index("idx_payments_status", "status"),
        Index("idx_payments_transaction", "transaction_reference"),
    )
