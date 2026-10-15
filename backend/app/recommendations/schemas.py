"""Recommendation schemas."""
from typing import Literal

from pydantic import BaseModel, Field

# Allowed reason tags as per REQ-DOMAIN-001
ReasonTag = Literal[
    "frequently_bought",
    "seasonal",
    "reorder_reminder",
    "based_on_diet",
    "trending"
]


class RecommendationResponse(BaseModel):
    """Recommendation response schema."""
    recommendation_id: str = Field(..., description="Recommendation ID with rec- prefix")
    customer_id: str = Field(..., description="Customer ID")
    product_id: str = Field(..., description="Product ID")
    score: float = Field(..., description="Recommendation score")
    reason_tag: ReasonTag = Field(..., description="Reason tag for recommendation")
    reason_text: str = Field(..., description="Human-readable reason text")
    generated_at: str = Field(..., description="ISO 8601 generation timestamp")
    
    class Config:
        from_attributes = True


class ProductRecommendationCard(BaseModel):
    """Product card with recommendation context."""
    product_id: str
    name: str
    unit_price: float
    unit_type: str
    is_organic: bool
    image_url: str | None
    average_rating: float | None
    reason_tag: ReasonTag
    reason_text: str
    score: float
