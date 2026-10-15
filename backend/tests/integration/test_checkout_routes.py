"""Integration tests for checkout endpoints."""
from datetime import UTC, datetime
from decimal import Decimal

from fastapi.testclient import TestClient

from app.main import app
from app.models.address import Address
from app.models.customer import Customer
from app.models.delivery_slot import DeliverySlot
from app.models.order import Order
from app.models.payment import Payment
from app.models.promotion import Promotion

client = TestClient(app)


def test_cart_pricing_basic(test_db_session, auth_token, sample_product):
    """Test basic cart pricing endpoint."""
    response = client.post(
        "/api/v1/cart/price",
        json={
            "items": [{"product_id": "prod-001", "quantity": 2}],
            "discount_code": None,
            "loyalty_points_to_redeem": None
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["subtotal"] == "50.00"
    assert data["discount_amount"] == "0.00"
    assert data["final_amount"] == "50.00"
    assert data["currency"] == "INR"


def test_cart_pricing_with_discount(test_db_session, auth_token, sample_product):
    """Test cart pricing with valid discount code."""
    # Create discount
    now_iso = datetime.now(UTC).isoformat()
    discount = Promotion(
        promotion_id="disc-001",
        code="SAVE10",
        description="Save ₹10",
        discount_type="flat",
        discount_value=10.0,
        minimum_order_threshold=0.0,
        usage_limit=100,
        usage_count=0,
        valid_from="2026-01-01T00:00:00Z",
        valid_to="2026-12-31T23:59:59Z",
        is_active="true",
        applicability_json="{}",
        created_at=now_iso,
        updated_at=now_iso
    )
    test_db_session.add(discount)
    test_db_session.commit()
    
    response = client.post(
        "/api/v1/cart/price",
        json={
            "items": [{"product_id": "prod-001", "quantity": 2}],
            "discount_code": "SAVE10",
            "loyalty_points_to_redeem": None
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["subtotal"] == "50.00"
    assert data["discount_amount"] == "10.00"
    assert data["final_amount"] == "40.00"


def test_cart_pricing_invalid_discount(test_db_session, auth_token, sample_product):
    """Test cart pricing with invalid discount code returns warning."""
    response = client.post(
        "/api/v1/cart/price",
        json={
            "items": [{"product_id": "prod-001", "quantity": 2}],
            "discount_code": "INVALID",
            "loyalty_points_to_redeem": None
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["discount_amount"] == "0.00"
    assert len(data["warnings"]) == 1
    assert data["warnings"][0]["reason"] == "DISCOUNT_CODE_NOT_FOUND"


def test_cart_pricing_expired_discount(test_db_session, auth_token, sample_product):
    """Test cart pricing with expired discount returns warning."""
    now_iso = datetime.now(UTC).isoformat()
    discount = Promotion(
        promotion_id="disc-002",
        code="EXPIRED",
        description="Expired discount",
        discount_type="flat",
        discount_value=10.0,
        minimum_order_threshold=0.0,
        usage_limit=None,
        usage_count=0,
        valid_from="2025-01-01T00:00:00Z",
        valid_to="2025-12-31T23:59:59Z",
        is_active="true",
        applicability_json="{}",
        created_at=now_iso,
        updated_at=now_iso
    )
    test_db_session.add(discount)
    test_db_session.commit()
    
    response = client.post(
        "/api/v1/cart/price",
        json={
            "items": [{"product_id": "prod-001", "quantity": 2}],
            "discount_code": "EXPIRED",
            "loyalty_points_to_redeem": None
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["discount_amount"] == "0.00"
    assert len(data["warnings"]) == 1
    assert data["warnings"][0]["reason"] == "DISCOUNT_EXPIRED"


def test_cart_pricing_minimum_threshold_not_met(test_db_session, auth_token, sample_product):
    """Test cart pricing with discount below minimum threshold."""
    now_iso = datetime.now(UTC).isoformat()
    discount = Promotion(
        promotion_id="disc-003",
        code="MIN100",
        description="₹15 off on orders above ₹100",
        discount_type="flat",
        discount_value=15.0,
        minimum_order_threshold=100.0,
        usage_limit=None,
        usage_count=0,
        valid_from="2026-01-01T00:00:00Z",
        valid_to="2026-12-31T23:59:59Z",
        is_active="true",
        applicability_json="{}",
        created_at=now_iso,
        updated_at=now_iso
    )
    test_db_session.add(discount)
    test_db_session.commit()
    
    response = client.post(
        "/api/v1/cart/price",
        json={
            "items": [{"product_id": "prod-001", "quantity": 2}],
            "discount_code": "MIN100",
            "loyalty_points_to_redeem": None
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["discount_amount"] == "0.00"
    assert len(data["warnings"]) == 1
    assert "MINIMUM_ORDER_THRESHOLD_NOT_MET" in data["warnings"][0]["reason"]


def test_cart_pricing_with_loyalty_redemption(test_db_session, auth_token, sample_product, sample_customer):
    """Test cart pricing with loyalty points redemption."""
    # Update customer loyalty points
    customer = test_db_session.query(Customer).filter(
        Customer.customer_id == "cust-001"
    ).first()
    customer.loyalty_points = 500
    test_db_session.commit()
    
    response = client.post(
        "/api/v1/cart/price",
        json={
            "items": [{"product_id": "prod-001", "quantity": 2}],
            "discount_code": None,
            "loyalty_points_to_redeem": 200
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert Decimal(data["subtotal"]) == Decimal("50.00")
    assert Decimal(data["loyalty_redeemed_amount"]) == Decimal("10.00")  # 200 points = ₹10
    assert Decimal(data["final_amount"]) == Decimal("40.00")


def test_checkout_submit_success(test_db_session, auth_token, sample_product, sample_customer, sample_address):
    """Test successful checkout submission."""
    # Create delivery slot
    now_iso = datetime.now(UTC).isoformat()
    slot = DeliverySlot(
        slot_id="slt-001",
        slot_date="2026-10-16",
        start_time="09:00",
        end_time="11:00",
        label="9 AM - 11 AM",
        max_capacity=10,
        reserved_count=5,
        is_available="true",
        service_zone="Mumbai-South",
        created_at=now_iso,
        updated_at=now_iso
    )
    test_db_session.add(slot)
    test_db_session.commit()
    
    response = client.post(
        "/api/v1/checkout/submit",
        json={
            "cart_items": [{"product_id": "prod-001", "quantity": 2}],
            "address_id": "addr-001",
            "slot_id": "slt-001",
            "discount_code": None,
            "loyalty_points_to_redeem": None,
            "payment_method": "upi",
            "client_amount": "50.00"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "order_id" in data
    assert "payment_id" in data
    assert data["payment_status"] == "initiated"
    assert Decimal(str(data["amount"])) == Decimal("50.00")
    assert data["currency"] == "INR"
    
    # Verify order created
    order = test_db_session.query(Order).filter(
        Order.order_id == data["order_id"]
    ).first()
    assert order is not None
    assert order.status == "payment_pending"
    
    # Verify payment created
    payment = test_db_session.query(Payment).filter(
        Payment.payment_id == data["payment_id"]
    ).first()
    assert payment is not None
    assert payment.status == "initiated"


def test_checkout_empty_cart_rejected(test_db_session, auth_token, sample_address):
    """Test checkout rejected for empty cart."""
    response = client.post(
        "/api/v1/checkout/submit",
        json={
            "cart_items": [],
            "address_id": "addr-001",
            "slot_id": "slt-001",
            "discount_code": None,
            "loyalty_points_to_redeem": None,
            "payment_method": "upi",
            "client_amount": "0.00"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 422
    data = response.json()
    assert data["error"]["code"] == "CART_EMPTY"


def test_checkout_unserviceable_address_rejected(test_db_session, auth_token, sample_product):
    """Test checkout rejected for unserviceable address."""
    # Create unserviceable address
    now_iso = datetime.now(UTC).isoformat()
    address = Address(
        address_id="addr-002",
        customer_id="cust-001",
        address_line1="Far location",
        city="Pune",
        state="Maharashtra",
        postal_code="411001",
        country="India",
        serviceability_status="not_serviceable",
        serviceability_reason="Outside delivery zone",
        created_at=now_iso,
        updated_at=now_iso
    )
    test_db_session.add(address)
    test_db_session.commit()
    
    response = client.post(
        "/api/v1/checkout/submit",
        json={
            "cart_items": [{"product_id": "prod-001", "quantity": 2}],
            "address_id": "addr-002",
            "slot_id": "slt-001",
            "discount_code": None,
            "loyalty_points_to_redeem": None,
            "payment_method": "upi",
            "client_amount": "50.00"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 409
    data = response.json()
    assert data["error"]["code"] == "ADDRESS_NOT_SERVICEABLE"


def test_checkout_slot_capacity_exceeded_rejected(test_db_session, auth_token, sample_product, sample_address):
    """Test checkout rejected when slot capacity is full."""
    # Create full slot
    now_iso = datetime.now(UTC).isoformat()
    slot = DeliverySlot(
        slot_id="slt-002",
        slot_date="2026-10-16",
        start_time="14:00",
        end_time="16:00",
        label="2 PM - 4 PM",
        max_capacity=10,
        reserved_count=10,  # Full
        is_available="true",
        service_zone="Mumbai-South",
        created_at=now_iso,
        updated_at=now_iso
    )
    test_db_session.add(slot)
    test_db_session.commit()
    
    response = client.post(
        "/api/v1/checkout/submit",
        json={
            "cart_items": [{"product_id": "prod-001", "quantity": 2}],
            "address_id": "addr-001",
            "slot_id": "slt-002",
            "discount_code": None,
            "loyalty_points_to_redeem": None,
            "payment_method": "upi",
            "client_amount": "50.00"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 409
    data = response.json()
    assert data["error"]["code"] == "SLOT_CAPACITY_EXCEEDED"


def test_checkout_amount_mismatch_rejected(test_db_session, auth_token, sample_product, sample_address):
    """Test checkout rejected when client amount doesn't match server calculation."""
    # Create slot
    now_iso = datetime.now(UTC).isoformat()
    slot = DeliverySlot(
        slot_id="slt-003",
        slot_date="2026-10-16",
        start_time="17:00",
        end_time="19:00",
        label="5 PM - 7 PM",
        max_capacity=10,
        reserved_count=3,
        is_available="true",
        service_zone="Mumbai-South",
        created_at=now_iso,
        updated_at=now_iso
    )
    test_db_session.add(slot)
    test_db_session.commit()
    
    response = client.post(
        "/api/v1/checkout/submit",
        json={
            "cart_items": [{"product_id": "prod-001", "quantity": 2}],
            "address_id": "addr-001",
            "slot_id": "slt-003",
            "discount_code": None,
            "loyalty_points_to_redeem": None,
            "payment_method": "upi",
            "client_amount": "100.00"  # Should be 50.00
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 409
    data = response.json()
    assert data["error"]["code"] == "AMOUNT_MISMATCH"


def test_checkout_order_never_confirmed_without_payment(test_db_session, auth_token, sample_product, sample_address):
    """Test order status remains payment_pending when payment is initiated."""
    # Create slot
    now_iso = datetime.now(UTC).isoformat()
    slot = DeliverySlot(
        slot_id="slt-004",
        slot_date="2026-10-17",
        start_time="10:00",
        end_time="12:00",
        label="10 AM - 12 PM",
        max_capacity=10,
        reserved_count=2,
        is_available="true",
        service_zone="Mumbai-South",
        created_at=now_iso,
        updated_at=now_iso
    )
    test_db_session.add(slot)
    test_db_session.commit()
    
    response = client.post(
        "/api/v1/checkout/submit",
        json={
            "cart_items": [{"product_id": "prod-001", "quantity": 2}],
            "address_id": "addr-001",
            "slot_id": "slt-004",
            "discount_code": None,
            "loyalty_points_to_redeem": None,
            "payment_method": "card",
            "client_amount": "50.00"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify order status is payment_pending
    order = test_db_session.query(Order).filter(
        Order.order_id == data["order_id"]
    ).first()
    assert order.status == "payment_pending"
    assert order.confirmed_at is None
    
    # Verify payment status is initiated
    payment = test_db_session.query(Payment).filter(
        Payment.order_id == data["order_id"]
    ).first()
    assert payment.status == "initiated"


def test_get_order_detail(test_db_session, auth_token, sample_product, sample_address):
    """Test retrieving order detail."""
    # Create order with slot and items
    now_iso = datetime.now(UTC).isoformat()
    
    slot = DeliverySlot(
        slot_id="slt-005",
        slot_date="2026-10-18",
        start_time="15:00",
        end_time="17:00",
        label="3 PM - 5 PM",
        max_capacity=10,
        reserved_count=5,
        is_available="true",
        service_zone="Mumbai-South",
        created_at=now_iso,
        updated_at=now_iso
    )
    test_db_session.add(slot)
    test_db_session.commit()
    
    # Submit checkout
    response = client.post(
        "/api/v1/checkout/submit",
        json={
            "cart_items": [{"product_id": "prod-001", "quantity": 3}],
            "address_id": "addr-001",
            "slot_id": "slt-005",
            "discount_code": None,
            "loyalty_points_to_redeem": None,
            "payment_method": "upi",
            "client_amount": "75.00"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    order_data = response.json()
    order_id = order_data["order_id"]
    
    # Get order detail
    response = client.get(
        f"/api/v1/orders/{order_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["order_id"] == order_id
    assert data["status"] == "payment_pending"
    assert data["payment_status"] == "initiated"
    assert Decimal(data["final_amount"]) == Decimal("75.00")
    assert data["slot"] is not None
    assert data["slot"]["slot_id"] == "slt-005"
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == "prod-001"
    assert data["items"][0]["quantity"] == 3
