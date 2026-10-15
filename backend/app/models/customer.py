"""Customer model."""
from sqlalchemy import Column, Index, Numeric, String, Text

from app.database import Base


class Customer(Base):
    """Customer profile with dietary preferences and loyalty."""
    __tablename__ = "customers"
    
    customer_id = Column(String(50), primary_key=True)
    full_name = Column(String(200), nullable=False)
    phone_number = Column(String(20), nullable=False, unique=True)
    email = Column(String(200))
    preferred_language = Column(String(10), default="en")
    dietary_preference = Column(String(50))
    allergies_json = Column(Text)
    loyalty_points = Column(Numeric(10, 2), default=0.0)
    status = Column(String(20), default="active")
    created_at = Column(Text, nullable=False)
    updated_at = Column(Text, nullable=False)
    
    __table_args__ = (
        Index("idx_customers_phone", "phone_number"),
        Index("idx_customers_email", "email"),
        Index("idx_customers_status", "status"),
    )
