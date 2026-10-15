"""Payment API routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.payments.schemas import PaymentStatusResponse
from app.payments.services import PaymentService

router = APIRouter()


@router.get("/{payment_id}", response_model=PaymentStatusResponse)
def get_payment_status(
    payment_id: str,
    db: Session = Depends(get_db)
):
    """Get payment status by payment ID."""
    service = PaymentService(db)
    payment = service.get_payment_status(payment_id)
    
    return PaymentStatusResponse(
        payment_id=payment.payment_id,
        order_id=payment.order_id,
        status=payment.status,
        transaction_reference=payment.transaction_reference,
        amount=str(payment.amount),
        currency="INR",
        payment_date=payment.payment_date,
        updated_at=payment.payment_date
    )
