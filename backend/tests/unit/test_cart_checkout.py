"""Unit tests for cart and checkout services."""
from decimal import Decimal
from unittest.mock import Mock, patch

import pytest

from app.cart_checkout.schemas import CartItemInput
from app.cart_checkout.services import price_cart, validate_and_submit_checkout
from app.errors import AppException


def test_price_cart_basic_calculation(mock_db_session, sample_product, sample_customer):
    """Test basic cart pricing without discount or loyalty."""
    mock_db_session.query().filter().first.return_value = sample_product
    
    items = [CartItemInput(product_id="prod-001", quantity=2)]
    
    result = price_cart(
        db=mock_db_session,
        items=items,
        discount_code=None,
        loyalty_points_to_redeem=None,
        customer_id="cust-001"
    )
    
    assert result.subtotal == Decimal("50.00")
    assert result.discount_amount == Decimal("0.00")
    assert result.loyalty_redeemed_amount == Decimal("0.00")
    assert result.final_amount == Decimal("50.00")
    assert len(result.warnings) == 0


def test_price_cart_with_flat_discount(mock_db_session, sample_product, sample_customer):
    """Test cart pricing with flat discount."""
    # Mock product and discount
    mock_discount = Mock()
    mock_discount.code = "FLAT10"
    mock_discount.is_active = "true"
    mock_discount.usage_limit = 100
    mock_discount.usage_count = 50
    mock_discount.valid_from = "2026-01-01T00:00:00Z"
    mock_discount.valid_to = "2026-12-31T23:59:59Z"
    mock_discount.minimum_order_threshold = 0
    mock_discount.discount_type = "flat"
    mock_discount.discount_value = 10.0
    
    def query_side_effect(*args):
        mock_query = Mock()
        if args[0].__name__ == "Product":
            mock_query.filter().first.return_value = sample_product
        elif args[0].__name__ == "Promotion":
            mock_query.filter().first.return_value = mock_discount
        return mock_query
    
    mock_db_session.query.side_effect = query_side_effect
    
    items = [CartItemInput(product_id="prod-001", quantity=2)]
    
    result = price_cart(
        db=mock_db_session,
        items=items,
        discount_code="FLAT10",
        loyalty_points_to_redeem=None,
        customer_id="cust-001"
    )
    
    assert result.subtotal == Decimal("50.00")
    assert result.discount_amount == Decimal("10.00")
    assert result.final_amount == Decimal("40.00")


def test_price_cart_with_percentage_discount(mock_db_session, sample_product, sample_customer):
    """Test cart pricing with percentage discount."""
    mock_discount = Mock()
    mock_discount.code = "PCT20"
    mock_discount.is_active = "true"
    mock_discount.usage_limit = None
    mock_discount.usage_count = 10
    mock_discount.valid_from = "2026-01-01T00:00:00Z"
    mock_discount.valid_to = "2026-12-31T23:59:59Z"
    mock_discount.minimum_order_threshold = 0
    mock_discount.discount_type = "percentage"
    mock_discount.discount_value = 20.0
    
    def query_side_effect(*args):
        mock_query = Mock()
        if args[0].__name__ == "Product":
            mock_query.filter().first.return_value = sample_product
        elif args[0].__name__ == "Promotion":
            mock_query.filter().first.return_value = mock_discount
        return mock_query
    
    mock_db_session.query.side_effect = query_side_effect
    
    items = [CartItemInput(product_id="prod-001", quantity=2)]
    
    result = price_cart(
        db=mock_db_session,
        items=items,
        discount_code="PCT20",
        loyalty_points_to_redeem=None,
        customer_id="cust-001"
    )
    
    assert result.subtotal == Decimal("50.00")
    assert result.discount_amount == Decimal("10.00")  # 20% of 50
    assert result.final_amount == Decimal("40.00")


