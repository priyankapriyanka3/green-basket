"""Cart and checkout services."""
from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.cart_checkout.schemas import (
    CartItemInput,
    CartPricingResponse,
    DiscountWarning,
)
from app.errors import AppException
from app.models.address import Address
from app.models.customer import Customer
from app.models.delivery_slot import DeliverySlot
from app.models.order import Order, OrderDiscount, OrderItem
from app.models.payment import Payment
from app.models.product import Product
from app.models.promotion import Promotion


def price_cart(
    db: Session,
    items: list[CartItemInput],
    discount_code: str | None,
    loyalty_points_to_redeem: int | None,
    customer_id: str
) -> CartPricingResponse:
    """Price cart with discount and loyalty redemption."""
    # Calculate subtotal
    subtotal = Decimal("0.00")
    for item in items:
        product = db.query(Product).filter(Product.product_id == item.product_id).first()
        if not product:
            raise AppException(
                code="PRODUCT_NOT_FOUND",
                message=f"Product {item.product_id} not found",
                status_code=404
            )
        subtotal += Decimal(str(product.unit_price)) * item.quantity
    
    # Apply discount
    discount_amount = Decimal("0.00")
    warnings = []
    
    if discount_code:
        discount = db.query(Promotion).filter(Promotion.code == discount_code).first()
        if not discount:
            warnings.append(DiscountWarning(
                code=discount_code,
                reason="DISCOUNT_CODE_NOT_FOUND"
            ))
        elif discount.is_active != "true":
            warnings.append(DiscountWarning(
                code=discount_code,
                reason="DISCOUNT_NOT_ACTIVE"
            ))
        elif discount.usage_limit and discount.usage_count >= discount.usage_limit:
            warnings.append(DiscountWarning(
                code=discount_code,
                reason="DISCOUNT_USAGE_LIMIT_EXCEEDED"
            ))
        else:
            # Check validity dates
            now = datetime.now(UTC).isoformat()
            if now < discount.valid_from:
                warnings.append(DiscountWarning(
                    code=discount_code,
                    reason="DISCOUNT_NOT_YET_VALID"
                ))
            elif now > discount.valid_to:
                warnings.append(DiscountWarning(
                    code=discount_code,
                    reason="DISCOUNT_EXPIRED"
                ))
            elif subtotal < Decimal(str(discount.minimum_order_threshold)):
                warnings.append(DiscountWarning(
                    code=discount_code,
                    reason=f"MINIMUM_ORDER_THRESHOLD_NOT_MET:{discount.minimum_order_threshold}"
                ))
            else:
                # Apply discount
                if discount.discount_type == "flat":
                    discount_amount = Decimal(str(discount.discount_value))
                elif discount.discount_type == "percentage":
                    discount_amount = subtotal * (Decimal(str(discount.discount_value)) / Decimal(100))
                discount_amount = min(discount_amount, subtotal)
    
    # Apply loyalty redemption (₹5 per 100 points)
    loyalty_redeemed_amount = Decimal("0.00")
    if loyalty_points_to_redeem:
        customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
        if not customer:
            raise AppException(
                code="CUSTOMER_NOT_FOUND",
                message="Customer not found",
                status_code=404
            )
        
        if loyalty_points_to_redeem > customer.loyalty_points:
            raise AppException(
                code="INSUFFICIENT_LOYALTY_POINTS",
                message=f"Insufficient loyalty points. Available: {customer.loyalty_points}",
                status_code=409
            )
        
        # ₹5 per 100 points
        loyalty_redeemed_amount = Decimal(str(loyalty_points_to_redeem)) * Decimal(5) / Decimal(100)
        amount_after_discount = subtotal - discount_amount
        loyalty_redeemed_amount = min(loyalty_redeemed_amount, amount_after_discount)
    
    final_amount = subtotal - discount_amount - loyalty_redeemed_amount
    final_amount = max(final_amount, Decimal("0.00"))
    
    return CartPricingResponse(
        subtotal=subtotal,
        discount_amount=discount_amount,
        loyalty_redeemed_amount=loyalty_redeemed_amount,
        final_amount=final_amount,
        warnings=warnings
    )


