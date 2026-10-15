"""Review request and response schemas."""

from pydantic import BaseModel, Field


class ReviewSubmitRequest(BaseModel):
    """Review submission request."""
    product_id: str = Field(..., description="Product identifier")
    rating: int = Field(..., ge=1, le=5, description="Rating (1-5)")
    review_text: str | None = Field(None, description="Review text")


class ReviewResponse(BaseModel):
    """Review response."""
    review_id: str
    order_id: str
    product_id: str
    customer_id: str
    rating: int
    review_text: str | None = None
    sentiment: str
    reviewed_at: str
