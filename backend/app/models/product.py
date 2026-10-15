"""Product model."""
from sqlalchemy import Column, ForeignKey, Index, Integer, Numeric, String, Text

from app.database import Base


class Product(Base):
    """Products with pricing, nutrition, and trust signals."""
    __tablename__ = "products"
    
    product_id = Column(String(50), primary_key=True)
    category_id = Column(String(50), ForeignKey("categories.category_id"), nullable=False)
    farmer_id = Column(String(50), ForeignKey("farmers.farmer_id"))
    name = Column(String(200), nullable=False)
    description = Column(Text)
    unit_price = Column(Numeric(10, 2), nullable=False)
    unit_type = Column(String(50), default="kg")
    is_organic = Column(Text, default="false")
    is_featured = Column(Text, default="false")
    nutrition_json = Column(Text)
    tags_json = Column(Text)
    image_url = Column(String(500))
    average_rating = Column(Numeric(3, 2))
    review_count = Column(Integer, default=0)
    created_at = Column(Text, nullable=False)
    updated_at = Column(Text, nullable=False)
    
    __table_args__ = (
        Index("idx_products_category", "category_id"),
        Index("idx_products_farmer", "farmer_id"),
        Index("idx_products_organic", "is_organic"),
        Index("idx_products_featured", "is_featured"),
    )