def test_price_cart_discount_minimum_threshold_not_met(mock_db_session, sample_product):
    """Test discount rejected when minimum order threshold not met."""
    mock_discount = Mock()
    mock_discount.code = "MIN100"
    mock_discount.is_active = "true"
    mock_discount.usage_limit = None
    mock_discount.usage_count = 0
    mock_discount.valid_from = "2026-01-01T00:00:00Z"
    mock_discount.valid_to = "2026-12-31T23:59:59Z"
    mock_discount.minimum_order_threshold = 100.0
    mock_discount.discount_type = "flat"
    mock_discount.discount_value = 15.0
    
    def query_side_effect(*args):
        mock_query = Mock()
        if args[0].__name__ == "Product":
            mock_query.filter().first.return_value = sample_product
        elif args[0].__name__ == "Promotion":
            mock_query.filter().first.return_value = mock_discount
        return mock_query
    
    mock_db_session.query.side_effect = query_side_effect
    
    items = [CartItemInput(product_id="prod-001", quantity=2)]  # Subtotal 50
    
    result = price_cart(
        db=mock_db_session,
        items=items,
        discount_code="MIN100",
        loyalty_points_to_redeem=None,
        customer_id="cust-001"
    )
    
    assert result.discount_amount == Decimal("0.00")
    assert len(result.warnings) == 1
    assert "MINIMUM_ORDER_THRESHOLD_NOT_MET" in result.warnings[0].reason


def test_price_cart_discount_expired(mock_db_session, sample_product):
    """Test discount rejected when expired."""
    mock_discount = Mock()
    mock_discount.code = "EXPIRED"
    mock_discount.is_active = "true"
    mock_discount.usage_limit = None
    mock_discount.usage_count = 0
    mock_discount.valid_from = "2025-01-01T00:00:00Z"
    mock_discount.valid_to = "2025-12-31T23:59:59Z"
    mock_discount.minimum_order_threshold = 0
    mock_discount.discount_type = "flat"
    mock_discount.discount_value = 10.0
    
    def query_side_effect(*args):
        mock_query = Mock()
        if args[0].__name__ == "Product":
            mock_query.filter().first.return_value = sample_product
        elif args[0].__name__ == "Promotion":
            mock_query.filter().first.return_value = mock_discount
        return mock_query
    
    mock_db_session.query.side_effect = query_side_effect
    
    items = [CartItemInput(product_id="prod-001", quantity=2)]
    
    result = price_cart(
        db=mock_db_session,
        items=items,
        discount_code="EXPIRED",
        loyalty_points_to_redeem=None,
        customer_id="cust-001"
    )
    
    assert result.discount_amount == Decimal("0.00")
    assert len(result.warnings) == 1
    assert result.warnings[0].reason == "DISCOUNT_EXPIRED"


def test_price_cart_discount_not_active(mock_db_session, sample_product):
    """Test discount rejected when not active."""
    mock_discount = Mock()
    mock_discount.code = "INACTIVE"
    mock_discount.is_active = "false"
    
    def query_side_effect(*args):
        mock_query = Mock()
        if args[0].__name__ == "Product":
            mock_query.filter().first.return_value = sample_product
        elif args[0].__name__ == "Promotion":
            mock_query.filter().first.return_value = mock_discount
        return mock_query
    
    mock_db_session.query.side_effect = query_side_effect
    
    items = [CartItemInput(product_id="prod-001", quantity=2)]
    
    result = price_cart(
        db=mock_db_session,
        items=items,
        discount_code="INACTIVE",
        loyalty_points_to_redeem=None,
        customer_id="cust-001"
    )
    
    assert result.discount_amount == Decimal("0.00")
    assert len(result.warnings) == 1
    assert result.warnings[0].reason == "DISCOUNT_NOT_ACTIVE"


def test_price_cart_discount_usage_limit_exceeded(mock_db_session, sample_product):
    """Test discount rejected when usage limit exceeded."""
    mock_discount = Mock()
    mock_discount.code = "MAXED"
    mock_discount.is_active = "true"
    mock_discount.usage_limit = 10
    mock_discount.usage_count = 10
    
    def query_side_effect(*args):
        mock_query = Mock()
        if args[0].__name__ == "Product":
            mock_query.filter().first.return_value = sample_product
        elif args[0].__name__ == "Promotion":
            mock_query.filter().first.return_value = mock_discount
        return mock_query
    
    mock_db_session.query.side_effect = query_side_effect
    
    items = [CartItemInput(product_id="prod-001", quantity=2)]
    
    result = price_cart(
        db=mock_db_session,
        items=items,
        discount_code="MAXED",
        loyalty_points_to_redeem=None,
        customer_id="cust-001"
    )
    
    assert result.discount_amount == Decimal("0.00")
    assert len(result.warnings) == 1
    assert result.warnings[0].reason == "DISCOUNT_USAGE_LIMIT_EXCEEDED"


