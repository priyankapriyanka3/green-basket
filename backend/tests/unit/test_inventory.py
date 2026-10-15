"""Unit tests for inventory module."""
from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.inventory.services import InventoryService
from app.models.category import Category
from app.models.inventory import Inventory
from app.models.product import Product


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
    now = datetime.now(UTC).isoformat()
    category = Category(
        category_id="cat-001",
        name="Fresh Fruits",
        description="Farm-fresh fruits",
        is_featured=1,
        created_at=now,
        updated_at=now,
    )
    session.add(category)
    session.commit()
    return category


@pytest.fixture
def sample_product(session, sample_category):
    """Create sample product."""
    now = datetime.now(UTC).isoformat()
    product = Product(
        product_id="prod-001",
        category_id=sample_category.category_id,
        name="Organic Bananas",
        description="Fresh organic bananas",
        unit_type="dozen",
        unit_price=65.00,
        is_organic="true",
        is_featured="false",
        tags_json="[]",
        nutrition_json="{}",
        created_at=now,
        updated_at=now,
    )
    session.add(product)
    session.commit()
    return product


def test_get_inventory_status(session, sample_product):
    """Test retrieving inventory status."""
    now = datetime.now(UTC)
    harvest_date = now - timedelta(days=1)
    expiry_date = now + timedelta(days=3)
    
    inventory = Inventory(
        inventory_id="inv-001",
        product_id=sample_product.product_id,
        stock_quantity=50,
        reorder_level=10,
        harvest_date=harvest_date.isoformat().replace('+00:00', 'Z'),
        expiry_date=expiry_date.isoformat().replace('+00:00', 'Z'),
        warehouse_zone="Mumbai-South",
        last_updated_at=now.isoformat().replace('+00:00', 'Z'),
        availability_status="available",
    )
    session.add(inventory)
    session.commit()
    
    service = InventoryService(session)
    status = service.get_inventory_status(sample_product.product_id)
    
    assert status is not None
    assert status.inventory_id == "inv-001"
    assert status.stock_quantity == 50
    assert status.reorder_level == 10
    assert status.availability_status == "available"
    assert status.harvest_date is not None
    assert status.expiry_date is not None


def test_update_availability_status_available(session, sample_product):
    """Test updating availability status to available."""
    now = datetime.now(UTC)
    inventory = Inventory(
        inventory_id="inv-001",
        product_id=sample_product.product_id,
        stock_quantity=15,
        reorder_level=10,
        warehouse_zone="Mumbai-South",
        last_updated_at=now.isoformat().replace("+00:00", "Z"),
        availability_status="low_stock",
    )
    session.add(inventory)
    session.commit()
    
    service = InventoryService(session)
    
    # Update stock above reorder level
    service.update_availability_status(sample_product.product_id, stock_quantity=20)
    
    # Verify status changed to available
    updated_inventory = session.query(Inventory).filter_by(product_id=sample_product.product_id).first()
    assert updated_inventory.stock_quantity == 20
    assert updated_inventory.availability_status == "available"


def test_update_availability_status_low_stock(session, sample_product):
    """Test updating availability status to low_stock."""
    now = datetime.now(UTC)
    inventory = Inventory(
        inventory_id="inv-001",
        product_id=sample_product.product_id,
        stock_quantity=50,
        reorder_level=10,
        warehouse_zone="Mumbai-South",
        last_updated_at=now.isoformat().replace("+00:00", "Z"),
        availability_status="available",
    )
    session.add(inventory)
    session.commit()
    
    service = InventoryService(session)
    
    # Update stock to at or below reorder level
    service.update_availability_status(sample_product.product_id, stock_quantity=8)
    
    # Verify status changed to low_stock
    updated_inventory = session.query(Inventory).filter_by(product_id=sample_product.product_id).first()
    assert updated_inventory.stock_quantity == 8
    assert updated_inventory.availability_status == "low_stock"


