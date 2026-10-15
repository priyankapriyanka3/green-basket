"""Address model."""
from sqlalchemy import Column, ForeignKey, Index, Numeric, String, Text

from app.database import Base


class Address(Base):
    """Customer saved addresses with serviceability status."""
    __tablename__ = "addresses"
    
    address_id = Column(String(50), primary_key=True)
    customer_id = Column(String(50), ForeignKey("customers.customer_id"), nullable=False)
    address_line1 = Column(String(200), nullable=False)
    address_line2 = Column(String(200))
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), default="India")
    latitude = Column(Numeric(10, 7))
    longitude = Column(Numeric(10, 7))
    service_zone = Column(String(100))
    serviceability_status = Column(String(50))
    serviceability_reason = Column(Text)
    is_default = Column(Text, default="false")
    created_at = Column(Text, nullable=False)
    updated_at = Column(Text, nullable=False)
    
    __table_args__ = (
        Index("idx_addresses_customer", "customer_id"),
        Index("idx_addresses_postal", "postal_code"),
        Index("idx_addresses_serviceability", "serviceability_status"),
    )
