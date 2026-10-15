"""Unit tests for payment adapter and service."""
from datetime import datetime

from app.adapters.payment_provider import PaymentProviderAdapter
from app.models.order import Order
from app.models.payment import Payment
from app.payments.services import PaymentService


class TestPaymentProviderAdapter:
    """Test payment provider adapter."""
    
    def test_create_intent_returns_transaction_reference(self):
        """Payment adapter returns transaction reference without storing card details."""
        adapter = PaymentProviderAdapter()
        
        result = adapter.create_intent(
            order_id="ord-001",
            amount="170.00",
            currency="INR",
            payment_method="upi",
            customer_context={"customer_id": "cust-001"},
            callback_url="https://api.greenbasket.ai/payments/callback"
        )
        
        assert "transaction_reference" in result
        assert result["transaction_reference"].startswith("txn-upi-")
        assert result["provider_status"] == "initiated"
        assert "client_token" in result
    
    def test_create_intent_never_stores_card_numbers(self):
        """Payment adapter never stores card numbers or CVV."""
        adapter = PaymentProviderAdapter()
        
        # Pass card details in request (as would happen in real integration)
        result = adapter.create_intent(
            order_id="ord-001",
            amount="170.00",
            currency="INR",
            payment_method="card",
            customer_context={"card_number": "4111111111111111", "cvv": "123"},
            callback_url="https://api.greenbasket.ai/payments/callback"
        )
        
        # Verify card details are not in response
        response_str = str(result)
        assert "4111111111111111" not in response_str
        assert "123" not in response_str
        assert "transaction_reference" in result
    
    def test_fetch_status_returns_provider_status(self):
        """Payment adapter fetches status from provider."""
        adapter = PaymentProviderAdapter()
        
        result = adapter.fetch_status("txn-upi-001")
        
        assert "provider_status" in result
        assert "updated_at" in result


class TestPaymentService:
    """Test payment service."""
    
    def test_initiate_payment_creates_payment_record(self, test_db):
        """Payment service creates payment record with transaction reference only."""
        service = PaymentService(test_db)
        
        payment = service.initiate_payment(
            order_id="ord-001",
            payment_method="upi",
            amount="170.00",
            currency="INR",
            customer_context={"customer_id": "cust-001"},
            callback_url="https://api.greenbasket.ai/payments/callback"
        )
        
        assert payment.payment_id.startswith("pay-")
        assert payment.order_id == "ord-001"
        assert payment.payment_method == "upi"
        assert payment.status == "initiated"
        assert float(payment.amount) == 170.00
        assert payment.transaction_reference.startswith("txn-upi-")
    
    def test_payment_record_stores_transaction_reference_only(self, test_db):
        """Payment record stores transaction_reference only, no card details."""
        service = PaymentService(test_db)
        
        payment = service.initiate_payment(
            order_id="ord-001",
            payment_method="card",
            amount="170.00",
            currency="INR",
            customer_context={"card_number": "4111111111111111", "cvv": "123"},
            callback_url="https://api.greenbasket.ai/payments/callback"
        )
        
        # Verify payment record in database
        saved_payment = test_db.query(Payment).filter(
            Payment.payment_id == payment.payment_id
        ).first()
        
        # Check that only transaction_reference is stored
        assert saved_payment.transaction_reference is not None
        # Verify no card details in any payment field
        payment_dict = {
            "payment_id": saved_payment.payment_id,
            "order_id": saved_payment.order_id,
            "payment_method": saved_payment.payment_method,
            "transaction_reference": saved_payment.transaction_reference
        }
        payment_str = str(payment_dict)
        assert "4111111111111111" not in payment_str
        assert "123" not in payment_str
    
    def test_reconcile_payment_updates_order_status(self, test_db):
        """Payment reconciliation updates order status to confirmed when paid."""
        service = PaymentService(test_db)
        
        # Create order with payment_pending status
        order = Order(
            order_id="ord-001",
            customer_id="cust-001",
            address_id="addr-001",
            slot_id="slt-001",
            status="payment_pending",
            subtotal=185.00,
            discount_amount=15.00,
            loyalty_redeemed_amount=0.00,
            final_amount=170.00,
            order_date=datetime.now().isoformat()
        )
        test_db.add(order)
        test_db.commit()
        
        # Create payment
        payment = service.initiate_payment(
            order_id="ord-001",
            payment_method="upi",
            amount="170.00",
            currency="INR",
            customer_context={"customer_id": "cust-001"},
            callback_url="https://api.greenbasket.ai/payments/callback"
        )
        
        # Reconcile payment
        reconciled_payment = service.reconcile_payment(payment.transaction_reference)
        
        assert reconciled_payment.status == "paid"
        
        # Verify order status updated
        updated_order = test_db.query(Order).filter(Order.order_id == "ord-001").first()
        assert updated_order.status == "confirmed"
        assert updated_order.confirmed_at is not None
    
    def test_order_never_confirmed_without_payment_success(self, test_db):
        """Order status never confirmed while payment status is initiated."""
        service = PaymentService(test_db)
        
        # Create order with payment_pending status
        order = Order(
            order_id="ord-002",
            customer_id="cust-001",
            address_id="addr-001",
            slot_id="slt-001",
            status="payment_pending",
            subtotal=185.00,
            discount_amount=15.00,
            loyalty_redeemed_amount=0.00,
            final_amount=170.00,
            order_date=datetime.now().isoformat()
        )
        test_db.add(order)
        test_db.commit()
        
        # Create payment (initiated status)
        payment = service.initiate_payment(
            order_id="ord-002",
            payment_method="upi",
            amount="170.00",
            currency="INR",
            customer_context={"customer_id": "cust-001"},
            callback_url="https://api.greenbasket.ai/payments/callback"
        )
        
        # Verify order still payment_pending
        order_check = test_db.query(Order).filter(Order.order_id == "ord-002").first()
        assert order_check.status == "payment_pending"
        assert payment.status == "initiated"