def test_update_availability_status_unavailable(session, sample_product):
    """Test updating availability status to unavailable."""
    now = datetime.now(UTC)
    inventory = Inventory(
        inventory_id="inv-001",
        product_id=sample_product.product_id,
        stock_quantity=5,
        reorder_level=10,
        warehouse_zone="Mumbai-South",
        last_updated_at=now.isoformat().replace("+00:00", "Z"),
        availability_status="low_stock",
    )
    session.add(inventory)
    session.commit()
    
    service = InventoryService(session)
    
    # Update stock to zero
    service.update_availability_status(sample_product.product_id, stock_quantity=0)
    
    # Verify status changed to unavailable
    updated_inventory = session.query(Inventory).filter_by(product_id=sample_product.product_id).first()
    assert updated_inventory.stock_quantity == 0
    assert updated_inventory.availability_status == "unavailable"


def test_get_low_stock_alerts(session, sample_category):
    """Test retrieving low stock alerts."""
    now = datetime.now(UTC)
    
    # Create products with varying stock levels
    products = []
    now_iso = datetime.now(UTC).isoformat()
    for i in range(3):
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
        products.append(product)
    
    # Create inventory records
    inventories = [
        # Low stock
        Inventory(
            inventory_id="inv-000",
            product_id=products[0].product_id,
            stock_quantity=5,
            reorder_level=10,
            warehouse_zone="Mumbai-South",
            last_updated_at=now.isoformat().replace("+00:00", "Z"),
            availability_status="low_stock",
        ),
        # Available (above reorder level)
        Inventory(
            inventory_id="inv-001",
            product_id=products[1].product_id,
            stock_quantity=50,
            reorder_level=10,
            warehouse_zone="Mumbai-Central",
            last_updated_at=now.isoformat().replace("+00:00", "Z"),
            availability_status="available",
        ),
        # Unavailable
        Inventory(
            inventory_id="inv-002",
            product_id=products[2].product_id,
            stock_quantity=0,
            reorder_level=10,
            warehouse_zone="Bengaluru-North",
            last_updated_at=now.isoformat().replace("+00:00", "Z"),
            availability_status="unavailable",
        ),
    ]
    for inventory in inventories:
        session.add(inventory)
    session.commit()
    
    service = InventoryService(session)
    alerts = service.get_low_stock_alerts()
    
    # Should return low_stock and unavailable items
    assert len(alerts) == 2
    alert_statuses = [alert.availability_status for alert in alerts]
    assert "low_stock" in alert_statuses
    assert "unavailable" in alert_statuses


def test_get_expiry_alerts(session, sample_category):
    """Test retrieving expiry alerts."""
    now = datetime.now(UTC)
    
    # Create products with varying expiry dates
    products = []
    now_iso = datetime.now(UTC).isoformat()
    for i in range(4):
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
        products.append(product)
    
    # Create inventory records with different expiry dates
    inventories = [
        # Expiring in 1 day (urgent)
        Inventory(
            inventory_id="inv-000",
            product_id=products[0].product_id,
            stock_quantity=10,
            reorder_level=5,
            expiry_date=(now + timedelta(days=1)).isoformat().replace("+00:00", "Z"),
            warehouse_zone="Mumbai-South",
            last_updated_at=now.isoformat().replace("+00:00", "Z"),
            availability_status="available",
        ),
        # Expiring in 5 days
        Inventory(
            inventory_id="inv-001",
            product_id=products[1].product_id,
            stock_quantity=20,
            reorder_level=5,
            expiry_date=(now + timedelta(days=5)).isoformat().replace("+00:00", "Z"),
            warehouse_zone="Mumbai-Central",
            last_updated_at=now.isoformat().replace("+00:00", "Z"),
            availability_status="available",
        ),
        # Expiring in 10 days (beyond threshold)
        Inventory(
            inventory_id="inv-002",
            product_id=products[2].product_id,
            stock_quantity=30,
            reorder_level=5,
            expiry_date=(now + timedelta(days=10)).isoformat().replace("+00:00", "Z"),
            warehouse_zone="Bengaluru-North",
            last_updated_at=now.isoformat().replace("+00:00", "Z"),
            availability_status="available",
        ),
        # No expiry date
        Inventory(
            inventory_id="inv-003",
            product_id=products[3].product_id,
            stock_quantity=40,
            reorder_level=5,
            expiry_date=None,
            warehouse_zone="Bengaluru-South",
            last_updated_at=now.isoformat().replace("+00:00", "Z"),
            availability_status="available",
        ),
    ]
    for inventory in inventories:
        session.add(inventory)
    session.commit()
    
    service = InventoryService(session)
    
    # Get alerts with 7-day threshold
    alerts = service.get_expiry_alerts(days_threshold=7)
    
    # Should return items expiring within 7 days
    assert len(alerts) == 2
    
    # Should be sorted by urgency (days until expiry)
    assert alerts[0].days_until_expiry <= alerts[1].days_until_expiry


