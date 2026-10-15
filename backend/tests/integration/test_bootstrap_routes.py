"""Integration tests for bootstrap endpoint."""
import json
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient

from app.auth.services import create_access_token
from app.main import app
from app.models.address import Address
from app.models.category import Category
from app.models.delivery_slot import DeliverySlot
from app.models.product import Product
from app.models.promotion import Promotion
from app.models.recommendation import Recommendation
from app.models.review import Review
from app.models.shopping_list import ShoppingList, ShoppingListItem

client = TestClient(app)


def test_bootstrap_returns_profile_and_data(sample_customer, sample_address, sample_product, auth_token, test_db):
    """Test bootstrap endpoint returns profile, addresses, categories, recommendations, lists."""
    # Create test data
    category = Category(
        category_id="cat-002",
        name="Fresh Fruits",
        is_active=1,
        icon_url="https://example.com/icon.svg",
        created_at=datetime.now(UTC).isoformat(),
        updated_at=datetime.now(UTC).isoformat()
    )
    test_db.add(category)
    
    recommendation = Recommendation(
        recommendation_id="rec-001",
        customer_id=sample_customer.customer_id,
        product_id="prod-001",
        score=0.95,
        reason_tag="reorder_reminder",
        reason_text="You buy these every week",
        generated_at=datetime.now(UTC).isoformat()
    )
    test_db.add(recommendation)
    
    shopping_list = ShoppingList(
        list_id="lst-001",
        customer_id=sample_customer.customer_id,
        name="Weekly Staples",
        is_ai_generated=0,
        suggestion_note=None,
        created_at=datetime.now(UTC).isoformat(),
        updated_at=datetime.now(UTC).isoformat()
    )
    test_db.add(shopping_list)
    
    test_db.commit()
    
    # Call bootstrap endpoint
    response = client.get(
        "/api/v1/app/bootstrap",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify profile
    assert data["profile"]["customer_id"] == sample_customer.customer_id
    assert data["profile"]["name"] == sample_customer.full_name
    assert data["profile"]["loyalty_points"] == 420
    
    # Verify default address
    assert data["default_address"] is not None
    assert data["default_address"]["address_id"] == sample_address.address_id
    assert data["default_address"]["serviceability"]["is_serviceable"] is True
    
    # Verify categories
    assert len(data["featured_categories"]) > 0
    assert data["featured_categories"][0]["category_id"] == "cat-001"
    
    # Verify recommendations
    assert len(data["recommendations"]) > 0
    assert data["recommendations"][0]["recommendation_id"] == "rec-001"
    assert data["recommendations"][0]["reason_tag"] == "reorder_reminder"
    
    # Verify shopping lists
    assert len(data["shopping_lists"]) > 0
    assert data["shopping_lists"][0]["list_id"] == "lst-001"
    assert data["shopping_lists"][0]["is_ai_generated"] is False


def test_bootstrap_requires_authentication(test_db):
    """Test bootstrap endpoint requires JWT token."""
    response = client.get("/api/v1/app/bootstrap")
    
    assert response.status_code == 401


def test_bootstrap_with_include_ops_for_operator(sample_customer, auth_token, test_db):
    """Test bootstrap endpoint returns ops summary for operator role."""
    # Create operator token
    operator_token, _ = create_access_token(
        customer_id=sample_customer.customer_id,
        role="operator"
    )
    
    # Create slot with high utilization
    slot = DeliverySlot(
        slot_id="slt-001",
        slot_date="2026-10-16",
        start_time="09:00",
        end_time="11:00",
        label="Morning",
        max_capacity=20,
        reserved_count=19,
        is_available="true",
        service_zone="Mumbai-South",
        created_at=datetime.now(UTC).isoformat(),
        updated_at=datetime.now(UTC).isoformat()
    )
    test_db.add(slot)
    test_db.commit()
    
    # Call bootstrap with includeOps=true
    response = client.get(
        "/api/v1/app/bootstrap?includeOps=true",
        headers={"Authorization": f"Bearer {operator_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify ops summary is included
    assert data["ops_summary"] is not None
    assert "open_slot_alerts" in data["ops_summary"]
    assert "promotion_warnings" in data["ops_summary"]
    assert "negative_sentiment_products" in data["ops_summary"]
    assert data["ops_summary"]["open_slot_alerts"] == 1


def test_bootstrap_with_include_ops_for_shopper_returns_403(sample_customer, auth_token, test_db):
    """Test bootstrap endpoint returns 403 when shopper tries includeOps=true."""
    # auth_token is shopper role by default
    response = client.get(
        "/api/v1/app/bootstrap?includeOps=true",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 403
    error = response.json()
    assert error["error"]["code"] == "FORBIDDEN_ROLE_SCOPE"


def test_bootstrap_ops_summary_excludes_pii(sample_customer, test_db):
    """Test that ops summary in bootstrap does not expose PII."""
    # Create operator token
    operator_token, _ = create_access_token(
        customer_id=sample_customer.customer_id,
        role="operator"
    )
    
    response = client.get(
        "/api/v1/app/bootstrap?includeOps=true",
        headers={"Authorization": f"Bearer {operator_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    ops_summary = data["ops_summary"]
    
    # Verify no PII in ops summary
    ops_str = json.dumps(ops_summary)
    assert "phone" not in ops_str.lower()
    assert "email" not in ops_str.lower()
    assert "allergy" not in ops_str.lower()
    assert sample_customer.full_name not in ops_str


def test_bootstrap_with_no_default_address(sample_customer, auth_token, test_db):
    """Test bootstrap handles customer with no default address."""
    # Remove default address flag
    address = test_db.query(Address).filter(
        Address.customer_id == sample_customer.customer_id
    ).first()
    if address:
        address.is_default = 0
        test_db.commit()
    
    response = client.get(
        "/api/v1/app/bootstrap",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["default_address"] is None


def test_bootstrap_with_empty_recommendations(sample_customer, auth_token, test_db):
    """Test bootstrap handles customer with no recommendations."""
    response = client.get(
        "/api/v1/app/bootstrap",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["recommendations"] == []


def test_bootstrap_with_empty_shopping_lists(sample_customer, auth_token, test_db):
    """Test bootstrap handles customer with no shopping lists."""
    response = client.get(
        "/api/v1/app/bootstrap",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["shopping_lists"] == []


def test_bootstrap_includes_list_item_count(sample_customer, sample_product, auth_token, test_db):
    """Test bootstrap includes item count for each shopping list."""
    # Create shopping list with items
    shopping_list = ShoppingList(
        list_id="lst-001",
        customer_id=sample_customer.customer_id,
        name="Weekly Staples",
        is_ai_generated=0,
        created_at=datetime.now(UTC).isoformat(),
        updated_at=datetime.now(UTC).isoformat()
    )
    test_db.add(shopping_list)
    
    # Create additional products for list items (skip prod-001 which sample_product created)
    now_iso = datetime.now(UTC).isoformat()
    # Use sample_product's product (prod-001) and create 4 more (prod-101 to prod-104)
    product_ids = [sample_product.product_id] + [f"prod-{100+i}" for i in range(1, 5)]
    for i in range(1, 5):
        product = Product(
            product_id=f"prod-{100+i}",
            category_id="cat-001",
            name=f"Test Product {i}",
            unit_type="kg",
            unit_price=25.0,
            is_organic="false",
            is_featured="false",
            tags_json="[]",
            nutrition_json="{}",
            created_at=now_iso,
            updated_at=now_iso
        )
        test_db.add(product)
    
    # Add items using the product IDs we created
    for i, product_id in enumerate(product_ids):
        item = ShoppingListItem(
            item_id=f"itm-{i:03d}",
            list_id="lst-001",
            product_id=product_id,
            quantity=1,
            added_at=datetime.now(UTC).isoformat()
        )
        test_db.add(item)
    
    test_db.commit()
    
    response = client.get(
        "/api/v1/app/bootstrap",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["shopping_lists"]) > 0
    assert data["shopping_lists"][0]["item_count"] == 5


def test_ops_summary_counts_negative_sentiment_products(sample_customer, sample_product, sample_address, test_db):
    """Test ops summary counts products with negative sentiment majority."""
    # Create operator token
    operator_token, _ = create_access_token(
        customer_id=sample_customer.customer_id,
        role="operator"
    )
    
    # Create delivery slot for the order
    slot = DeliverySlot(
        slot_id="slt-001",
        slot_date="2026-10-16",
        start_time="09:00",
        end_time="11:00",
        label="Morning",
        max_capacity=100,
        reserved_count=10,
        is_available="true",
        service_zone="Mumbai-South",
        created_at=datetime.now(UTC).isoformat(),
        updated_at=datetime.now(UTC).isoformat()
    )
    test_db.add(slot)
    
    # Create order for the reviews
    from app.models.order import Order, OrderItem
    order = Order(
        order_id="ord-001",
        customer_id=sample_customer.customer_id,
        address_id=sample_address.address_id,
        slot_id="slt-001",
        status="delivered",
        subtotal=25.00,
        discount_amount=0.00,
        loyalty_redeemed_amount=0.00,
        final_amount=25.00,
        order_date=datetime.now(UTC).isoformat(),
        confirmed_at=datetime.now(UTC).isoformat()
    )
    test_db.add(order)
    
    order_item = OrderItem(
        item_id="item-001",
        order_id="ord-001",
        product_id=sample_product.product_id,
        quantity=1,
        unit_price=25.00,
        total_price=25.00
    )
    test_db.add(order_item)
    
    # Create reviews with negative sentiment
    for i in range(5):
        review = Review(
            review_id=f"rev-{i:03d}",
            order_id="ord-001",
            product_id=sample_product.product_id,
            customer_id=sample_customer.customer_id,
            rating=2 if i < 4 else 4,
            review_text="Test review",
            sentiment="negative" if i < 4 else "positive",
            reviewed_at=datetime.now(UTC).isoformat()
        )
        test_db.add(review)
    
    test_db.commit()
    
    response = client.get(
        "/api/v1/app/bootstrap?includeOps=true",
        headers={"Authorization": f"Bearer {operator_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Should count product with 4/5 negative reviews
    assert data["ops_summary"]["negative_sentiment_products"] >= 1


def test_ops_summary_counts_promotion_warnings(sample_customer, test_db):
    """Test ops summary counts promotions with low usage."""
    # Create operator token
    operator_token, _ = create_access_token(
        customer_id=sample_customer.customer_id,
        role="operator"
    )
    
    # Create promotion with low usage
    now_iso = datetime.now(UTC).isoformat()
    promotion = Promotion(
        promotion_id="prm-001",
        code="LOWUSE10",
        discount_type="percentage",
        discount_value=10,
        minimum_order_threshold=100.00,
        applicability_json="{}",
        valid_from=now_iso,
        valid_to=(datetime.now(UTC).replace(year=2027)).isoformat(),
        usage_count=2,
        usage_limit=100,
        is_active="true",
        created_at=now_iso,
        updated_at=now_iso
    )
    test_db.add(promotion)
    test_db.commit()
    
    response = client.get(
        "/api/v1/app/bootstrap?includeOps=true",
        headers={"Authorization": f"Bearer {operator_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["ops_summary"]["promotion_warnings"] >= 1


def test_ops_summary_counts_slot_alerts(sample_customer, test_db):
    """Test ops summary counts slots with high utilization."""
    # Create operator token
    operator_token, _ = create_access_token(
        customer_id=sample_customer.customer_id,
        role="operator"
    )
    
    # Create slots with different utilization
    slots = [
        DeliverySlot(
            slot_id=f"slt-{i:03d}",
            slot_date="2026-10-16",
            start_time="09:00",
            end_time="11:00",
            max_capacity=20,
            reserved_count=19 if i == 0 else 5,  # First slot at 95%
            is_available="true",
            created_at=datetime.now(UTC).isoformat(),
            updated_at=datetime.now(UTC).isoformat()
        )
        for i in range(3)
    ]
    
    for slot in slots:
        test_db.add(slot)
    test_db.commit()
    
    response = client.get(
        "/api/v1/app/bootstrap?includeOps=true",
        headers={"Authorization": f"Bearer {operator_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Should count at least one slot with >=90% capacity
    assert data["ops_summary"]["open_slot_alerts"] >= 1
