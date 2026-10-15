"""Bootstrap response schemas."""

from pydantic import BaseModel

from app.operations.schemas import OpsSummaryResponse


class ProfileSummary(BaseModel):
    """Customer profile summary for bootstrap."""
    customer_id: str
    name: str
    preferred_language: str
    dietary_preference: str | None = None
    allergies: list[str]
    loyalty_points: int


class AddressServiceability(BaseModel):
    """Address serviceability status."""
    is_serviceable: bool
    service_zone: str | None = None
    reason: str


class AddressSummary(BaseModel):
    """Address summary for bootstrap."""
    address_id: str
    label: str
    postal_code: str
    serviceability: AddressServiceability


class CategorySummary(BaseModel):
    """Category summary for bootstrap."""
    category_id: str
    name: str
    icon_url: str | None = None


class RecommendationCard(BaseModel):
    """Recommendation card for bootstrap."""
    recommendation_id: str
    product_id: str
    score: float
    reason_tag: str
    reason_text: str


class ShoppingListSummary(BaseModel):
    """Shopping list summary for bootstrap."""
    list_id: str
    name: str
    is_ai_generated: bool
    suggestion_note: str | None = None
    item_count: int


class BootstrapResponse(BaseModel):
    """Bootstrap data for authenticated user."""
    profile: ProfileSummary
    default_address: AddressSummary | None = None
    featured_categories: list[CategorySummary]
    recommendations: list[RecommendationCard]
    shopping_lists: list[ShoppingListSummary]
    ops_summary: OpsSummaryResponse | None = None
