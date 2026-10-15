"""Unit tests for catalog module."""
from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.catalog.services import CatalogService
from app.database import Base
from app.models.category import Category
from app.models.farmer import Farmer
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.review import Review


@pytest.fixture
def session():
    """Create test database session."""
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
def sample_category(session):
    """Create sample category."""
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).isoformat()
    category = Category(
        category_id="cat-001",
        name="Fresh Fruits",
        description="Farm-fresh fruits",
        parent_category_id=None,
        icon_url="https://example.com/fruits.svg",
        is_featured=1,
        created_at=now,
        updated_at=now,
    )
    session.add(category)
    session.commit()
    return category


@pytest.fixture
def sample_farmer(session):
    """Create sample farmer."""
    from datetime import UTC, datetime
    now_iso = datetime.now(UTC).isoformat()
    farmer = Farmer(
        farmer_id="frm-001",
        name="Sahyadri Farms",
        location="Nashik, Maharashtra",
        certification_type="organic",
        rating=4.5,
        created_at=now_iso,
        updated_at=now_iso
    )
    session.add(farmer)
    session.commit()
    return farmer


@pytest.fixture
def sample_product(session, sample_category, sample_farmer):
    """Create sample product."""
    from datetime import UTC, datetime
    now_iso = datetime.now(UTC).isoformat()
    product = Product(
        product_id="prod-001",
        category_id=sample_category.category_id,
        farmer_id=sample_farmer.farmer_id,
        name="Organic Bananas",
        description="Fresh organic bananas",
        unit_type="1 dozen",
        unit_price=65.00,
        is_organic="true",
        is_featured="false",
        tags_json='["fruit", "breakfast"]',
        nutrition_json='{"calories": 89, "potassiumMg": 358}',
        created_at=now_iso,
        updated_at=now_iso
    )
    session.add(product)
    session.commit()
    return product


@pytest.fixture
def sample_inventory(session, sample_product):
    """Create sample inventory."""
    now = datetime.now(UTC)
    harvest_date = now - timedelta(days=1)
    expiry_date = now + timedelta(days=3)
    
    inventory = Inventory(
        inventory_id="inv-001",
        product_id=sample_product.product_id,
        stock_quantity=50,
        reorder_level=10,
        harvest_date=harvest_date.isoformat() + "Z",
        expiry_date=expiry_date.isoformat() + "Z",
        warehouse_zone="Mumbai-South",
        last_updated_at=now.isoformat() + "Z",
        availability_status="available",
    )
    session.add(inventory)
    session.commit()
    return inventory


def test_get_featured_categories(session, sample_category):
    """Test retrieving featured categories."""
    service = CatalogService(session)
    categories = service.get_featured_categories()
    
    assert len(categories) == 1
    assert categories[0].category_id == "cat-001"
    assert categories[0].name == "Fresh Fruits"
    assert categories[0].is_featured is True


def test_search_products_basic(session, sample_product):
    """Test basic product search without filters."""
    service = CatalogService(session)
    result = service.search_products()
    
    assert result.total == 1
    assert len(result.products) == 1
    assert result.products[0].product_id == "prod-001"
    assert result.products[0].name == "Organic Bananas"


def test_search_products_by_keyword(session, sample_product):
    """Test product search with keyword."""
    service = CatalogService(session)
    
    # Search by name
    result = service.search_products(q="Bananas")
    assert result.total == 1
    assert result.products[0].product_id == "prod-001"
    
    # Search by description
    result = service.search_products(q="organic")
    assert result.total == 1
    
    # No match
    result = service.search_products(q="Apples")
    assert result.total == 0


def test_search_products_by_category(session, sample_product, sample_category):
    """Test product search filtered by category."""
    service = CatalogService(session)
    
    result = service.search_products(category_id="cat-001")
    assert result.total == 1
    assert result.products[0].product_id == "prod-001"
    
    result = service.search_products(category_id="cat-999")
    assert result.total == 0


def test_search_products_by_organic_flag(session, sample_product):
    """Test product search filtered by organic status."""
    service = CatalogService(session)
    
    # Filter organic products
    result = service.search_products(is_organic=True)
    assert result.total == 1
    assert result.products[0].is_organic is True
    
    # Filter non-organic products
    result = service.search_products(is_organic=False)
    assert result.total == 0


def test_search_products_featured_only(session, sample_product, sample_category):
    """Test product search filtered by featured status."""
    # Add featured product
    from datetime import UTC, datetime
    now_iso = datetime.now(UTC).isoformat()
    featured_product = Product(
        product_id="prod-002",
        category_id=sample_category.category_id,
        name="Featured Apples",
        unit_type="1 kg",
        unit_price=120.00,
        is_organic="false",
        is_featured="true",
        tags_json="[]",
        nutrition_json="{}",
        created_at=now_iso,
        updated_at=now_iso
    )
    session.add(featured_product)
    session.commit()
    
    service = CatalogService(session)
    
    # Get all products
    result = service.search_products()
    assert result.total == 2
    
    # Get featured only
    result = service.search_products(featured_only=True)
    assert result.total == 1
    assert result.products[0].product_id == "prod-002"
    assert result.products[0].is_featured is True


