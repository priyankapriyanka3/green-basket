"""Integration tests for review routes."""
from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.auth.services import create_access_token
from app.main import app
from app.models.category import Category
from app.models.customer import Customer
from app.models.order import Order, OrderItem
from app.models.product import Product

client = TestClient(app)


class TestReviewRoutes:
    """Test review API routes."""
    
    def test_submit_review_for_fulfilled_order(self, test_db, sample_customer, sample_address, auth_token):
        """Customer can submit review for fulfilled order."""
        # sample_customer and sample_address fixtures already created customer and address
        
        # Create delivery slot
        from app.models.delivery_slot import DeliverySlot
        slot = DeliverySlot(
            slot_id="slt-001",
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
        
        category = Category(
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            category_id="cat-001",
            name="Fruits",
            # is_featured removed - read-only property
        )
        test_db.add(category)
        
        now_iso = datetime.now(UTC).isoformat()
        product = Product(
            product_id="prod-001",
            category_id="cat-001",
            name="Organic Bananas",
            unit_type="1 dozen",
            unit_price=65.00,
            is_organic="true",
            is_featured="false",
            tags_json="[]",
            nutrition_json="{}",
            created_at=now_iso,
            updated_at=now_iso
        )
        test_db.add(product)
        
        order = Order(
            order_id="ord-001",
            customer_id="cust-001",
            address_id="addr-001",
            slot_id="slt-001",
            status="delivered",
            subtotal=65.00,
            discount_amount=0.00,
            loyalty_redeemed_amount=0.00,
            final_amount=65.00,
            order_date=datetime.now().isoformat(),
            confirmed_at=datetime.now().isoformat()
        )
        test_db.add(order)
        test_db.flush()  # Ensure order is inserted before order_item
        
        order_item = OrderItem(
            item_id="item-001",
            order_id="ord-001",
            product_id="prod-001",
            quantity=1,
            unit_price=65.00,
            total_price=65.00
        )
        test_db.add(order_item)
        test_db.commit()
        
        # Submit review
        response = client.post(
            "/api/v1/orders/ord-001/reviews",
            json={
                "product_id": "prod-001",
                "rating": 5,
                "review_text": "Fresh and ripe bananas delivered on time."
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["order_id"] == "ord-001"
        assert data["product_id"] == "prod-001"
        assert data["rating"] == 5
        assert data["sentiment"] == "positive"
        assert data["review_text"] == "Fresh and ripe bananas delivered on time."
    
    def test_review_not_eligible_for_unfulfilled_order(self, test_db):
        """403 REVIEW_NOT_ELIGIBLE for unfulfilled orders."""
        # Create test data
        customer = Customer(
            customer_id="cust-002",
            full_name="Test Customer",
            phone_number="+919876543211",
            preferred_language="en-IN",
            dietary_preference="vegetarian",
            allergies_json="[]",
            loyalty_points=100,
            status="active",
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        test_db.add(customer)
        test_db.commit()
        test_db.commit()
        
        # Create address for the order
        from app.models.address import Address
        address = Address(
            address_id="addr-002",
            customer_id="cust-002",
            address_line1="456 Test St",
            city="Mumbai",
            state="Maharashtra",
            postal_code="400002",
            country="India",
            is_default="true",
            serviceability_status="serviceable",
            created_at=datetime.now(UTC).isoformat(),
            updated_at=datetime.now(UTC).isoformat()
        )
        test_db.add(address)
        
        # Create delivery slot for the order
        from app.models.delivery_slot import DeliverySlot
        slot = DeliverySlot(
            slot_id="slt-002",
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
        
        category = Category(
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            category_id="cat-002",
            name="Vegetables",
            # is_featured removed - read-only property
        )
        test_db.add(category)
        
        now_iso = datetime.now(UTC).isoformat()
        product = Product(
            product_id="prod-002",
            category_id="cat-002",
            name="Spinach",
            unit_type="1 bunch",
            unit_price=30.00,
            is_organic="true",
            is_featured="false",
            tags_json="[]",
            nutrition_json="{}",
            created_at=now_iso,
            updated_at=now_iso
            
        )
        test_db.add(product)
        test_db.flush()
        
        order = Order(
            order_id="ord-002",
            customer_id="cust-002",
            address_id="addr-002",
            slot_id="slt-002",
            status="payment_pending",  # Not fulfilled
            subtotal=30.00,
            discount_amount=0.00,
            loyalty_redeemed_amount=0.00,
            final_amount=30.00,
            order_date=datetime.now().isoformat()
        )
        test_db.add(order)
        test_db.flush()
        
        order_item = OrderItem(
            item_id="item-002",
            order_id="ord-002",
            product_id="prod-002",
            quantity=1,
            unit_price=30.00,
            total_price=30.00
        )
        test_db.add(order_item)
        test_db.commit()
        
        # Generate token for cust-002
        # AuthService not needed
        token, _ = create_access_token(customer_id="cust-002", role="shopper")
        
        # Attempt to submit review
        response = client.post(
            "/api/v1/orders/ord-002/reviews",
            json={
                "product_id": "prod-002",
                "rating": 4,
                "review_text": "Good quality."
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 403
        assert response.json()["error"]["code"] == "REVIEW_NOT_ELIGIBLE"
    
    def test_sentiment_derived_from_review_text(self, test_db, auth_token):
        """Sentiment is derived from review text and rating."""
        # Create test data
        customer = Customer(
            customer_id="cust-003",
            full_name="Test Customer",
            phone_number="+919876543212",
            preferred_language="en-IN",
            dietary_preference="vegetarian",
            allergies_json="[]",
            loyalty_points=100,
            status="active",
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        test_db.add(customer)
        test_db.commit()
        
        # Create address for the order
        from app.models.address import Address
        address = Address(
            address_id="addr-003",
            customer_id="cust-003",
            address_line1="789 Test St",
            city="Mumbai",
            state="Maharashtra",
            postal_code="400003",
            country="India",
            is_default="true",
            serviceability_status="serviceable",
            created_at=datetime.now(UTC).isoformat(),
            updated_at=datetime.now(UTC).isoformat()
        )
        test_db.add(address)
        
        # Create delivery slot for the order
        from app.models.delivery_slot import DeliverySlot
        slot = DeliverySlot(
            slot_id="slt-003",
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
        
        category = Category(
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            category_id="cat-003",
            name="Dairy",
            # is_featured removed - read-only property
        )
        test_db.add(category)
        
        now_iso = datetime.now(UTC).isoformat()
        product = Product(
            product_id="prod-003",
            category_id="cat-003",
            name="Milk",
            unit_type="1 liter",
            unit_price=60.00,
            is_organic="true",
            is_featured="false",
            tags_json="[]",
            nutrition_json="{}",
            created_at=now_iso,
            updated_at=now_iso
            
        )
        test_db.add(product)
        test_db.flush()
        
        order = Order(
            order_id="ord-003",
            customer_id="cust-003",
            address_id="addr-003",
            slot_id="slt-003",
            status="delivered",
            subtotal=60.00,
            discount_amount=0.00,
            loyalty_redeemed_amount=0.00,
            final_amount=60.00,
            order_date=datetime.now().isoformat(),
            confirmed_at=datetime.now().isoformat()
        )
        test_db.add(order)
        test_db.flush()
        
        order_item = OrderItem(
            item_id="item-003",
            order_id="ord-003",
            product_id="prod-003",
            quantity=1,
            unit_price=60.00,
            total_price=60.00
        )
        test_db.add(order_item)
        test_db.commit()
        
        # Generate token for cust-003
        # AuthService not needed
        token, _ = create_access_token(customer_id="cust-003", role="shopper")
        
        # Test positive sentiment (rating 5)
        response = client.post(
            "/api/v1/orders/ord-003/reviews",
            json={
                "product_id": "prod-003",
                "rating": 5,
                "review_text": "Excellent quality milk."
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 201
        assert response.json()["sentiment"] == "positive"
    
    def test_sentiment_neutral_for_rating_3(self, test_db):
        """Sentiment is neutral for rating 3."""
        # Create test data
        customer = Customer(
            customer_id="cust-004",
            full_name="Test Customer",
            phone_number="+919876543213",
            preferred_language="en-IN",
            dietary_preference="vegetarian",
            allergies_json="[]",
            loyalty_points=100,
            status="active",
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        test_db.add(customer)
        test_db.commit()
        
        # Create address for the order
        from app.models.address import Address
        address = Address(
            address_id="addr-004",
            customer_id="cust-004",
            address_line1="101 Test St",
            city="Mumbai",
            state="Maharashtra",
            postal_code="400004",
            country="India",
            is_default="true",
            serviceability_status="serviceable",
            created_at=datetime.now(UTC).isoformat(),
            updated_at=datetime.now(UTC).isoformat()
        )
        test_db.add(address)
        
        # Create delivery slot for the order
        from app.models.delivery_slot import DeliverySlot
        slot = DeliverySlot(
            slot_id="slt-004",
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
        
        category = Category(
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            category_id="cat-004",
            name="Grains",
            # is_featured removed - read-only property
        )
        test_db.add(category)
        
        now_iso = datetime.now(UTC).isoformat()
        product = Product(
            product_id="prod-004",
            category_id="cat-004",
            name="Rice",
            unit_type="1 kg",
            unit_price=80.00,
            is_organic="true",
            is_featured="false",
            tags_json="[]",
            nutrition_json="{}",
            created_at=now_iso,
            updated_at=now_iso
            
        )
        test_db.add(product)
        test_db.flush()
        
        order = Order(
            order_id="ord-004",
            customer_id="cust-004",
            address_id="addr-004",
            slot_id="slt-004",
            status="delivered",
            subtotal=80.00,
            discount_amount=0.00,
            loyalty_redeemed_amount=0.00,
            final_amount=80.00,
            order_date=datetime.now().isoformat(),
            confirmed_at=datetime.now().isoformat()
        )
        test_db.add(order)
        test_db.flush()
        
        order_item = OrderItem(
            item_id="item-004",
            order_id="ord-004",
            product_id="prod-004",
            quantity=1,
            unit_price=80.00,
            total_price=80.00
        )
        test_db.add(order_item)
        test_db.commit()
        
        # Generate token for cust-004
        # AuthService not needed
        token, _ = create_access_token(customer_id="cust-004", role="shopper")
        
        # Test neutral sentiment (rating 3)
        response = client.post(
            "/api/v1/orders/ord-004/reviews",
            json={
                "product_id": "prod-004",
                "rating": 3,
                "review_text": "Average quality."
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 201
        assert response.json()["sentiment"] == "neutral"
    
    def test_sentiment_negative_for_low_rating(self, test_db):
        """Sentiment is negative for rating 1-2."""
        # Create test data
        customer = Customer(
            customer_id="cust-005",
            full_name="Test Customer",
            phone_number="+919876543214",
            preferred_language="en-IN",
            dietary_preference="vegetarian",
            allergies_json="[]",
            loyalty_points=100,
            status="active",
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        test_db.add(customer)
        test_db.commit()
        
        # Create address for the order
        from app.models.address import Address
        address = Address(
            address_id="addr-005",
            customer_id="cust-005",
            address_line1="202 Test St",
            city="Mumbai",
            state="Maharashtra",
            postal_code="400005",
            country="India",
            is_default="true",
            serviceability_status="serviceable",
            created_at=datetime.now(UTC).isoformat(),
            updated_at=datetime.now(UTC).isoformat()
        )
        test_db.add(address)
        
        # Create delivery slot for the order
        from app.models.delivery_slot import DeliverySlot
        slot = DeliverySlot(
            slot_id="slt-005",
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
        
        category = Category(
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            category_id="cat-005",
            name="Snacks",
            # is_featured removed - read-only property
        )
        test_db.add(category)
        
        now_iso = datetime.now(UTC).isoformat()
        product = Product(
            product_id="prod-005",
            category_id="cat-005",
            name="Chips",
            unit_type="200g",
            unit_price=50.00,
            is_organic="true",
            is_featured="false",
            tags_json="[]",
            nutrition_json="{}",
            created_at=now_iso,
            updated_at=now_iso
            
        )
        test_db.add(product)
        test_db.flush()
        
        order = Order(
            order_id="ord-005",
            customer_id="cust-005",
            address_id="addr-005",
            slot_id="slt-005",
            status="delivered",
            subtotal=50.00,
            discount_amount=0.00,
            loyalty_redeemed_amount=0.00,
            final_amount=50.00,
            order_date=datetime.now().isoformat(),
            confirmed_at=datetime.now().isoformat()
        )
        test_db.add(order)
        test_db.flush()
        
        order_item = OrderItem(
            item_id="item-005",
            order_id="ord-005",
            product_id="prod-005",
            quantity=1,
            unit_price=50.00,
            total_price=50.00
        )
        test_db.add(order_item)
        test_db.commit()
        
        # Generate token for cust-005
        # AuthService not needed
        token, _ = create_access_token(customer_id="cust-005", role="shopper")
        
        # Test negative sentiment (rating 2)
        response = client.post(
            "/api/v1/orders/ord-005/reviews",
            json={
                "product_id": "prod-005",
                "rating": 2,
                "review_text": "Not fresh, disappointed."
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 201
        assert response.json()["sentiment"] == "negative"
