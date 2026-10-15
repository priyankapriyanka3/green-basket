"""Unit tests for address module."""
from datetime import UTC, datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.addresses.schemas import AddressCreateRequest, AddressUpdateRequest
from app.addresses.services import AddressService
from app.database import Base
from app.errors import AppException
from app.models.customer import Customer


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
def sample_customer(session):
    """Create sample customer."""
    customer = Customer(
        customer_id="cust-001",
        full_name="Ananya Sharma",
        phone_number="+919876543210",
        preferred_language="en-IN",
        dietary_preference="vegetarian",
        allergies_json='["peanut"]',
        loyalty_points=420,
        status="active",
        created_at=datetime.now(UTC).isoformat() + "Z",
        updated_at=datetime.now(UTC).isoformat() + "Z",
    )
    session.add(customer)
    session.commit()
    return customer


def test_check_serviceability_mumbai_postal_code(session):
    """Test serviceability check for Mumbai postal codes."""
    service = AddressService(session)
    
    # Valid Mumbai postal code
    result = service.check_serviceability("400001")
    assert result.is_serviceable is True
    assert result.service_zone == "Mumbai-400001"
    assert result.reason == "supported_postal_code"


def test_check_serviceability_bengaluru_postal_code(session):
    """Test serviceability check for Bengaluru postal codes."""
    service = AddressService(session)
    
    # Valid Bengaluru postal code
    result = service.check_serviceability("560001")
    assert result.is_serviceable is True
    assert result.service_zone == "Bengaluru-560001"
    assert result.reason == "supported_postal_code"


def test_check_serviceability_unsupported_postal_code(session):
    """Test serviceability check rejects unsupported postal codes."""
    service = AddressService(session)
    
    # Delhi postal code (not supported)
    result = service.check_serviceability("110001")
    assert result.is_serviceable is False
    assert result.service_zone is None
    assert result.reason == "unsupported_postal_code"


def test_check_serviceability_with_coordinates_valid(session):
    """Test coordinate-aware serviceability validation."""
    service = AddressService(session)
    
    # Mumbai postal code with valid Mumbai coordinates
    result = service.check_serviceability(
        postal_code="400001",
        latitude=18.9388,
        longitude=72.8354,
    )
    assert result.is_serviceable is True
    assert result.service_zone == "Mumbai-400001"


def test_check_serviceability_with_coordinates_invalid(session):
    """Test coordinate-aware validation rejects out-of-bounds coordinates."""
    service = AddressService(session)
    
    # Mumbai postal code but Bengaluru coordinates
    result = service.check_serviceability(
        postal_code="400001",
        latitude=12.9716,
        longitude=77.5946,
    )
    assert result.is_serviceable is False
    assert result.reason == "coordinates_outside_service_area"


def test_create_address_serviceable(session, sample_customer):
    """Test creating a serviceable address."""
    service = AddressService(session)
    
    data = AddressCreateRequest(
        label="Home",
        street="123 MG Road",
        city="Mumbai",
        state="Maharashtra",
        postal_code="400001",
        country="India",
        latitude=18.9388,
        longitude=72.8354,
        is_default=True,
    )
    
    address = service.create_address(sample_customer.customer_id, data)
    
    assert address.address_id.startswith("addr-")
    assert address.customer_id == sample_customer.customer_id
    assert address.label == "Home"
    assert address.postal_code == "400001"
    assert address.is_default is True
    assert address.serviceability.is_serviceable is True
    assert address.serviceability.service_zone == "Mumbai-400001"


def test_create_address_not_serviceable(session, sample_customer):
    """Test creating an unserviceable address is allowed but marked."""
    service = AddressService(session)
    
    data = AddressCreateRequest(
        label="Work",
        street="456 Brigade Road",
        city="Delhi",
        state="Delhi",
        postal_code="110001",
        country="India",
        is_default=False,
    )
    
    address = service.create_address(sample_customer.customer_id, data)
    
    assert address.address_id.startswith("addr-")
    assert address.serviceability.is_serviceable is False
    assert address.serviceability.reason == "unsupported_postal_code"


def test_create_address_sets_default(session, sample_customer):
    """Test creating address with is_default clears other defaults."""
    service = AddressService(session)
    
    # Create first address as default
    data1 = AddressCreateRequest(
        label="Home",
        street="123 MG Road",
        city="Mumbai",
        state="Maharashtra",
        postal_code="400001",
        is_default=True,
    )
    address1 = service.create_address(sample_customer.customer_id, data1)
    assert address1.is_default is True
    
    # Create second address as default
    data2 = AddressCreateRequest(
        label="Office",
        street="456 BKC",
        city="Mumbai",
        state="Maharashtra",
        postal_code="400051",
        is_default=True,
    )
    address2 = service.create_address(sample_customer.customer_id, data2)
    assert address2.is_default is True
    
    # Verify first address is no longer default
    addresses = service.list_addresses(sample_customer.customer_id)
    addr1_updated = next(a for a in addresses if a.address_id == address1.address_id)
    assert addr1_updated.is_default is False


