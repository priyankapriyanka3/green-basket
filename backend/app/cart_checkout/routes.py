"""Cart and checkout routes."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.cart_checkout.schemas import (
    CartPricingRequest,
    CartPricingResponse,
    CheckoutRequest,
    CheckoutResponse,
)
from app.cart_checkout.services import price_cart, validate_and_submit_checkout
from app.database import get_db

router = APIRouter()


@router.post("/api/v1/cart/price", response_model=CartPricingResponse)
def price_cart_endpoint(
    request: CartPricingRequest,
    db: Session = Depends(get_db),
    current_user: tuple = Depends(get_current_user)
):
    """Price cart with discount and loyalty redemption."""
    customer, _role = current_user
    
    return price_cart(
        db=db,
        items=request.items,
        discount_code=request.discount_code,
        loyalty_points_to_redeem=request.loyalty_points_to_redeem,
        customer_id=customer.customer_id
    )


@router.post("/api/v1/checkout/submit", response_model=CheckoutResponse)
def submit_checkout(
    request: CheckoutRequest,
    db: Session = Depends(get_db),
    current_user: tuple = Depends(get_current_user)
):
    """Submit checkout and create order with payment."""
    customer, _role = current_user
    
    order, payment = validate_and_submit_checkout(
        db=db,
        cart_items=request.cart_items,
        address_id=request.address_id,
        slot_id=request.slot_id,
        discount_code=request.discount_code,
        loyalty_points_to_redeem=request.loyalty_points_to_redeem,
        payment_method=request.payment_method,
        client_amount=request.client_amount,
        customer_id=customer.customer_id
    )
    
    return CheckoutResponse(
        order_id=order.order_id,
        payment_id=payment.payment_id,
        payment_status=payment.status,
        amount=order.final_amount,
        currency="INR"
    )
