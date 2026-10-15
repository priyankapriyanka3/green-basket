"""Payment request and response schemas."""

from pydantic import BaseModel, Field


class PaymentInitRequest(BaseModel):
    """Payment initiation request."""
    order_id: str = Field(..., description="Order identifier")
    payment_method: str = Field(..., description="Payment method (upi, card, netbanking)")
    amount: str = Field(..., description="Payment amount in INR")
    currency: str = Field(default="INR", description="Currency code")
    callback_url: str | None = Field(None, description="Payment callback URL")


class PaymentInitResponse(BaseModel):
    """Payment initiation response."""
    payment_id: str
    order_id: str
    status: str
    transaction_reference: str
    client_token: str
    redirect_url: str | None = None


class PaymentStatusResponse(BaseModel):
    """Payment status response."""
    payment_id: str
    order_id: str
    status: str
    transaction_reference: str
    amount: str
    currency: str
    payment_date: str | None = None
    updated_at: str
