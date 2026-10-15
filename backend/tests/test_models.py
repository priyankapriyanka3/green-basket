"""Tests for database models."""
from datetime import datetime


def test_models_import():
    """Test that all models can be imported successfully."""
    from app.models import (
        Address,
        AuditLog,
        Category,
        Customer,
        DeliveryAgent,
        DeliverySlot,
        Farmer,
        Inventory,
        Notification,
        Order,
        OrderDiscount,
        OrderItem,
        Payment,
        Product,
        Promotion,
        Recommendation,
        Review,
        ShoppingList,
        ShoppingListItem,
    )
    assert Customer is not None
    assert Address is not None
    assert Category is not None
    assert Product is not None
    assert Farmer is not None
    assert Inventory is not None
    assert ShoppingList is not None
    assert ShoppingListItem is not None
    assert Recommendation is not None
    assert Promotion is not None
    assert DeliverySlot is not None
    assert DeliveryAgent is not None
    assert Order is not None
    assert OrderItem is not None
    assert OrderDiscount is not None
    assert Payment is not None
    assert Review is not None
    assert Notification is not None
    assert AuditLog is not None


def test_customer_model_create(test_db):
    """Test creating a customer record."""
    from app.models import Customer
    
    customer = Customer(
        customer_id="cust-001",
        full_name="Test User",
        phone_number="+919876543210",
        email="test@example.com",
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )
    test_db.add(customer)
    test_db.commit()
    
    retrieved = test_db.query(Customer).filter_by(customer_id="cust-001").first()
    assert retrieved is not None
    assert retrieved.full_name == "Test User"
    assert retrieved.phone_number == "+919876543210"