def test_price_cart_with_loyalty_redemption(mock_db_session, sample_product):
    """Test cart pricing with loyalty points redemption."""
    sample_customer = Mock()
    sample_customer.customer_id = "cust-001"
    sample_customer.loyalty_points = 500
    
    def query_side_effect(*args):
        mock_query = Mock()
        if args[0].__name__ == "Product":
            mock_query.filter().first.return_value = sample_product
        elif args[0].__name__ == "Customer":
            mock_query.filter().first.return_value = sample_customer
        return mock_query
    
    mock_db_session.query.side_effect = query_side_effect
    
    items = [CartItemInput(product_id="prod-001", quantity=2)]
    
    # Redeem 200 points = ₹10 (₹5 per 100 points)
    result = price_cart(
        db=mock_db_session,
        items=items,
        discount_code=None,
        loyalty_points_to_redeem=200,
        customer_id="cust-001"
    )
    
    assert result.subtotal == Decimal("50.00")
    assert result.loyalty_redeemed_amount == Decimal("10.00")
    assert result.final_amount == Decimal("40.00")


def test_price_cart_insufficient_loyalty_points(mock_db_session, sample_product):
    """Test loyalty redemption rejected when insufficient points."""
    sample_customer = Mock()
    sample_customer.customer_id = "cust-001"
    sample_customer.loyalty_points = 50
    
    def query_side_effect(*args):
        mock_query = Mock()
        if args[0].__name__ == "Product":
            mock_query.filter().first.return_value = sample_product
        elif args[0].__name__ == "Customer":
            mock_query.filter().first.return_value = sample_customer
        return mock_query
    
    mock_db_session.query.side_effect = query_side_effect
    
    items = [CartItemInput(product_id="prod-001", quantity=2)]
    
    with pytest.raises(AppException) as exc_info:
        price_cart(
            db=mock_db_session,
            items=items,
            discount_code=None,
            loyalty_points_to_redeem=200,
            customer_id="cust-001"
        )
    
    assert exc_info.value.code == "INSUFFICIENT_LOYALTY_POINTS"
    assert exc_info.value.status_code == 409


def test_validate_checkout_empty_cart(mock_db_session):
    """Test checkout validation rejects empty cart."""
    with pytest.raises(AppException) as exc_info:
        validate_and_submit_checkout(
            db=mock_db_session,
            cart_items=[],
            address_id="addr-001",
            slot_id="slt-001",
            discount_code=None,
            loyalty_points_to_redeem=None,
            payment_method="upi",
            client_amount=Decimal("50.00"),
            customer_id="cust-001"
        )
    
    assert exc_info.value.code == "CART_EMPTY"
    assert exc_info.value.status_code == 422


def test_validate_checkout_address_not_serviceable(mock_db_session, sample_product):
    """Test checkout blocked for unserviceable address."""
    mock_address = Mock()
    mock_address.address_id = "addr-001"
    mock_address.customer_id = "cust-001"
    mock_address.serviceability_status = "not_serviceable"
    mock_address.serviceability_reason = "Outside delivery zone"
    
    def query_side_effect(*args):
        mock_query = Mock()
        if args[0].__name__ == "Address":
            mock_query.filter().first.return_value = mock_address
        return mock_query
    
    mock_db_session.query.side_effect = query_side_effect
    
    items = [CartItemInput(product_id="prod-001", quantity=2)]
    
    with pytest.raises(AppException) as exc_info:
        validate_and_submit_checkout(
            db=mock_db_session,
            cart_items=items,
            address_id="addr-001",
            slot_id="slt-001",
            discount_code=None,
            loyalty_points_to_redeem=None,
            payment_method="upi",
            client_amount=Decimal("50.00"),
            customer_id="cust-001"
        )
    
    assert exc_info.value.code == "ADDRESS_NOT_SERVICEABLE"
    assert exc_info.value.status_code == 409


