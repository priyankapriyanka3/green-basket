"""Promotion model."""
from sqlalchemy import Column, Index, Integer, Numeric, String, Text

from app.database import Base


class Promotion(Base):
    """Discount promotions with eligibility rules."""
    __tablename__ = "promotions"
    
    promotion_id = Column(String(50), primary_key=True)
    code = Column(String(50), nullable=False, unique=True)
    description = Column(Text)
    discount_type = Column(String(20), nullable=False)
    discount_value = Column(Numeric(10, 2), nullable=False)
    minimum_order_threshold = Column(Numeric(10, 2))
    usage_limit = Column(Integer)
    usage_count = Column(Integer, default=0)
    valid_from = Column(Text, nullable=False)
    valid_to = Column(Text, nullable=False)
    is_active = Column(Text, default="true")
    applicability_json = Column(Text)
    created_at = Column(Text, nullable=False)
    updated_at = Column(Text, nullable=False)
    
    __table_args__ = (
        Index("idx_promotions_code", "code"),
        Index("idx_promotions_active", "is_active"),
        Index("idx_promotions_valid_dates", "valid_from", "valid_to"),
    )
