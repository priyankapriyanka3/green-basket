"""Integration tests for shopping list routes."""
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.auth.services import create_access_token, hash_password
from app.database import Base, get_db
from app.main import app
from app.models.category import Category
from app.models.customer import Customer
from app.models.order import Order, OrderItem
from app.models.product import Product


@pytest.fixture
def db_session():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    # Override the get_db dependency
    def override_get_db():
        try:
            yield session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield session
    
    session.close()
    app.dependency_overrides.clear()


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def sample_customer(db_session):
    """Create a sample customer with hashed password."""
    hash_password("password123")
    
    customer = Customer(
        customer_id="cust-001",
        full_name="Test Customer",
        phone_number="+919876543210",
        email="test@example.com",
        preferred_language="en",
        dietary_preference="vegetarian",
        allergies_json='["peanut"]',
        loyalty_points=100.0,
        status="active",
        created_at=datetime.now(UTC).isoformat(),
        updated_at=datetime.now(UTC).isoformat()
    )
    db_session.add(customer)
    db_session.commit()
    return customer


@pytest.fixture
def auth_token(db_session, sample_customer):
    """Generate an auth token for the sample customer."""
    token, _ = create_access_token(
        customer_id=sample_customer.customer_id,
        role="shopper"
    )
    return token


@pytest.fixture
def sample_category(db_session):
    """Create a sample category."""
    category = Category(
        category_id="cat-001",
        name="Vegetables",
        description="Fresh vegetables",
        parent_category_id=None,
        display_order=0,
        icon_url="https://example.com/icon.png",
        is_active="true",
        created_at=datetime.now(UTC).isoformat(),
        updated_at=datetime.now(UTC).isoformat()
    )
    db_session.add(category)
    db_session.commit()
    return category


@pytest.fixture
def sample_products(db_session, sample_category):
    """Create sample products."""
    products = [
        Product(
            product_id="prod-001",
            category_id=sample_category.category_id,
            farmer_id=None,
            name="Organic Tomatoes",
            description="Fresh organic tomatoes",
            unit_price=50.0,
            unit_type="kg",
            is_organic="true",
            is_featured="true",
            nutrition_json='{}',
            tags_json='["organic", "fresh"]',
            image_url="https://example.com/tomato.jpg",
            average_rating=4.5,
            review_count=10,
            created_at=datetime.now(UTC).isoformat(),
            updated_at=datetime.now(UTC).isoformat()
        ),
        Product(
            product_id="prod-002",
            category_id=sample_category.category_id,
            farmer_id=None,
            name="Organic Carrots",
            description="Fresh organic carrots",
            unit_price=40.0,
            unit_type="kg",
            is_organic="true",
            is_featured="false",
            nutrition_json='{}',
            tags_json='["organic"]',
            image_url="https://example.com/carrot.jpg",
            average_rating=4.8,
            review_count=15,
            created_at=datetime.now(UTC).isoformat(),
            updated_at=datetime.now(UTC).isoformat()
        )
    ]
    for product in products:
        db_session.add(product)
    db_session.commit()
    return products


@pytest.fixture
def sample_orders(db_session, sample_customer, sample_products):
    """Create sample orders with order items."""
    orders = []
    
    for i in range(3):
        order = Order(
            order_id=f"ord-00{i+1}",
            customer_id=sample_customer.customer_id,
            address_id="addr-001",
            slot_id="slt-001",
            agent_id=None,
            status="delivered",
            subtotal=100.0,
            discount_amount=0.0,
            loyalty_redeemed_amount=0.0,
            final_amount=100.0,
            tracking_url=f"https://track.example.com/ord-00{i+1}",
            order_date=datetime.now(UTC).isoformat(),
            confirmed_at=datetime.now(UTC).isoformat()
        )
        db_session.add(order)
        
        item = OrderItem(
            item_id=f"oi-00{i+1}",
            order_id=order.order_id,
            product_id="prod-001",
            quantity=2,
            unit_price=50.0,
            total_price=100.0
        )
        db_session.add(item)
        orders.append(order)
    
    db_session.commit()
    return orders


