"""Fulfillment schemas."""
from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel


class DeliverySlotResponse(BaseModel):
    """Delivery slot response."""
    slot_id: str
    slot_date: str
    start_time: str
    end_time: str
    label: str
    max_capacity: int
    reserved_count: int
    is_available: bool
    service_zone: str | None = None


class DeliveryAgentResponse(BaseModel):
    """Delivery agent response."""
    agent_id: str
    full_name: str
    phone_number: str
    vehicle_details: str | None = None
    availability_status: str


class OrderItemResponse(BaseModel):
    """Order item response."""
    product_id: str
    product_name: str
    quantity: int
    unit_price: Decimal
    total_price: Decimal


class OrderDetailResponse(BaseModel):
    """Order detail response."""
    order_id: str
    status: str
    payment_status: str | None = None
    subtotal: Decimal
    discount_amount: Decimal
    loyalty_redeemed_amount: Decimal
    final_amount: Decimal
    currency: str = "INR"
    tracking_url: str | None = None
    order_date: str
    confirmed_at: str | None = None
    slot: DeliverySlotResponse | None = None
    delivery_agent: DeliveryAgentResponse | None = None
    items: list[OrderItemResponse] = []
