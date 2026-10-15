"""Farmer model."""
from sqlalchemy import Column, Index, Numeric, String, Text

from app.database import Base


class Farmer(Base):
    """Farmer profiles for product sourcing context."""
    __tablename__ = "farmers"
    
    farmer_id = Column(String(50), primary_key=True)
    name = Column(String(200), nullable=False)
    location = Column(String(200))
    bio = Column(Text)
    certification_type = Column(String(100))
    rating = Column(Numeric(3, 2))
    phone_number = Column(String(20))
    created_at = Column(Text, nullable=False)
    updated_at = Column(Text, nullable=False)
    
    __table_args__ = (
        Index("idx_farmers_location", "location"),
    )
