"""Simple integration tests for review routes."""
from datetime import datetime

from fastapi.testclient import TestClient

from app.main import app
from app.models.order import Order, OrderItem

client = TestClient(app)


class TestReviewRoutesSimple:
    """Simple test review API routes."""
    
    def test_submit_review_for_fulfilled_order(self, test_db, sample_customer, sample_product, auth_token, test_address_and_slot):
        """Customer can submit review for fulfilled order."""
        address, slot = test_address_and_slot
        
        # Create fulfilled order with product
        order = Order(
            order_id="ord-rev-001",
            customer_id="cust-001",
            address_id=address.address_id,
            slot_id=slot.slot_id,
            status="delivered",
            subtotal=25.00,
            discount_amount=0.00,
            loyalty_redeemed_amount=0.00,
            final_amount=25.00,
            order_date=datetime.now().isoformat(),
            confirmed_at=datetime.now().isoformat()
        )
        test_db.add(order)
        
        order_item = OrderItem(
            item_id="item-rev-001",
            order_id="ord-rev-001",
            product_id="prod-001",
            quantity=1,
            unit_price=25.00,
            total_price=25.00
        )
        test_db.add(order_item)
        test_db.commit()
        
        # Submit review
        response = client.post(
            "/api/v1/orders/ord-rev-001/reviews",
            json={
                "product_id": "prod-001",
                "rating": 5,
                "review_text": "Fresh and ripe bananas delivered on time."
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["order_id"] == "ord-rev-001"
        assert data["product_id"] == "prod-001"
        assert data["rating"] == 5
        assert data["sentiment"] == "positive"
    
    def test_review_not_eligible_for_pending_order(self, test_db, sample_customer, sample_product, auth_token, test_address_and_slot):
        address, slot = test_address_and_slot
        
        """403 REVIEW_NOT_ELIGIBLE for pending orders."""
        # Create payment_pending order
        order = Order(
            order_id="ord-rev-002",
            customer_id="cust-001",
            address_id=address.address_id,
            slot_id=slot.slot_id,
            status="payment_pending",
            subtotal=25.00,
            discount_amount=0.00,
            loyalty_redeemed_amount=0.00,
            final_amount=25.00,
            order_date=datetime.now().isoformat()
        )
        test_db.add(order)
        
        order_item = OrderItem(
            item_id="item-rev-002",
            order_id="ord-rev-002",
            product_id="prod-001",
            quantity=1,
            unit_price=25.00,
            total_price=25.00
        )
        test_db.add(order_item)
        test_db.commit()
        
        # Attempt to submit review
        response = client.post(
            "/api/v1/orders/ord-rev-002/reviews",
            json={
                "product_id": "prod-001",
                "rating": 5,
                "review_text": "Good."
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert response.status_code == 403
        assert response.json()["error"]["code"] == "REVIEW_NOT_ELIGIBLE"
    
    def test_sentiment_derived_positive(self, test_db, sample_customer, sample_product, auth_token, test_address_and_slot):
        address, slot = test_address_and_slot
        
        """Positive sentiment for rating 4-5."""
        order = Order(
            order_id="ord-rev-003",
            customer_id="cust-001",
            address_id=address.address_id,
            slot_id=slot.slot_id,
            status="delivered",
            subtotal=25.00,
            discount_amount=0.00,
            loyalty_redeemed_amount=0.00,
            final_amount=25.00,
            order_date=datetime.now().isoformat(),
            confirmed_at=datetime.now().isoformat()
        )
        test_db.add(order)
        
        order_item = OrderItem(
            item_id="item-rev-003",
            order_id="ord-rev-003",
            product_id="prod-001",
            quantity=1,
            unit_price=25.00,
            total_price=25.00
        )
        test_db.add(order_item)
        test_db.commit()
        
        response = client.post(
            "/api/v1/orders/ord-rev-003/reviews",
            json={
                "product_id": "prod-001",
                "rating": 4,
                "review_text": "Great quality."
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert response.status_code == 201
        assert response.json()["sentiment"] == "positive"
    
    def test_sentiment_derived_neutral(self, test_db, sample_customer, sample_product, auth_token, test_address_and_slot):
        address, slot = test_address_and_slot
        
        """Neutral sentiment for rating 3."""
        order = Order(
            order_id="ord-rev-004",
            customer_id="cust-001",
            address_id=address.address_id,
            slot_id=slot.slot_id,
            status="delivered",
            subtotal=25.00,
            discount_amount=0.00,
            loyalty_redeemed_amount=0.00,
            final_amount=25.00,
            order_date=datetime.now().isoformat(),
            confirmed_at=datetime.now().isoformat()
        )
        test_db.add(order)
        
        order_item = OrderItem(
            item_id="item-rev-004",
            order_id="ord-rev-004",
            product_id="prod-001",
            quantity=1,
            unit_price=25.00,
            total_price=25.00
        )
        test_db.add(order_item)
        test_db.commit()
        
        response = client.post(
            "/api/v1/orders/ord-rev-004/reviews",
            json={
                "product_id": "prod-001",
                "rating": 3,
                "review_text": "Average quality."
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert response.status_code == 201
        assert response.json()["sentiment"] == "neutral"
    
    def test_sentiment_derived_negative(self, test_db, sample_customer, sample_product, auth_token, test_address_and_slot):
        address, slot = test_address_and_slot
        
        """Negative sentiment for rating 1-2."""
        order = Order(
            order_id="ord-rev-005",
            customer_id="cust-001",
            address_id=address.address_id,
            slot_id=slot.slot_id,
            status="delivered",
            subtotal=25.00,
            discount_amount=0.00,
            loyalty_redeemed_amount=0.00,
            final_amount=25.00,
            order_date=datetime.now().isoformat(),
            confirmed_at=datetime.now().isoformat()
        )
        test_db.add(order)
        
        order_item = OrderItem(
            item_id="item-rev-005",
            order_id="ord-rev-005",
            product_id="prod-001",
            quantity=1,
            unit_price=25.00,
            total_price=25.00
        )
        test_db.add(order_item)
        test_db.commit()
        
        response = client.post(
            "/api/v1/orders/ord-rev-005/reviews",
            json={
                "product_id": "prod-001",
                "rating": 2,
                "review_text": "Not fresh."
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert response.status_code == 201
        assert response.json()["sentiment"] == "negative"