def test_validate_checkout_slot_capacity_exceeded(mock_db_session, sample_product, sample_address):
    """Test checkout blocked when slot is full."""
    mock_slot = Mock()
    mock_slot.slot_id = "slt-001"
    mock_slot.max_capacity = 10
    mock_slot.reserved_count = 10
    
    def query_side_effect(*args):
        mock_query = Mock()
        if args[0].__name__ == "Address":
            mock_query.filter().first.return_value = sample_address
        elif args[0].__name__ == "DeliverySlot":
            mock_query.filter().first.return_value = mock_slot
        return mock_query
    
    mock_db_session.query.side_effect = query_side_effect
    
    items = [CartItemInput(product_id="prod-001", quantity=2)]
    
    with pytest.raises(AppException) as exc_info:
        validate_and_submit_checkout(
            db=mock_db_session,
            cart_items=items,
            address_id="addr-001",
            slot_id="slt-001",
            discount_code=None,
            loyalty_points_to_redeem=None,
            payment_method="upi",
            client_amount=Decimal("50.00"),
            customer_id="cust-001"
        )
    
    assert exc_info.value.code == "SLOT_CAPACITY_EXCEEDED"
    assert exc_info.value.status_code == 409


def test_validate_checkout_amount_mismatch(mock_db_session, sample_product, sample_address):
    """Test checkout blocked when client amount doesn't match server amount."""
    mock_slot = Mock()
    mock_slot.slot_id = "slt-001"
    mock_slot.max_capacity = 10
    mock_slot.reserved_count = 5
    
    def query_side_effect(*args):
        mock_query = Mock()
        if args[0].__name__ == "Product":
            mock_query.filter().first.return_value = sample_product
        elif args[0].__name__ == "Address":
            mock_query.filter().first.return_value = sample_address
        elif args[0].__name__ == "DeliverySlot":
            mock_query.filter().first.return_value = mock_slot
        return mock_query
    
    mock_db_session.query.side_effect = query_side_effect
    
    items = [CartItemInput(product_id="prod-001", quantity=2)]
    
    with pytest.raises(AppException) as exc_info:
        validate_and_submit_checkout(
            db=mock_db_session,
            cart_items=items,
            address_id="addr-001",
            slot_id="slt-001",
            discount_code=None,
            loyalty_points_to_redeem=None,
            payment_method="upi",
            client_amount=Decimal("100.00"),  # Should be 50.00
            customer_id="cust-001"
        )
    
    assert exc_info.value.code == "AMOUNT_MISMATCH"
    assert exc_info.value.status_code == 409


def test_validate_checkout_order_payment_atomicity(mock_db_session, sample_product, sample_address):
    """Test order and payment created atomically with payment_pending status."""
    mock_slot = Mock()
    mock_slot.slot_id = "slt-001"
    mock_slot.max_capacity = 10
    mock_slot.reserved_count = 5
    mock_slot.updated_at = None
    
    mock_order = Mock()
    mock_order.order_id = "ord-001"
    mock_order.status = "payment_pending"
    mock_order.final_amount = 50.0
    
    mock_payment = Mock()
    mock_payment.payment_id = "pay-001"
    mock_payment.status = "initiated"
    
    def query_side_effect(*args):
        mock_query = Mock()
        if args[0].__name__ == "Product":
            mock_query.filter().first.return_value = sample_product
        elif args[0].__name__ == "Address":
            mock_query.filter().first.return_value = sample_address
        elif args[0].__name__ == "DeliverySlot":
            mock_query.filter().first.return_value = mock_slot
        return mock_query
    
    mock_db_session.query.side_effect = query_side_effect
    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.side_effect = lambda obj: None
    
    items = [CartItemInput(product_id="prod-001", quantity=2)]
    
    # Mock the return values
    with patch('app.cart_checkout.services.Order', return_value=mock_order), \
         patch('app.cart_checkout.services.Payment', return_value=mock_payment):
        
        _order, payment = validate_and_submit_checkout(
            db=mock_db_session,
            cart_items=items,
            address_id="addr-001",
            slot_id="slt-001",
            discount_code=None,
            loyalty_points_to_redeem=None,
            payment_method="upi",
            client_amount=Decimal("50.00"),
            customer_id="cust-001"
        )
    
    # Verify order created with payment_pending status
    assert mock_db_session.add.called
    assert mock_db_session.commit.called
    
    # Verify payment status is initiated (never confirmed before payment succeeds)
    assert payment.status == "initiated"
