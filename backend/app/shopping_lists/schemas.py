"""Shopping list schemas."""
from typing import Literal

from pydantic import BaseModel, Field, field_validator

# Generation modes as per REQ-DOMAIN-002
GenerationMode = Literal["weekly_reorder", "diet_boost", "seasonal_refresh"]


class ShoppingListItemResponse(BaseModel):
    """Shopping list item response."""
    item_id: str
    product_id: str
    product_name: str
    quantity: int
    source_reason_tag: str | None
    unit_price: float
    unit_type: str
    
    class Config:
        from_attributes = True


class ShoppingListResponse(BaseModel):
    """Shopping list response."""
    list_id: str
    customer_id: str
    name: str
    is_ai_generated: bool
    suggestion_note: str | None
    created_at: str
    items: list[ShoppingListItemResponse] = []
    
    class Config:
        from_attributes = True


class GenerateShoppingListRequest(BaseModel):
    """Request to generate an AI shopping list."""
    mode: GenerationMode = Field(..., description="Generation mode")
    source_order_window_days: int = Field(
        default=42,
        ge=7,
        le=90,
        description="Order history window in days (7-90)"
    )
    target_list_name: str = Field(..., description="Name for the generated list")
    
    @field_validator("source_order_window_days")
    @classmethod
    def validate_window(cls, v: int) -> int:
        """Validate source order window is within 7-90 days."""
        if not (7 <= v <= 90):
            raise ValueError("source_order_window_days must be between 7 and 90")
        return v


class GenerateShoppingListResponse(BaseModel):
    """Response for generated shopping list."""
    list: ShoppingListResponse
    suggestion_note: str
    items_added: int
