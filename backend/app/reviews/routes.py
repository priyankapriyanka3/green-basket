"""Review API routes."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.reviews.schemas import ReviewResponse, ReviewSubmitRequest
from app.reviews.services import ReviewService

router = APIRouter()


@router.post("/{order_id}/reviews", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def submit_review(
    order_id: str,
    request: ReviewSubmitRequest,
    current_user: tuple = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit product review for order.
    
    Endpoint: POST /api/v1/orders/{orderId}/reviews
    
    Requirements:
    - Order must be fulfilled or eligible
    - Product must be in order
    - Customer must own order
    """
    customer, _role = current_user
    
    service = ReviewService(db)
    review = service.submit_review(
        order_id=order_id,
        customer_id=customer.customer_id,
        product_id=request.product_id,
        rating=request.rating,
        review_text=request.review_text
    )
    
    return ReviewResponse(
        review_id=review.review_id,
        order_id=review.order_id,
        product_id=review.product_id,
        customer_id=review.customer_id,
        rating=review.rating,
        review_text=review.review_text,
        sentiment=review.sentiment,
        reviewed_at=review.reviewed_at
    )
