"""Integration tests for catalog API routes."""
from datetime import UTC, datetime, timedelta

import pytest

from app.models.category import Category
from app.models.farmer import Farmer
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.review import Review


@pytest.fixture
def sample_data(test_db):
    """Create sample catalog data."""
    # Create category
    now_iso = datetime.now(UTC).isoformat()
    category = Category(
        category_id="cat-001",
        name="Fresh Fruits",
        description="Farm-fresh fruits",
        parent_category_id=None,
        icon_url="https://example.com/fruits.svg",
        is_featured=1,
        created_at=now_iso,
        updated_at=now_iso,
    )
    test_db.add(category)
    
    # Create farmer
    farmer = Farmer(
        farmer_id="frm-001",
        name="Sahyadri Farms",
        location="Nashik, Maharashtra",
        certification_type="organic",
        rating=4.5,
        created_at=datetime.now(UTC).isoformat(),
        updated_at=datetime.now(UTC).isoformat()
    )
    test_db.add(farmer)
    
    # Create products
    products = [
        Product(
            product_id="prod-001",
            category_id="cat-001",
            farmer_id="frm-001",
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
        ),
        Product(
            product_id="prod-002",
            category_id="cat-001",
            farmer_id="frm-001",
            name="Fresh Apples",
            description="Crisp red apples",
            unit_type="1 kg",
            unit_price=120.00,
            is_organic="false",
            is_featured="true",
            tags_json='["fruit", "snack"]',
            nutrition_json='{"calories": 52}',
            created_at=now_iso,
            updated_at=now_iso
        ),
        Product(
            product_id="prod-003",
            category_id="cat-001",
            name="Organic Grapes",
            description="Seedless green grapes",
            unit_type="500g",
            unit_price=85.00,
            is_organic="true",
            is_featured="false",
            tags_json='["fruit"]',
            nutrition_json='{}',
            created_at=now_iso,
            updated_at=now_iso
        ),
    ]
    for product in products:
        test_db.add(product)
    test_db.commit()
    
    # Create inventory
    now = datetime.now(UTC)
    inventories = [
        Inventory(
            inventory_id="inv-001",
            product_id="prod-001",
            stock_quantity=50,
            reorder_level=10,
            harvest_date=(now - timedelta(days=1)).isoformat() + "Z",
            expiry_date=(now + timedelta(days=3)).isoformat() + "Z",
            warehouse_zone="Mumbai-South",
            last_updated_at=now.isoformat() + "Z",
            availability_status="available",
        ),
        Inventory(
            inventory_id="inv-002",
            product_id="prod-002",
            stock_quantity=8,
            reorder_level=10,
            warehouse_zone="Mumbai-Central",
            last_updated_at=now.isoformat() + "Z",
            availability_status="low_stock",
        ),
        Inventory(
            inventory_id="inv-003",
            product_id="prod-003",
            stock_quantity=30,
            reorder_level=5,
            warehouse_zone="Bengaluru-North",
            last_updated_at=now.isoformat() + "Z",
            availability_status="available",
        ),
    ]
    for inventory in inventories:
        test_db.add(inventory)
    test_db.commit()
    
    # Note: Reviews not created here as they require orders and customers


def test_get_products_basic(client, test_db, sample_data):
    """Test basic product listing."""
    response = client.get("/api/v1/catalog/products")
    assert response.status_code == 200
    
    data = response.json()
    assert "categories" in data
    assert "products" in data
    assert "total" in data
    assert data["total"] == 3
    assert len(data["products"]) == 3


def test_get_products_with_keyword_search(client, test_db, sample_data):
    """Test product search with keyword."""
    # Search for "Bananas"
    response = client.get("/api/v1/catalog/products?q=Bananas")
    assert response.status_code == 200
    
    data = response.json()
    assert data["total"] == 1
    assert data["products"][0]["name"] == "Organic Bananas"
    
    # Search for "organic" (matches description)
    response = client.get("/api/v1/catalog/products?q=organic")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2  # Bananas and Grapes


def test_get_products_filter_by_category(client, test_db, sample_data):
    """Test product filtering by category."""
    response = client.get("/api/v1/catalog/products?categoryId=cat-001")
    assert response.status_code == 200
    
    data = response.json()
    assert data["total"] == 3
    
    # Non-existent category
    response = client.get("/api/v1/catalog/products?categoryId=cat-999")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0


def test_get_products_filter_by_organic(client, test_db, sample_data):
    """Test product filtering by organic status."""
    # Filter organic products
    response = client.get("/api/v1/catalog/products?isOrganic=true")
    assert response.status_code == 200
    
    data = response.json()
    assert data["total"] == 2  # Bananas and Grapes
    for product in data["products"]:
        assert product["isOrganic"] is True
    
    # Filter non-organic products
    response = client.get("/api/v1/catalog/products?isOrganic=false")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1  # Apples
    assert data["products"][0]["isOrganic"] is False


