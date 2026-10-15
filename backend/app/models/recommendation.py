"""Recommendation model."""
from sqlalchemy import Column, ForeignKey, Index, Numeric, String, Text

from app.database import Base


class Recommendation(Base):
    """AI product recommendations with reason tags."""
    __tablename__ = "recommendations"
    
    recommendation_id = Column(String(50), primary_key=True)
    customer_id = Column(String(50), ForeignKey("customers.customer_id"), nullable=False)
    product_id = Column(String(50), ForeignKey("products.product_id"), nullable=False)
    score = Column(Numeric(5, 4), nullable=False)
    reason_tag = Column(String(50), nullable=False)
    reason_text = Column(Text)
    generated_at = Column(Text, nullable=False)
    
    __table_args__ = (
        Index("idx_recommendations_customer", "customer_id"),
        Index("idx_recommendations_product", "product_id"),
        Index("idx_recommendations_reason_tag", "reason_tag"),
    )
