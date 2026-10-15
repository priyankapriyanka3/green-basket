"""Cart and checkout schemas."""
from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, Field


class CartItemInput(BaseModel):
    """Cart item input."""
    product_id: str
    quantity: int = Field(gt=0)


class DiscountWarning(BaseModel):
    """Discount warning message."""
    code: str
    reason: str


class CartPricingRequest(BaseModel):
    """Cart pricing request."""
    items: list[CartItemInput]
    discount_code: str | None = None
    loyalty_points_to_redeem: int | None = None


class CartPricingResponse(BaseModel):
    """Cart pricing response."""
    subtotal: Decimal
    discount_amount: Decimal
    loyalty_redeemed_amount: Decimal
    final_amount: Decimal
    currency: str = "INR"
    warnings: list[DiscountWarning] = Field(default_factory=list)


class CheckoutRequest(BaseModel):
    """Checkout submission request."""
    cart_items: list[CartItemInput]
    address_id: str
    slot_id: str
    discount_code: str | None = None
    loyalty_points_to_redeem: int | None = None
    payment_method: str
    client_amount: Decimal


class CheckoutResponse(BaseModel):
    """Checkout response."""
    order_id: str
    payment_id: str
    payment_status: str
    amount: Decimal
    currency: str = "INR"