def test_get_products_filter_featured_only(client, test_db, sample_data):
    """Test product filtering by featured status."""
    response = client.get("/api/v1/catalog/products?featuredOnly=true")
    assert response.status_code == 200
    
    data = response.json()
    assert data["total"] == 1
    assert data["products"][0]["name"] == "Fresh Apples"
    assert data["products"][0]["isFeatured"] is True


def test_get_products_pagination(client, test_db, sample_data):
    """Test product pagination."""
    # Page 1 with 2 items
    response = client.get("/api/v1/catalog/products?page=1&pageSize=2")
    assert response.status_code == 200
    
    data = response.json()
    assert data["total"] == 3
    assert len(data["products"]) == 2
    assert data["page"] == 1
    assert data["pageSize"] == 2
    
    # Page 2
    response = client.get("/api/v1/catalog/products?page=2&pageSize=2")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert len(data["products"]) == 1
    assert data["page"] == 2


def test_product_includes_nutrition_data(client, test_db, sample_data):
    """Test that product response includes nutrition data."""
    response = client.get("/api/v1/catalog/products?q=Bananas")
    assert response.status_code == 200
    
    data = response.json()
    product = data["products"][0]
    
    assert "nutrition" in product
    assert product["nutrition"] is not None
    assert product["nutrition"]["calories"] == 89
    assert product["nutrition"]["potassiumMg"] == 358


def test_product_includes_freshness_data(client, test_db, sample_data):
    """Test that product response includes freshness data."""
    response = client.get("/api/v1/catalog/products?q=Bananas")
    assert response.status_code == 200
    
    data = response.json()
    product = data["products"][0]
    
    assert "freshness" in product
    assert product["freshness"] is not None
    assert product["freshness"]["stockQuantity"] == 50
    assert product["freshness"]["availabilityStatus"] == "available"
    assert "harvestDate" in product["freshness"]
    assert "expiryDate" in product["freshness"]


def test_product_includes_review_summary(client, test_db, sample_data):
    """Test that product response includes reviewSummary field."""
    response = client.get("/api/v1/catalog/products?q=Bananas")
    assert response.status_code == 200
    
    data = response.json()
    product = data["products"][0]
    
    # reviewSummary field should be present (None when no reviews exist)
    assert "reviewSummary" in product


def test_product_includes_farmer_info(client, test_db, sample_data):
    """Test that product response includes farmer information."""
    response = client.get("/api/v1/catalog/products?q=Bananas")
    assert response.status_code == 200
    
    data = response.json()
    product = data["products"][0]
    
    assert "farmer" in product
    assert product["farmer"] is not None
    assert product["farmer"]["farmerId"] == "frm-001"
    assert product["farmer"]["name"] == "Sahyadri Farms"
    assert product["farmer"]["isVerified"] is True
    assert product["farmer"]["isOrganicCertified"] is True


def test_product_price_format(client, test_db, sample_data):
    """Test that product prices are correctly formatted."""
    response = client.get("/api/v1/catalog/products")
    assert response.status_code == 200
    
    data = response.json()
    for product in data["products"]:
        assert "priceInr" in product
        # Should be formatted as decimal string
        price = float(product["priceInr"])
        assert price > 0


def test_combine_multiple_filters(client, test_db, sample_data):
    """Test combining multiple filters."""
    # Combine keyword + category + organic
    response = client.get(
        "/api/v1/catalog/products?q=organic&categoryId=cat-001&isOrganic=true"
    )
    assert response.status_code == 200
    
    data = response.json()
    assert data["total"] == 2  # Bananas and Grapes
    
    # Conflicting filters (no match)
    response = client.get(
        "/api/v1/catalog/products?q=Apples&isOrganic=true"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0


def test_featured_categories_in_response(client, test_db, sample_data):
    """Test that response includes featured categories."""
    response = client.get("/api/v1/catalog/products")
    assert response.status_code == 200
    
    data = response.json()
    assert "categories" in data
    assert len(data["categories"]) >= 1
    
    category = data["categories"][0]
    assert category["categoryId"] == "cat-001"
    assert category["name"] == "Fresh Fruits"
    assert category["isFeatured"] is True


def test_availability_status_reflected(client, test_db, sample_data):
    """Test that low stock status is correctly reflected."""
    response = client.get("/api/v1/catalog/products?q=Apples")
    assert response.status_code == 200
    
    data = response.json()
    product = data["products"][0]
    
    assert product["freshness"]["availabilityStatus"] == "low_stock"
    assert product["freshness"]["stockQuantity"] == 8
