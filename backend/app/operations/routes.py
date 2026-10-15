"""Operations API routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import require_operator
from app.database import get_db
from app.operations.schemas import OpsSummaryResponse
from app.operations.services import OperationsService

router = APIRouter(prefix="/api/v1/operations", tags=["operations"])


@router.get("/summary", response_model=OpsSummaryResponse)
def get_operations_summary(
    current_user: tuple = Depends(require_operator),
    db: Session = Depends(get_db)
):
    """Get operations summary KPIs (operator role only).
    
    Returns:
        OpsSummaryResponse with open slot alerts, promotion warnings, and negative sentiment product counts.
    """
    service = OperationsService(db)
    return service.get_ops_summary()


@router.get("/slots/utilization")
def get_slot_utilization(
    current_user: tuple = Depends(require_operator),
    db: Session = Depends(get_db)
):
    """Get delivery slot utilization by zone and window (operator role only)."""
    service = OperationsService(db)
    return service.calculate_slot_utilization()


@router.get("/promotions/warnings")
def get_promotion_warnings(
    current_user: tuple = Depends(require_operator),
    db: Session = Depends(get_db)
):
    """Get promotion warnings for low usage or low-stock products (operator role only)."""
    service = OperationsService(db)
    return service.get_promotion_warnings()


@router.get("/recommendations/reason-distribution")
def get_recommendation_reason_distribution(
    current_user: tuple = Depends(require_operator),
    db: Session = Depends(get_db)
):
    """Get recommendation reason tag distribution (operator role only)."""
    service = OperationsService(db)
    return service.get_recommendation_reason_distribution()


@router.get("/reviews/sentiment-by-category")
def get_review_sentiment_by_category(
    current_user: tuple = Depends(require_operator),
    db: Session = Depends(get_db)
):
    """Get review sentiment distribution by product category (operator role only)."""
    service = OperationsService(db)
    return service.get_review_sentiment_by_category()


@router.get("/notifications/dispatch-performance")
def get_notification_dispatch_performance(
    current_user: tuple = Depends(require_operator),
    db: Session = Depends(get_db)
):
    """Get notification dispatch performance by channel (operator role only)."""
    service = OperationsService(db)
    return service.get_notification_dispatch_performance()