def test_search_products_pagination(session, sample_category):
    """Test product search pagination."""
    from datetime import UTC, datetime
    now_iso = datetime.now(UTC).isoformat()
    # Create multiple products
    for i in range(5):
        product = Product(
            product_id=f"prod-{i:03d}",
            category_id=sample_category.category_id,
            name=f"Product {i}",
            unit_type="1 unit",
            unit_price=100.00,
            is_organic="false",
            is_featured="false",
            tags_json="[]",
            nutrition_json="{}",
            created_at=now_iso,
            updated_at=now_iso
        )
        session.add(product)
    session.commit()
    
    service = CatalogService(session)
    
    # Page 1
    result = service.search_products(page=1, page_size=2)
    assert result.total == 5
    assert len(result.products) == 2
    assert result.page == 1
    assert result.page_size == 2
    
    # Page 2
    result = service.search_products(page=2, page_size=2)
    assert result.total == 5
    assert len(result.products) == 2
    assert result.page == 2


def test_product_card_includes_nutrition(session, sample_product, sample_inventory):
    """Test that product card includes parsed nutrition data."""
    service = CatalogService(session)
    result = service.search_products()
    
    product_card = result.products[0]
    assert product_card.nutrition is not None
    assert product_card.nutrition.calories == 89
    assert product_card.nutrition.potassium_mg == 358


def test_product_card_includes_freshness(session, sample_product, sample_inventory):
    """Test that product card includes freshness data from inventory."""
    service = CatalogService(session)
    result = service.search_products()
    
    product_card = result.products[0]
    assert product_card.freshness is not None
    assert product_card.freshness.stock_quantity == 50
    assert product_card.freshness.availability_status == "available"
    assert product_card.freshness.harvest_date is not None
    assert product_card.freshness.expiry_date is not None


def test_freshness_calculation_expiry_days(session, sample_product):
    """Test freshness indicator calculation with expiry date."""
    now = datetime.now(UTC)
    expiry_soon = now + timedelta(days=1)
    
    inventory = Inventory(
        inventory_id="inv-002",
        product_id=sample_product.product_id,
        stock_quantity=10,
        reorder_level=5,
        expiry_date=expiry_soon.isoformat() + "Z",
        warehouse_zone="Test",
        last_updated_at=now.isoformat() + "Z",
        availability_status="available",
    )
    session.add(inventory)
    session.commit()
    
    service = CatalogService(session)
    result = service.search_products()
    
    product_card = result.products[0]
    assert product_card.freshness is not None
    assert product_card.freshness.expiry_days is not None
    assert product_card.freshness.expiry_days <= 1


def test_product_card_includes_farmer_info(session, sample_product, sample_inventory, sample_farmer):
    """Test that product card includes farmer information."""
    service = CatalogService(session)
    result = service.search_products()
    
    product_card = result.products[0]
    assert product_card.farmer is not None
    assert product_card.farmer.farmer_id == "frm-001"
    assert product_card.farmer.name == "Sahyadri Farms"
    assert product_card.farmer.is_verified is True
    assert product_card.farmer.is_organic_certified is True


def test_product_card_includes_review_summary(session, sample_product, sample_inventory):
    """Test that product card includes review summary."""
    # Add sample reviews
    customer_id = "cust-001"
    order_id = "ord-001"
    
    reviews = [
        Review(
            review_id="rev-001",
            order_id=order_id,
            product_id=sample_product.product_id,
            customer_id=customer_id,
            rating=5,
            review_text="Great bananas!",
            sentiment="positive",
            reviewed_at=datetime.now(UTC).isoformat() + "Z",
        ),
        Review(
            review_id="rev-002",
            order_id=order_id,
            product_id=sample_product.product_id,
            customer_id=customer_id,
            rating=4,
            review_text="Good quality",
            sentiment="positive",
            reviewed_at=datetime.now(UTC).isoformat() + "Z",
        ),
    ]
    for review in reviews:
        session.add(review)
    session.commit()
    
    service = CatalogService(session)
    result = service.search_products()
    
    product_card = result.products[0]
    assert product_card.review_summary is not None
    assert product_card.review_summary.review_count == 2
    assert product_card.review_summary.average_rating == 4.5
    assert product_card.review_summary.sentiment == "positive"


def test_get_low_stock_products(session, sample_product, sample_category):
    """Test operational low stock monitoring."""
    # Create low stock inventory
    now = datetime.now(UTC)
    inventory = Inventory(
        inventory_id="inv-low",
        product_id=sample_product.product_id,
        stock_quantity=5,
        reorder_level=10,
        warehouse_zone="Mumbai-South",
        last_updated_at=now.isoformat() + "Z",
        availability_status="low_stock",
    )
    session.add(inventory)
    session.commit()
    
    service = CatalogService(session)
    low_stock = service.get_low_stock_products()
    
    assert len(low_stock) == 1
    assert low_stock[0]["product_id"] == sample_product.product_id
    assert low_stock[0]["availability_status"] == "low_stock"


def test_product_tags_parsed_from_json(session, sample_product, sample_inventory):
    """Test that product tags are correctly parsed from JSON."""
    service = CatalogService(session)
    result = service.search_products()
    
    product_card = result.products[0]
    assert product_card.tags == ["fruit", "breakfast"]


def test_combined_filters(session, sample_product, sample_category):
    """Test combining multiple filters."""
    service = CatalogService(session)
    
    # Combine category + organic + keyword
    result = service.search_products(
        q="Bananas",
        category_id="cat-001",
        is_organic=True,
    )
    assert result.total == 1
    assert result.products[0].product_id == "prod-001"
    
    # Filters that don't match
    result = service.search_products(
        q="Bananas",
        category_id="cat-001",
        is_organic=False,
    )
    assert result.total == 0
