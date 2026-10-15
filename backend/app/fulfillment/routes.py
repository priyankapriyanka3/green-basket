"""Fulfillment routes."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.fulfillment.schemas import OrderDetailResponse
from app.fulfillment.services import get_order_detail

router = APIRouter()


@router.get("/api/v1/orders/{order_id}", response_model=OrderDetailResponse)
def get_order(
    order_id: str,
    db: Session = Depends(get_db),
    current_user: tuple = Depends(get_current_user)
):
    """Get order detail with slot, agent, and items."""
    customer, _role = current_user
    
    return get_order_detail(db=db, order_id=order_id, customer_id=customer.customer_id)
