"""Integration test configuration."""
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.auth.services import create_access_token, hash_password
from app.database import Base, get_db
from app.main import app
from app.models.address import Address
from app.models.category import Category
from app.models.customer import Customer
from app.models.product import Product

# Create test engine with StaticPool to avoid threading issues
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Enable foreign key support for SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def override_get_db():
    """Override database dependency for tests."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override the app's database dependency
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Create test database schema once for all integration tests."""
    # Import all models to register with Base.metadata
    from app.models.address import Address
    from app.models.audit_log import AuditLog
    from app.models.category import Category
    from app.models.customer import Customer
    from app.models.delivery_agent import DeliveryAgent
    from app.models.delivery_slot import DeliverySlot
    from app.models.farmer import Farmer
    from app.models.inventory import Inventory
    from app.models.notification import Notification
    from app.models.order import Order, OrderDiscount, OrderItem
    from app.models.payment import Payment
    from app.models.product import Product
    from app.models.promotion import Promotion
    from app.models.recommendation import Recommendation
    from app.models.review import Review
    from app.models.shopping_list import ShoppingList, ShoppingListItem
    
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_db():
    """Provide database session for each test."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function", autouse=True)
def clean_db():
    """Clean database before each test."""
    # Delete all data in reverse dependency order
    from app.models.audit_log import AuditLog
    from app.models.delivery_agent import DeliveryAgent
    from app.models.delivery_slot import DeliverySlot
    from app.models.farmer import Farmer
    from app.models.inventory import Inventory
    from app.models.notification import Notification
    from app.models.order import Order, OrderDiscount, OrderItem
    from app.models.payment import Payment
    from app.models.promotion import Promotion
    from app.models.recommendation import Recommendation
    from app.models.review import Review
    from app.models.shopping_list import ShoppingList, ShoppingListItem
    
    db = TestingSessionLocal()
    try:
        # Temporarily disable foreign key checks for cleanup
        db.execute(text("PRAGMA foreign_keys=OFF"))
        
        db.query(AuditLog).delete()
        db.query(Notification).delete()
        db.query(OrderDiscount).delete()
        db.query(OrderItem).delete()
        db.query(Payment).delete()
        db.query(Order).delete()
        db.query(Promotion).delete()
        db.query(DeliverySlot).delete()
        db.query(ShoppingListItem).delete()
        db.query(ShoppingList).delete()
        db.query(Review).delete()
        db.query(Recommendation).delete()
        db.query(Inventory).delete()
        db.query(Address).delete()
        db.query(Product).delete()
        db.query(Farmer).delete()
        db.query(DeliveryAgent).delete()
        db.query(Category).delete()
        db.query(Customer).delete()
        db.commit()
        
        # Re-enable foreign key checks
        db.execute(text("PRAGMA foreign_keys=ON"))
        db.commit()
    finally:
        db.close()


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def test_customer(test_db):
    """Create test customer with hashed password."""
    hashed_pw = hash_password("password123")
    
    customer = Customer(
        customer_id="cust-test-001",
        full_name="Test Shopper",
        phone_number="+919876543210",
        email=hashed_pw,
        preferred_language="en",
        dietary_preference=None,
        allergies_json="[]",
        loyalty_points=0,
        status="active",
        created_at=datetime.now(UTC).isoformat(),
        updated_at=datetime.now(UTC).isoformat()
    )
    
    test_db.add(customer)
    test_db.commit()
    test_db.refresh(customer)
    
    return customer


@pytest.fixture
def test_operator(test_db):
    """Create test operator account."""
    hashed_pw = hash_password("operator123")
    
    operator = Customer(
        customer_id="cust-op-001",
        full_name="Test Operator",
        phone_number="+919123456789",
        email=hashed_pw,
        preferred_language="en",
        dietary_preference="role:operator",
        allergies_json="[]",
        loyalty_points=0,
        status="active",
        created_at=datetime.now(UTC).isoformat(),
        updated_at=datetime.now(UTC).isoformat()
    )
    
    test_db.add(operator)
    test_db.commit()
    test_db.refresh(operator)
    
    return operator


@pytest.fixture
def sample_customer(test_db):
    """Create sample customer for testing."""
    hashed_pw = hash_password("password123")
    now_iso = datetime.now(UTC).isoformat()
    
    customer = Customer(
        customer_id="cust-001",
        full_name="Ananya Sharma",
        phone_number="+919876543210",
        email=hashed_pw,
        preferred_language="en",
        dietary_preference="vegetarian",
        allergies_json='["peanuts"]',
        loyalty_points=420,
        status="active",
        created_at=now_iso,
        updated_at=now_iso
    )
    
    test_db.add(customer)
    test_db.commit()
    test_db.refresh(customer)
    
    return customer


@pytest.fixture
def sample_product(test_db):
    """Create sample product for testing."""
    now_iso = datetime.now(UTC).isoformat()
    
    # Create category first
    category = Category(
        category_id="cat-001",
        name="Fruits",
        description="Fresh fruits",
        is_active="true",
        created_at=now_iso,
        updated_at=now_iso
    )
    test_db.add(category)
    test_db.commit()
    
    product = Product(
        product_id="prod-001",
        category_id="cat-001",
        name="Fresh Bananas",
        description="Organic bananas from local farms",
        unit_type="kg",
        unit_price=25.0,
        is_organic="true",
        is_featured="false",
        tags_json='[]',
        nutrition_json='{}',
        created_at=now_iso,
        updated_at=now_iso
    )
    
    test_db.add(product)
    test_db.commit()
    test_db.refresh(product)
    
    return product


@pytest.fixture
def sample_address(test_db, sample_customer):
    """Create sample serviceable address for testing."""
    now_iso = datetime.now(UTC).isoformat()
    
    address = Address(
        address_id="addr-001",
        customer_id="cust-001",
        address_line1="123 Marine Drive",
        city="Mumbai",
        state="Maharashtra",
        postal_code="400001",
        country="India",
        latitude=18.9388,
        longitude=72.8354,
        is_default="true",
        serviceability_status="serviceable",
        serviceability_reason=None,
        created_at=now_iso,
        updated_at=now_iso
    )
    
    test_db.add(address)
    test_db.commit()
    test_db.refresh(address)
    
    return address


@pytest.fixture
def auth_token(sample_customer):
    """Create JWT token for authenticated requests."""
    token, _ = create_access_token(customer_id="cust-001", role="shopper")
    return token


@pytest.fixture
def test_db_session(test_db):
    """Alias for test_db to match test expectations."""
    return test_db


@pytest.fixture
def test_address_and_slot(test_db, sample_customer):
    """Create test address and delivery slot for orders."""
    from app.models.address import Address
    from app.models.delivery_slot import DeliverySlot
    
    address = Address(
        address_id="addr-test-001",
        customer_id="cust-001",
        address_line1="123 Test St",
        city="Mumbai",
        state="Maharashtra",
        postal_code="400001",
        country="India",
        is_default="true",
        serviceability_status="serviceable",
        created_at=datetime.now(UTC).isoformat(),
        updated_at=datetime.now(UTC).isoformat()
    )
    test_db.add(address)
    
    slot = DeliverySlot(
        slot_id="slt-test-001",
        slot_date="2026-10-16",
        start_time="09:00",
        end_time="11:00",
        label="Morning",
        max_capacity=100,
        reserved_count=10,
        is_available=1,
        service_zone="Mumbai-South",
        created_at=datetime.now(UTC).isoformat(),
        updated_at=datetime.now(UTC).isoformat()
    )
    test_db.add(slot)
    test_db.commit()
    
    return address, slot
