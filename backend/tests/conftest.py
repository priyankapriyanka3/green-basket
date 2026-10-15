"""Pytest configuration and fixtures."""
from unittest.mock import Mock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base


@pytest.fixture
def test_db():
    """Create a test database."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(engine)


@pytest.fixture
def mock_db_session():
    """Mock database session for unit tests."""
    mock_session = Mock()
    mock_session.query.return_value = Mock()
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None
    return mock_session


@pytest.fixture
def sample_product():
    """Sample product for testing."""
    return Mock(
        product_id="prod-001",
        name="Fresh Bananas",
        unit_type="kg",
        unit_price=25.0,
        is_organic=False,
        status="active"
    )


@pytest.fixture
def sample_customer():
    """Sample customer for testing."""
    return Mock(
        customer_id="cust-001",
        full_name="Ananya Sharma",
        phone_number="+919876543210",
        loyalty_points=100,
        status="active"
    )


@pytest.fixture
def sample_address():
    """Sample serviceable address for testing."""
    return Mock(
        address_id="addr-001",
        customer_id="cust-001",
        label="Home",
        address_line1="123 Main St",
        city="Mumbai",
        state="Maharashtra",
        postal_code="400001",
        country="India",
        serviceability_status="serviceable",
        serviceability_reason=None
    )
