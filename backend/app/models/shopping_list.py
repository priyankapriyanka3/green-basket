"""Shopping list models."""
from sqlalchemy import Column, ForeignKey, Index, Integer, String, Text

from app.database import Base


class ShoppingList(Base):
    """Customer shopping lists with AI generation support."""
    __tablename__ = "shopping_lists"
    
    list_id = Column(String(50), primary_key=True)
    customer_id = Column(String(50), ForeignKey("customers.customer_id"), nullable=False)
    name = Column(String(200), nullable=False)
    is_ai_generated = Column(Text, default="false")
    suggestion_note = Column(Text)
    created_at = Column(Text, nullable=False)
    updated_at = Column(Text, nullable=False)
    
    __table_args__ = (
        Index("idx_shopping_lists_customer", "customer_id"),
        Index("idx_shopping_lists_ai_generated", "is_ai_generated"),
    )


class ShoppingListItem(Base):
    """Items within shopping lists."""
    __tablename__ = "shopping_list_items"
    
    item_id = Column(String(50), primary_key=True)
    list_id = Column(String(50), ForeignKey("shopping_lists.list_id"), nullable=False)
    product_id = Column(String(50), ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Integer, default=1)
    source_reason_tag = Column(String(50))
    added_at = Column(Text, nullable=False)
    
    __table_args__ = (
        Index("idx_shopping_list_items_list", "list_id"),
        Index("idx_shopping_list_items_product", "product_id"),
    )
