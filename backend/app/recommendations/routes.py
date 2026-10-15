"""Recommendation routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.customer import Customer
from app.recommendations.schemas import ProductRecommendationCard
from app.recommendations.services import RecommendationService

router = APIRouter(prefix="/api/v1/recommendations", tags=["recommendations"])


@router.get("/", response_model=list[ProductRecommendationCard])
def get_recommendations(
    limit: int = 10,
    force_refresh: bool = False,
    current_user: tuple[Customer, str] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized recommendations for the current customer."""
    customer, _role = current_user
    service = RecommendationService(db)
    
    # Generate recommendations if needed
    if force_refresh:
        service.generate_recommendations(
            customer_id=customer.customer_id,
            force_refresh=True
        )
    else:
        # Check if recommendations exist, generate if not
        existing = service.get_customer_recommendations(
            customer_id=customer.customer_id,
            limit=1
        )
        if not existing:
            service.generate_recommendations(
                customer_id=customer.customer_id,
                force_refresh=False
            )
    
    # Return recommendations with product details
    return service.get_customer_recommendations(
        customer_id=customer.customer_id,
        limit=limit
    )


@router.get("/reason-distribution")
def get_reason_distribution(
    current_user: tuple[Customer, str] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get recommendation reason distribution for operations reporting."""
    # This endpoint could be restricted to operator role
    service = RecommendationService(db)
    return service.get_reason_distribution()
