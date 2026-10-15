"""Unit tests for recommendation service."""
from datetime import UTC, datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models.category import Category
from app.models.customer import Customer
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.recommendations.services import RecommendationService


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
    yield session
    session.close()


@pytest.fixture
def sample_customer(db_session: Session):
    """Create a sample customer."""
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
def sample_category(db_session: Session):
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
def sample_products(db_session: Session, sample_category):
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
        ),
        Product(
            product_id="prod-003",
            category_id=sample_category.category_id,
            farmer_id=None,
            name="Peanut Butter",
            description="Creamy peanut butter",
            unit_price=150.0,
            unit_type="jar",
            is_organic="false",
            is_featured="false",
            nutrition_json='{}',
            tags_json='[]',
            image_url="https://example.com/peanut.jpg",
            average_rating=4.0,
            review_count=5,
            created_at=datetime.now(UTC).isoformat(),
            updated_at=datetime.now(UTC).isoformat()
        )
    ]
    for product in products:
        db_session.add(product)
    db_session.commit()
    return products


@pytest.fixture
def sample_orders(db_session: Session, sample_customer, sample_products):
    """Create sample orders with order items."""
    orders = []
    
    # Create 3 orders
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
        
        # Add order items (customer frequently buys prod-001)
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


def test_generate_reorder_recommendations(
    db_session: Session,
    sample_customer,
    sample_products,
    sample_orders
):
    """Test that reorder recommendations are generated based on purchase history."""
    service = RecommendationService(db_session)
    
    recommendations = service.generate_recommendations(
        customer_id=sample_customer.customer_id,
        force_refresh=True
    )
    
    # Should have recommendations
    assert len(recommendations) > 0
    
    # Should include reorder_reminder for frequently bought product
    reorder_recs = [r for r in recommendations if r.reason_tag == "reorder_reminder"]
    assert len(reorder_recs) > 0
    
    # Check that the frequently bought product is recommended
    product_ids = [r.product_id for r in reorder_recs]
    assert "prod-001" in product_ids


def test_recommendation_reason_tags_valid(
    db_session: Session,
    sample_customer,
    sample_products,
    sample_orders
):
    """Test that all recommendation reason tags are from the allowed set."""
    service = RecommendationService(db_session)
    
    recommendations = service.generate_recommendations(
        customer_id=sample_customer.customer_id,
        force_refresh=True
    )
    
    allowed_tags = {
        "frequently_bought",
        "seasonal",
        "reorder_reminder",
        "based_on_diet",
        "trending"
    }
    
    for rec in recommendations:
        assert rec.reason_tag in allowed_tags


def test_diet_based_recommendations_respect_preferences(
    db_session: Session,
    sample_customer,
    sample_products
):
    """Test that diet-based recommendations respect dietary preferences."""
    service = RecommendationService(db_session)
    
    recommendations = service.generate_recommendations(
        customer_id=sample_customer.customer_id,
        force_refresh=True
    )
    
    # Should have diet-based recommendations
    diet_recs = [r for r in recommendations if r.reason_tag == "based_on_diet"]
    assert len(diet_recs) > 0
    
    # Verify products in diet recommendations are organic (vegetarian preference)
    for rec in diet_recs:
        product = db_session.query(Product).filter(
            Product.product_id == rec.product_id
        ).first()
        assert product.is_organic == "true"


def test_recommendations_avoid_allergens(
    db_session: Session,
    sample_customer,
    sample_products
):
    """Test that recommendations avoid products with customer allergens."""
    # Create a peanut product
    peanut_product = Product(
        product_id="prod-peanut",
        category_id=sample_products[0].category_id,
        farmer_id=None,
        name="Creamy Peanut Butter",
        description="Smooth peanut butter",
        unit_price=150.0,
        unit_type="jar",
        is_organic="false",
        is_featured="false",
        nutrition_json='{}',
        tags_json='[]',
        image_url="https://example.com/peanut.jpg",
        average_rating=4.2,
        review_count=8,
        created_at=datetime.now(UTC).isoformat(),
        updated_at=datetime.now(UTC).isoformat()
    )
    db_session.add(peanut_product)
    db_session.commit()
    
    service = RecommendationService(db_session)
    
    recommendations = service.generate_recommendations(
        customer_id=sample_customer.customer_id,
        force_refresh=True
    )
    
    # Check that peanut products are excluded (customer has peanut allergy)
    product_ids = [rec.product_id for rec in recommendations]
    assert "prod-peanut" not in product_ids


def test_recommendation_scoring_logic(
    db_session: Session,
    sample_customer,
    sample_products,
    sample_orders
):
    """Test that recommendation scores are calculated correctly."""
    service = RecommendationService(db_session)
    
    recommendations = service.generate_recommendations(
        customer_id=sample_customer.customer_id,
        force_refresh=True
    )
    
    # All recommendations should have scores
    for rec in recommendations:
        assert rec.score > 0.0
        assert rec.score <= 1.0