def test_calculate_freshness_indicator_unavailable(session, sample_product):
    """Test freshness indicator for unavailable products."""
    now = datetime.now(UTC)
    inventory = Inventory(
        inventory_id="inv-001",
        product_id=sample_product.product_id,
        stock_quantity=0,
        reorder_level=10,
        warehouse_zone="Mumbai-South",
        last_updated_at=now.isoformat().replace("+00:00", "Z"),
        availability_status="unavailable",
    )
    session.add(inventory)
    session.commit()
    
    service = InventoryService(session)
    text, color = service.calculate_freshness_indicator(inventory)
    
    assert text == "Unavailable"
    assert color == "grey"


def test_calculate_freshness_indicator_low_stock(session, sample_product):
    """Test freshness indicator for low stock products."""
    now = datetime.now(UTC)
    inventory = Inventory(
        inventory_id="inv-001",
        product_id=sample_product.product_id,
        stock_quantity=3,
        reorder_level=10,
        warehouse_zone="Mumbai-South",
        last_updated_at=now.isoformat().replace("+00:00", "Z"),
        availability_status="low_stock",
    )
    session.add(inventory)
    session.commit()
    
    service = InventoryService(session)
    text, color = service.calculate_freshness_indicator(inventory)
    
    assert "Low stock: 3 left" == text
    assert color == "marigold"


def test_calculate_freshness_indicator_expiring_soon(session, sample_product):
    """Test freshness indicator for expiring products."""
    now = datetime.now(UTC)
    expiry_date = now + timedelta(days=1)
    
    inventory = Inventory(
        inventory_id="inv-001",
        product_id=sample_product.product_id,
        stock_quantity=20,
        reorder_level=10,
        expiry_date=expiry_date.isoformat().replace("+00:00", "Z"),
        warehouse_zone="Mumbai-South",
        last_updated_at=now.isoformat().replace("+00:00", "Z"),
        availability_status="available",
    )
    session.add(inventory)
    session.commit()
    
    service = InventoryService(session)
    text, color = service.calculate_freshness_indicator(inventory)
    
    assert "Expires in" in text
    assert color == "marigold"


def test_calculate_freshness_indicator_fresh_harvest(session, sample_product):
    """Test freshness indicator for recently harvested products."""
    now = datetime.now(UTC)
    harvest_date = now - timedelta(days=1)
    expiry_date = now + timedelta(days=4)
    
    inventory = Inventory(
        inventory_id="inv-001",
        product_id=sample_product.product_id,
        stock_quantity=50,
        reorder_level=10,
        harvest_date=harvest_date.isoformat().replace("+00:00", "Z"),
        expiry_date=expiry_date.isoformat().replace("+00:00", "Z"),
        warehouse_zone="Mumbai-South",
        last_updated_at=now.isoformat().replace("+00:00", "Z"),
        availability_status="available",
    )
    session.add(inventory)
    session.commit()
    
    service = InventoryService(session)
    text, color = service.calculate_freshness_indicator(inventory)
    
    assert "Harvested" in text
    assert "best within" in text
    assert color == "green"
