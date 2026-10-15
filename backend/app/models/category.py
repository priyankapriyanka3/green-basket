"""Category model."""
from sqlalchemy import Column, Index, Integer, String, Text

from app.database import Base


class Category(Base):
    """Product categories with hierarchy support."""
    __tablename__ = "categories"
    
    category_id = Column(String(50), primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    parent_category_id = Column(String(50))
    display_order = Column(Integer, default=0)
    icon_url = Column(String(500))
    is_active = Column(Text, default="true")
    created_at = Column(Text, nullable=False)
    updated_at = Column(Text, nullable=False)
    
    # Property to treat is_active as is_featured for API compatibility
    @property
    def is_featured(self):
        return self.is_active == "true"
    
    @is_featured.setter
    def is_featured(self, value: bool):
        self.is_active = "true" if value else "false"
    
    __table_args__ = (
        Index("idx_categories_parent", "parent_category_id"),
        Index("idx_categories_active", "is_active"),
    )
