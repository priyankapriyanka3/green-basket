"""Payment service layer."""
from datetime import datetime

from sqlalchemy.orm import Session

from app.adapters.payment_provider import PaymentProviderAdapter
from app.errors import NotFoundError
from app.models.order import Order
from app.models.payment import Payment


class PaymentService:
    """Payment service with provider integration."""
    
    def __init__(self, db: Session):
        """Initialize payment service."""
        self.db = db
        self.payment_adapter = PaymentProviderAdapter(db=db)
    
    def initiate_payment(
        self,
        order_id: str,
        payment_method: str,
        amount: str,
        currency: str,
        customer_context: dict,
        callback_url: str | None = None
    ) -> Payment:
        """
        Initiate payment with external provider.
        
        Args:
            order_id: Order identifier
            payment_method: Payment method (upi, card, netbanking)
            amount: Payment amount
            currency: Currency code
            customer_context: Customer metadata
            callback_url: Callback URL for payment status
        
        Returns:
            Payment record with initiated status
        """
        # Call payment provider adapter
        provider_response = self.payment_adapter.create_intent(
            order_id=order_id,
            amount=amount,
            currency=currency,
            payment_method=payment_method,
            customer_context=customer_context,
            callback_url=callback_url or "https://api.greenbasket.ai/payments/callback"
        )
        
        # Generate payment ID
        payment_id = f"pay-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Create payment record (stores transaction_reference only, no card details)
        payment = Payment(
            payment_id=payment_id,
            order_id=order_id,
            payment_method=payment_method,
            status="initiated",
            amount=float(amount),
            transaction_reference=provider_response["transaction_reference"],
            payment_date=datetime.now().isoformat(),
        )
        
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        
        return payment
    
    def get_payment_status(self, payment_id: str) -> Payment:
        """
        Get payment status by payment ID.
        
        Args:
            payment_id: Payment identifier
        
        Returns:
            Payment record
        """
        payment = self.db.query(Payment).filter(Payment.payment_id == payment_id).first()
        if not payment:
            raise NotFoundError("Payment not found")
        
        return payment
    
    def reconcile_payment(self, transaction_reference: str) -> Payment:
        """
        Reconcile payment status with provider.
        
        Args:
            transaction_reference: Transaction reference from provider
        
        Returns:
            Updated payment record
        """
        payment = self.db.query(Payment).filter(
            Payment.transaction_reference == transaction_reference
        ).first()
        
        if not payment:
            raise NotFoundError("Payment not found for transaction reference")
        
        # Fetch status from provider
        provider_status = self.payment_adapter.fetch_status(transaction_reference)
        
        # Update payment status
        payment.status = provider_status["provider_status"]
        payment.payment_date = datetime.now().isoformat()
        
        # Update order status if payment successful
        if payment.status == "paid":
            order = self.db.query(Order).filter(Order.order_id == payment.order_id).first()
            if order and order.status == "payment_pending":
                order.status = "confirmed"
                order.confirmed_at = datetime.now().isoformat()
        
        self.db.commit()
        self.db.refresh(payment)
        
        return payment
