"""Review model."""
from sqlalchemy import Column, ForeignKey, Index, Integer, String, Text

from app.database import Base


class Review(Base):
    """Product reviews with sentiment analysis."""
    __tablename__ = "reviews"
    
    review_id = Column(String(50), primary_key=True)
    order_id = Column(String(50), ForeignKey("orders.order_id"), nullable=False)
    product_id = Column(String(50), ForeignKey("products.product_id"), nullable=False)
    customer_id = Column(String(50), ForeignKey("customers.customer_id"), nullable=False)
    rating = Column(Integer, nullable=False)
    review_text = Column(Text)
    sentiment = Column(String(20))
    reviewed_at = Column(Text, nullable=False)
    
    __table_args__ = (
        Index("idx_reviews_product", "product_id"),
        Index("idx_reviews_customer", "customer_id"),
        Index("idx_reviews_order", "order_id"),
        Index("idx_reviews_sentiment", "sentiment"),
    )
