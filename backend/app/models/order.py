"""Order models."""
from sqlalchemy import Column, ForeignKey, Index, Integer, Numeric, String, Text

from app.database import Base


class Order(Base):
    """Customer orders with lifecycle tracking."""
    __tablename__ = "orders"
    
    order_id = Column(String(50), primary_key=True)
    customer_id = Column(String(50), ForeignKey("customers.customer_id"), nullable=False)
    address_id = Column(String(50), ForeignKey("addresses.address_id"), nullable=False)
    slot_id = Column(String(50), ForeignKey("delivery_slots.slot_id"))
    agent_id = Column(String(50), ForeignKey("delivery_agents.agent_id"))
    status = Column(String(50), default="payment_pending")
    subtotal = Column(Numeric(10, 2), nullable=False)
    discount_amount = Column(Numeric(10, 2), default=0.0)
    loyalty_redeemed_amount = Column(Numeric(10, 2), default=0.0)
    final_amount = Column(Numeric(10, 2), nullable=False)
    tracking_url = Column(String(500))
    order_date = Column(Text, nullable=False)
    confirmed_at = Column(Text)
    
    __table_args__ = (
        Index("idx_orders_customer", "customer_id"),
        Index("idx_orders_status", "status"),
        Index("idx_orders_slot", "slot_id"),
        Index("idx_orders_date", "order_date"),
    )


class OrderItem(Base):
    """Line items within orders."""
    __tablename__ = "order_items"
    
    item_id = Column(String(50), primary_key=True)
    order_id = Column(String(50), ForeignKey("orders.order_id"), nullable=False)
    product_id = Column(String(50), ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    
    __table_args__ = (
        Index("idx_order_items_order", "order_id"),
        Index("idx_order_items_product", "product_id"),
    )


class OrderDiscount(Base):
    """Discounts applied to orders."""
    __tablename__ = "order_discounts"
    
    order_discount_id = Column(String(50), primary_key=True)
    order_id = Column(String(50), ForeignKey("orders.order_id"), nullable=False)
    promotion_id = Column(String(50), ForeignKey("promotions.promotion_id"), nullable=False)
    discount_amount = Column(Numeric(10, 2), nullable=False)
    applied_at = Column(Text, nullable=False)
    
    __table_args__ = (
        Index("idx_order_discounts_order", "order_id"),
        Index("idx_order_discounts_promotion", "promotion_id"),
    )