def test_list_addresses(session, sample_customer):
    """Test listing customer addresses."""
    service = AddressService(session)
    
    # Create multiple addresses
    for i in range(3):
        data = AddressCreateRequest(
            label=f"Address {i+1}",
            street=f"{i+1}23 Street",
            city="Mumbai",
            state="Maharashtra",
            postal_code="400001",
        )
        service.create_address(sample_customer.customer_id, data)
    
    addresses = service.list_addresses(sample_customer.customer_id)
    assert len(addresses) == 3


def test_get_address(session, sample_customer):
    """Test getting specific address."""
    service = AddressService(session)
    
    # Create address
    data = AddressCreateRequest(
        label="Home",
        street="123 Street",
        city="Mumbai",
        state="Maharashtra",
        postal_code="400001",
    )
    created = service.create_address(sample_customer.customer_id, data)
    
    # Retrieve address
    address = service.get_address(created.address_id, sample_customer.customer_id)
    assert address.address_id == created.address_id
    assert address.label == "Home"


def test_get_address_not_found(session, sample_customer):
    """Test getting non-existent address raises exception."""
    service = AddressService(session)
    
    with pytest.raises(AppException) as exc_info:
        service.get_address("addr-999", sample_customer.customer_id)
    
    assert exc_info.value.code == "ADDRESS_NOT_FOUND"
    assert exc_info.value.status_code == 404


def test_update_address(session, sample_customer):
    """Test updating address fields."""
    service = AddressService(session)
    
    # Create address
    data = AddressCreateRequest(
        label="Home",
        street="123 Street",
        city="Mumbai",
        state="Maharashtra",
        postal_code="400001",
    )
    address = service.create_address(sample_customer.customer_id, data)
    
    # Update address
    update_data = AddressUpdateRequest(
        label="Updated Home",
        street="456 New Street",
    )
    updated = service.update_address(address.address_id, sample_customer.customer_id, update_data)
    
    assert updated.label == "Updated Home"
    assert updated.street == "456 New Street"
    assert updated.city == "Mumbai"  # Unchanged


def test_update_address_postal_code_revalidates(session, sample_customer):
    """Test updating postal code triggers serviceability revalidation."""
    service = AddressService(session)
    
    # Create serviceable address
    data = AddressCreateRequest(
        label="Home",
        street="123 Street",
        city="Mumbai",
        state="Maharashtra",
        postal_code="400001",
    )
    address = service.create_address(sample_customer.customer_id, data)
    assert address.serviceability.is_serviceable is True
    
    # Update to unsupported postal code
    update_data = AddressUpdateRequest(
        postal_code="110001",  # Delhi
    )
    updated = service.update_address(address.address_id, sample_customer.customer_id, update_data)
    
    assert updated.postal_code == "110001"
    assert updated.serviceability.is_serviceable is False


def test_update_address_make_default(session, sample_customer):
    """Test updating address to make it default."""
    service = AddressService(session)
    
    # Create two addresses
    data1 = AddressCreateRequest(
        label="Home",
        street="123 Street",
        city="Mumbai",
        state="Maharashtra",
        postal_code="400001",
        is_default=True,
    )
    address1 = service.create_address(sample_customer.customer_id, data1)
    
    data2 = AddressCreateRequest(
        label="Office",
        street="456 Street",
        city="Mumbai",
        state="Maharashtra",
        postal_code="400051",
        is_default=False,
    )
    address2 = service.create_address(sample_customer.customer_id, data2)
    
    # Make address2 default
    update_data = AddressUpdateRequest(is_default=True)
    updated = service.update_address(address2.address_id, sample_customer.customer_id, update_data)
    
    assert updated.is_default is True
    
    # Verify address1 is no longer default
    addr1_updated = service.get_address(address1.address_id, sample_customer.customer_id)
    assert addr1_updated.is_default is False


def test_delete_address(session, sample_customer):
    """Test deleting address."""
    service = AddressService(session)
    
    # Create address
    data = AddressCreateRequest(
        label="Home",
        street="123 Street",
        city="Mumbai",
        state="Maharashtra",
        postal_code="400001",
    )
    address = service.create_address(sample_customer.customer_id, data)
    
    # Delete address
    service.delete_address(address.address_id, sample_customer.customer_id)
    
    # Verify deleted
    with pytest.raises(AppException) as exc_info:
        service.get_address(address.address_id, sample_customer.customer_id)
    
    assert exc_info.value.code == "ADDRESS_NOT_FOUND"


def test_postal_code_validation(session, sample_customer):
    """Test postal code validation in address creation."""
    AddressService(session)
    
    # Invalid postal code (not 6 digits)
    with pytest.raises(ValueError):
        AddressCreateRequest(
            label="Home",
            street="123 Street",
            city="Mumbai",
            state="Maharashtra",
            postal_code="12345",  # Only 5 digits
        )