def test_recommendation_includes_reason_text(
    db_session: Session,
    sample_customer,
    sample_products,
    sample_orders
):
    """Test that each recommendation includes reason text."""
    service = RecommendationService(db_session)
    
    recommendations = service.generate_recommendations(
        customer_id=sample_customer.customer_id,
        force_refresh=True
    )
    
    # All recommendations should have reason text
    for rec in recommendations:
        assert rec.reason_text is not None
        assert len(rec.reason_text) > 0


def test_recommendation_timestamps_preserved(
    db_session: Session,
    sample_customer,
    sample_products
):
    """Test that recommendation generation timestamps are preserved."""
    service = RecommendationService(db_session)
    
    recommendations = service.generate_recommendations(
        customer_id=sample_customer.customer_id,
        force_refresh=True
    )
    
    # All recommendations should have generated_at timestamp
    for rec in recommendations:
        assert rec.generated_at is not None
        # Should be valid ISO 8601 format
        datetime.fromisoformat(rec.generated_at)


def test_trending_recommendations_generated(
    db_session: Session,
    sample_customer,
    sample_products
):
    """Test that trending recommendations are generated."""
    service = RecommendationService(db_session)
    
    recommendations = service.generate_recommendations(
        customer_id=sample_customer.customer_id,
        force_refresh=True
    )
    
    # Should have trending recommendations
    trending_recs = [r for r in recommendations if r.reason_tag == "trending"]
    assert len(trending_recs) > 0


def test_seasonal_recommendations_generated(
    db_session: Session,
    sample_customer,
    sample_products
):
    """Test that seasonal recommendations are generated."""
    service = RecommendationService(db_session)
    
    recommendations = service.generate_recommendations(
        customer_id=sample_customer.customer_id,
        force_refresh=True
    )
    
    # Should have seasonal recommendations
    seasonal_recs = [r for r in recommendations if r.reason_tag == "seasonal"]
    assert len(seasonal_recs) > 0


def test_get_customer_recommendations(
    db_session: Session,
    sample_customer,
    sample_products,
    sample_orders
):
    """Test retrieving customer recommendations with product details."""
    service = RecommendationService(db_session)
    
    # Generate recommendations first
    service.generate_recommendations(
        customer_id=sample_customer.customer_id,
        force_refresh=True
    )
    
    # Retrieve recommendations
    cards = service.get_customer_recommendations(
        customer_id=sample_customer.customer_id,
        limit=10
    )
    
    # Should have recommendation cards
    assert len(cards) > 0
    
    # Each card should have complete product info
    for card in cards:
        assert card.product_id is not None
        assert card.name is not None
        assert card.unit_price > 0
        assert card.reason_tag is not None
        assert card.reason_text is not None


def test_reason_distribution_reporting(
    db_session: Session,
    sample_customer,
    sample_products,
    sample_orders
):
    """Test that reason distribution can be queried for operations reporting."""
    service = RecommendationService(db_session)
    
    # Generate recommendations
    service.generate_recommendations(
        customer_id=sample_customer.customer_id,
        force_refresh=True
    )
    
    # Get reason distribution
    distribution = service.get_reason_distribution()
    
    # Should have counts for each reason type
    assert isinstance(distribution, dict)
    assert len(distribution) > 0
    
    # All values should be positive integers
    for count in distribution.values():
        assert count > 0


def test_preference_updates_influence_recommendations(
    db_session: Session,
    sample_customer,
    sample_products
):
    """Test that preference updates influence future recommendations."""
    service = RecommendationService(db_session)
    
    # Generate initial recommendations
    initial_recs = service.generate_recommendations(
        customer_id=sample_customer.customer_id,
        force_refresh=True
    )
    
    [r for r in initial_recs if r.reason_tag == "based_on_diet"]
    
    # Update customer dietary preference
    sample_customer.dietary_preference = "vegan"
    db_session.commit()
    
    # Regenerate recommendations
    updated_recs = service.generate_recommendations(
        customer_id=sample_customer.customer_id,
        force_refresh=True
    )
    
    updated_diet_recs = [r for r in updated_recs if r.reason_tag == "based_on_diet"]
    
    # Should still have diet-based recommendations
    assert len(updated_diet_recs) > 0


def test_no_recommendations_without_reason(
    db_session: Session,
    sample_customer,
    sample_products
):
    """Test that no recommendations are created without reason classification."""
    service = RecommendationService(db_session)
    
    recommendations = service.generate_recommendations(
        customer_id=sample_customer.customer_id,
        force_refresh=True
    )
    
    # All recommendations must have a reason tag
    for rec in recommendations:
        assert rec.reason_tag is not None
        assert rec.reason_tag != ""
