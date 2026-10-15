"""Review service layer with sentiment analysis."""
from datetime import datetime

from sqlalchemy.orm import Session

from app.errors import AppException
from app.models.order import Order, OrderItem
from app.models.review import Review


class ReviewService:
    """Review service with sentiment derivation."""
    
    def __init__(self, db: Session):
        """Initialize review service."""
        self.db = db
    
    def derive_sentiment(self, review_text: str, rating: int) -> str:
        """
        Derive sentiment from review text and rating.
        
        Sentiment analysis stub implementation:
        - Rating 4-5: positive
        - Rating 3: neutral
        - Rating 1-2: negative
        
        In production, this would use NLP/ML sentiment analysis.
        
        Args:
            review_text: Review text content
            rating: Numeric rating (1-5)
        
        Returns:
            Sentiment label: positive, neutral, or negative
        """
        # Rating-based sentiment analysis for MVP
        # Production would use NLP sentiment analysis on review_text
        # This implementation classifies based on rating thresholds
        if rating >= 4:
            return "positive"
        elif rating == 3:
            return "neutral"
        else:
            return "negative"
    
    def check_review_eligibility(self, order_id: str, customer_id: str, product_id: str) -> bool:
        """
        Check if customer can review product for this order.
        
        Rules:
        - Order must exist and belong to customer
        - Order must be fulfilled (confirmed, delivered, or eligible status)
        - Product must be in order items
        
        Args:
            order_id: Order identifier
            customer_id: Customer identifier
            product_id: Product identifier
        
        Returns:
            True if eligible, False otherwise
        """
        # Check order exists and belongs to customer
        order = self.db.query(Order).filter(
            Order.order_id == order_id,
            Order.customer_id == customer_id
        ).first()
        
        if not order:
            return False
        
        # Check order is eligible for review (confirmed or delivered)
        eligible_statuses = ["confirmed", "packed", "out_for_delivery", "delivered"]
        if order.status not in eligible_statuses:
            return False
        
        # Check product is in order items
        order_item = self.db.query(OrderItem).filter(
            OrderItem.order_id == order_id,
            OrderItem.product_id == product_id
        ).first()
        
        return order_item
    
    def submit_review(
        self,
        order_id: str,
        customer_id: str,
        product_id: str,
        rating: int,
        review_text: str | None = None
    ) -> Review:
        """
        Submit product review for order.
        
        Args:
            order_id: Order identifier
            customer_id: Customer identifier
            product_id: Product identifier
            rating: Rating (1-5)
            review_text: Optional review text
        
        Returns:
            Created review record
        
        Raises:
            AppException: If review not eligible (403 REVIEW_NOT_ELIGIBLE)
        """
        # Check eligibility
        if not self.check_review_eligibility(order_id, customer_id, product_id):
            raise AppException(
                code="REVIEW_NOT_ELIGIBLE",
                message="This order is not eligible for review",
                status_code=403
            )
        
        # Check for duplicate review
        existing_review = self.db.query(Review).filter(
            Review.order_id == order_id,
            Review.product_id == product_id,
            Review.customer_id == customer_id
        ).first()
        
        if existing_review:
            raise AppException(
                code="REVIEW_ALREADY_EXISTS",
                message="You have already reviewed this product for this order",
                status_code=409
            )
        
        # Derive sentiment
        sentiment = self.derive_sentiment(review_text or "", rating)
        
        # Generate review ID
        review_id = f"rev-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Create review record
        review = Review(
            review_id=review_id,
            order_id=order_id,
            product_id=product_id,
            customer_id=customer_id,
            rating=rating,
            review_text=review_text,
            sentiment=sentiment,
            reviewed_at=datetime.now().isoformat()
        )
        
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        
        return review
    
    def get_product_reviews(self, product_id: str, limit: int = 10) -> list[Review]:
        """
        Get reviews for a product.
        
        Args:
            product_id: Product identifier
            limit: Maximum number of reviews to return
        
        Returns:
            List of review records
        """
        reviews = self.db.query(Review).filter(
            Review.product_id == product_id
        ).order_by(Review.reviewed_at.desc()).limit(limit).all()
        
        return reviews