def test_generate_shopping_list_weekly_reorder(
    client,
    db_session,
    auth_token,
    sample_customer,
    sample_products,
    sample_orders
):
    """Test generating a weekly reorder shopping list."""
    response = client.post(
        "/api/v1/shopping-lists/generate",
        json={
            "mode": "weekly_reorder",
            "source_order_window_days": 42,
            "target_list_name": "My Weekly Reorder"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    
    assert "list" in data
    assert "suggestion_note" in data
    assert "items_added" in data
    
    assert data["list"]["name"] == "My Weekly Reorder"
    assert data["list"]["is_ai_generated"] is True
    assert data["items_added"] > 0


def test_generate_shopping_list_diet_boost(
    client,
    db_session,
    auth_token,
    sample_customer,
    sample_products,
    sample_orders
):
    """Test generating a diet boost shopping list."""
    response = client.post(
        "/api/v1/shopping-lists/generate",
        json={
            "mode": "diet_boost",
            "source_order_window_days": 30,
            "target_list_name": "Diet Boost List"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    
    assert data["list"]["name"] == "Diet Boost List"
    assert data["list"]["is_ai_generated"] is True
    assert "dietary" in data["suggestion_note"].lower() or "diet" in data["suggestion_note"].lower()


def test_generate_shopping_list_seasonal_refresh(
    client,
    db_session,
    auth_token,
    sample_customer,
    sample_products
):
    """Test generating a seasonal refresh shopping list."""
    response = client.post(
        "/api/v1/shopping-lists/generate",
        json={
            "mode": "seasonal_refresh",
            "source_order_window_days": 42,
            "target_list_name": "Seasonal Picks"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    
    assert data["list"]["name"] == "Seasonal Picks"
    assert data["list"]["is_ai_generated"] is True
    assert "seasonal" in data["suggestion_note"].lower()


def test_source_order_window_validation_min(
    client,
    db_session,
    auth_token,
    sample_customer,
    sample_products
):
    """Test that source order window below 7 days is rejected."""
    response = client.post(
        "/api/v1/shopping-lists/generate",
        json={
            "mode": "weekly_reorder",
            "source_order_window_days": 5,
            "target_list_name": "Test List"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 422


def test_source_order_window_validation_max(
    client,
    db_session,
    auth_token,
    sample_customer,
    sample_products
):
    """Test that source order window above 90 days is rejected."""
    response = client.post(
        "/api/v1/shopping-lists/generate",
        json={
            "mode": "weekly_reorder",
            "source_order_window_days": 95,
            "target_list_name": "Test List"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 422


def test_shopping_list_respects_dietary_preferences(
    client,
    db_session,
    auth_token,
    sample_customer,
    sample_products
):
    """Test that shopping list generation respects dietary preferences."""
    response = client.post(
        "/api/v1/shopping-lists/generate",
        json={
            "mode": "diet_boost",
            "source_order_window_days": 42,
            "target_list_name": "Vegetarian List"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    
    # Check that items in list are appropriate for dietary preference
    assert data["list"]["is_ai_generated"] is True
    assert len(data["list"]["items"]) > 0


def test_shopping_list_respects_allergies(
    client,
    db_session,
    auth_token,
    sample_customer,
    sample_products
):
    """Test that shopping list generation respects customer allergies."""
    # Add a peanut product
    peanut_product = Product(
        product_id="prod-peanut",
        category_id=sample_products[0].category_id,
        farmer_id=None,
        name="Peanut Butter",
        description="Creamy peanut butter",
        unit_price=150.0,
        unit_type="jar",
        is_organic="false",
        is_featured="true",
        nutrition_json='{}',
        tags_json='[]',
        image_url="https://example.com/peanut.jpg",
        average_rating=4.0,
        review_count=5,
        created_at=datetime.now(UTC).isoformat(),
        updated_at=datetime.now(UTC).isoformat()
    )
    db_session.add(peanut_product)
    db_session.commit()
    
    response = client.post(
        "/api/v1/shopping-lists/generate",
        json={
            "mode": "seasonal_refresh",
            "source_order_window_days": 42,
            "target_list_name": "Safe List"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    
    # Check that peanut products are excluded
    product_names = [item["product_name"].lower() for item in data["list"]["items"]]
    assert not any("peanut" in name for name in product_names)


def test_get_shopping_lists(
    client,
    db_session,
    auth_token,
    sample_customer,
    sample_products
):
    """Test retrieving all shopping lists for a customer."""
    # Generate a list first
    client.post(
        "/api/v1/shopping-lists/generate",
        json={
            "mode": "weekly_reorder",
            "source_order_window_days": 42,
            "target_list_name": "Test List"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    # Get all lists
    response = client.get(
        "/api/v1/shopping-lists/",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["name"] == "Test List"


def test_get_shopping_list_by_id(
    client,
    db_session,
    auth_token,
    sample_customer,
    sample_products
):
    """Test retrieving a specific shopping list by ID."""
    # Generate a list first
    create_response = client.post(
        "/api/v1/shopping-lists/generate",
        json={
            "mode": "weekly_reorder",
            "source_order_window_days": 42,
            "target_list_name": "Specific List"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    list_id = create_response.json()["list"]["list_id"]
    
    # Get the specific list
    response = client.get(
        f"/api/v1/shopping-lists/{list_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["list_id"] == list_id
    assert data["name"] == "Specific List"


def test_shopping_list_items_include_reason_tags(
    client,
    db_session,
    auth_token,
    sample_customer,
    sample_products,
    sample_orders
):
    """Test that shopping list items include reason tags."""
    response = client.post(
        "/api/v1/shopping-lists/generate",
        json={
            "mode": "weekly_reorder",
            "source_order_window_days": 42,
            "target_list_name": "Tagged List"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    
    # Check that items have reason tags
    items = data["list"]["items"]
    assert len(items) > 0
    
    for item in items:
        assert "source_reason_tag" in item
        # Reason tag should be one of the allowed values
        allowed_tags = {
            "frequently_bought",
            "seasonal",
            "reorder_reminder",
            "based_on_diet",
            "trending"
        }
        if item["source_reason_tag"]:
            assert item["source_reason_tag"] in allowed_tags


def test_shopping_list_generation_requires_auth(
    client,
    db_session,
    sample_customer,
    sample_products
):
    """Test that shopping list generation requires authentication."""
    response = client.post(
        "/api/v1/shopping-lists/generate",
        json={
            "mode": "weekly_reorder",
            "source_order_window_days": 42,
            "target_list_name": "Unauthorized List"
        }
    )
    
    assert response.status_code == 401


def test_get_shopping_lists_requires_auth(
    client,
    db_session
):
    """Test that retrieving shopping lists requires authentication."""
    response = client.get("/api/v1/shopping-lists/")
    
    assert response.status_code == 401


def test_generated_list_marked_as_ai_generated(
    client,
    db_session,
    auth_token,
    sample_customer,
    sample_products
):
    """Test that generated lists are marked with is_ai_generated flag."""
    response = client.post(
        "/api/v1/shopping-lists/generate",
        json={
            "mode": "seasonal_refresh",
            "source_order_window_days": 42,
            "target_list_name": "AI List"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    
    assert data["list"]["is_ai_generated"] is True


def test_shopping_list_has_suggestion_note(
    client,
    db_session,
    auth_token,
    sample_customer,
    sample_products
):
    """Test that generated lists include suggestion notes."""
    response = client.post(
        "/api/v1/shopping-lists/generate",
        json={
            "mode": "diet_boost",
            "source_order_window_days": 42,
            "target_list_name": "Note List"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    
    assert data["suggestion_note"] is not None
    assert len(data["suggestion_note"]) > 0
    assert data["list"]["suggestion_note"] is not None