def validate_and_submit_checkout(
    db: Session,
    cart_items: list[CartItemInput],
    address_id: str,
    slot_id: str,
    discount_code: str | None,
    loyalty_points_to_redeem: int | None,
    payment_method: str,
    client_amount: Decimal,
    customer_id: str
) -> tuple[Order, Payment]:
    """Validate checkout and create order with payment."""
    # Validate cart completeness
    if not cart_items:
        raise AppException(
            code="CART_EMPTY",
            message="Cart cannot be empty",
            status_code=422
        )
    
    # Validate address serviceability
    address = db.query(Address).filter(
        Address.address_id == address_id,
        Address.customer_id == customer_id
    ).first()
    
    if not address:
        raise AppException(
            code="ADDRESS_NOT_FOUND",
            message="Address not found or does not belong to customer",
            status_code=404
        )
    
    if address.serviceability_status != "serviceable":
        raise AppException(
            code="ADDRESS_NOT_SERVICEABLE",
            message=f"Address is not serviceable: {address.serviceability_reason}",
            status_code=409
        )
    
    # Validate slot availability and capacity
    slot = db.query(DeliverySlot).filter(DeliverySlot.slot_id == slot_id).first()
    if not slot:
        raise AppException(
            code="SLOT_NOT_FOUND",
            message="Delivery slot not found",
            status_code=404
        )
    
    if slot.reserved_count >= slot.max_capacity:
        raise AppException(
            code="SLOT_CAPACITY_EXCEEDED",
            message=f"Delivery slot is full. Capacity: {slot.max_capacity}",
            status_code=409
        )
    
    # Recalculate pricing server-side
    pricing = price_cart(db, cart_items, discount_code, loyalty_points_to_redeem, customer_id)
    
    # Validate amount match
    if abs(pricing.final_amount - client_amount) > Decimal("0.01"):
        raise AppException(
            code="AMOUNT_MISMATCH",
            message=f"Client amount {client_amount} does not match server amount {pricing.final_amount}",
            status_code=409
        )
    
    # Reserve slot capacity
    slot.reserved_count += 1
    slot.updated_at = datetime.now(UTC).isoformat()
    
    # Generate IDs
    now_iso = datetime.now(UTC).isoformat()
    order_id = f"ord-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}"
    payment_id = f"pay-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}"
    
    # Create order
    order = Order(
        order_id=order_id,
        customer_id=customer_id,
        address_id=address_id,
        slot_id=slot_id,
        status="payment_pending",
        subtotal=float(pricing.subtotal),
        discount_amount=float(pricing.discount_amount),
        loyalty_redeemed_amount=float(pricing.loyalty_redeemed_amount),
        final_amount=float(pricing.final_amount),
        order_date=now_iso
    )
    db.add(order)
    
    # Create order items
    for item in cart_items:
        product = db.query(Product).filter(Product.product_id == item.product_id).first()
        if not product:
            raise AppException(
                code="PRODUCT_NOT_FOUND",
                message=f"Product {item.product_id} not found",
                status_code=404
            )
        
        item_id = f"itm-{datetime.now(UTC).strftime('%Y%m%d%H%M%S%f')}"
        order_item = OrderItem(
            item_id=item_id,
            order_id=order_id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=float(product.unit_price),
            total_price=float(Decimal(str(product.unit_price)) * item.quantity)
        )
        db.add(order_item)
    
    # Create order discount if applicable
    if discount_code and pricing.discount_amount > 0:
        discount = db.query(Promotion).filter(Promotion.code == discount_code).first()
        if discount:
            order_discount_id = f"odc-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}"
            order_discount = OrderDiscount(
                order_discount_id=order_discount_id,
                order_id=order_id,
                promotion_id=discount.promotion_id,
                discount_amount=float(pricing.discount_amount),
                applied_at=now_iso
            )
            db.add(order_discount)
            
            # Increment usage count
            discount.usage_count += 1
            discount.updated_at = now_iso
    
    # Deduct loyalty points if redeemed
    if loyalty_points_to_redeem and pricing.loyalty_redeemed_amount > 0:
        customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
        if customer:
            customer.loyalty_points -= loyalty_points_to_redeem
            customer.updated_at = now_iso
    
    # Create payment record
    payment = Payment(
        payment_id=payment_id,
        order_id=order_id,
        payment_method=payment_method,
        status="initiated",
        amount=float(pricing.final_amount),
        transaction_reference=f"txn-{payment_id}",
        payment_date=now_iso
    )
    db.add(payment)
    
    db.commit()
    db.refresh(order)
    db.refresh(payment)
    
    return order, payment
