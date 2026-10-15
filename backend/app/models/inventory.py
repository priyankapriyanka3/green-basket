"""Inventory model."""
from sqlalchemy import Column, ForeignKey, Index, Integer, String, Text

from app.database import Base


class Inventory(Base):
    """Product inventory with freshness tracking."""
    __tablename__ = "inventory"
    
    inventory_id = Column(String(50), primary_key=True)
    product_id = Column(String(50), ForeignKey("products.product_id"), nullable=False)
    stock_quantity = Column(Integer, nullable=False, default=0)
    reorder_level = Column(Integer, default=10)
    harvest_date = Column(Text)
    expiry_date = Column(Text)
    warehouse_zone = Column(String(100))
    availability_status = Column(String(50), default="available")
    last_updated_at = Column(Text, nullable=False)
    
    __table_args__ = (
        Index("idx_inventory_product", "product_id"),
        Index("idx_inventory_availability", "availability_status"),
        Index("idx_inventory_expiry", "expiry_date"),
    )
