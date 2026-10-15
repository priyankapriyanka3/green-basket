"""Fulfillment services."""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.errors import AppException
from app.fulfillment.schemas import (
    DeliveryAgentResponse,
    DeliverySlotResponse,
    OrderDetailResponse,
    OrderItemResponse,
)
from app.models.delivery_agent import DeliveryAgent
from app.models.delivery_slot import DeliverySlot
from app.models.order import Order, OrderItem
from app.models.payment import Payment
from app.models.product import Product


def get_order_detail(db: Session, order_id: str, customer_id: str) -> OrderDetailResponse:
    """Get order detail with slot, agent, and items."""
    order = db.query(Order).filter(
        Order.order_id == order_id,
        Order.customer_id == customer_id
    ).first()
    
    if not order:
        raise AppException(
            code="ORDER_NOT_FOUND",
            message="Order not found",
            status_code=404
        )
    
    # Get payment status
    payment = db.query(Payment).filter(Payment.order_id == order_id).first()
    payment_status = payment.status if payment else None
    
    # Get slot details
    slot_response = None
    if order.slot_id:
        slot = db.query(DeliverySlot).filter(DeliverySlot.slot_id == order.slot_id).first()
        if slot:
            slot_response = DeliverySlotResponse(
                slot_id=slot.slot_id,
                slot_date=slot.slot_date,
                start_time=slot.start_time,
                end_time=slot.end_time,
                label=slot.label or f"{slot.start_time} - {slot.end_time}",
                max_capacity=slot.max_capacity,
                reserved_count=slot.reserved_count,
                is_available=(slot.is_available == "true"),
                service_zone=slot.service_zone
            )
    
    # Get agent details
    agent_response = None
    if order.agent_id:
        agent = db.query(DeliveryAgent).filter(DeliveryAgent.agent_id == order.agent_id).first()
        if agent:
            agent_response = DeliveryAgentResponse(
                agent_id=agent.agent_id,
                full_name=agent.full_name,
                phone_number=agent.phone_number,
                vehicle_details=agent.vehicle_details,
                availability_status=agent.availability_status
            )
    
    # Get order items
    order_items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    items_response = []
    
    for item in order_items:
        product = db.query(Product).filter(Product.product_id == item.product_id).first()
        product_name = product.name if product else "Unknown"
        
        items_response.append(OrderItemResponse(
            product_id=item.product_id,
            product_name=product_name,
            quantity=item.quantity,
            unit_price=item.unit_price,
            total_price=item.total_price
        ))
    
    return OrderDetailResponse(
        order_id=order.order_id,
        status=order.status,
        payment_status=payment_status,
        subtotal=order.subtotal,
        discount_amount=order.discount_amount,
        loyalty_redeemed_amount=order.loyalty_redeemed_amount,
        final_amount=order.final_amount,
        tracking_url=order.tracking_url,
        order_date=order.order_date,
        confirmed_at=order.confirmed_at,
        slot=slot_response,
        delivery_agent=agent_response,
        items=items_response
    )
