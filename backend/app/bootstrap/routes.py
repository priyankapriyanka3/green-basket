"""Bootstrap API routes."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.bootstrap.schemas import BootstrapResponse
from app.bootstrap.services import BootstrapService
from app.database import get_db

router = APIRouter(prefix="/api/v1/app", tags=["bootstrap"])


@router.get("/bootstrap", response_model=BootstrapResponse)
def get_bootstrap(
    include_ops: bool = Query(False, alias="includeOps"),
    current_user: tuple = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get bootstrap data for authenticated user.
    
    Returns profile, default address, categories, recommendations, lists,
    and optional operations summary (operator role only).
    
    Args:
        include_ops: Whether to include operations summary (operator role only)
        current_user: Authenticated user from JWT token
        db: Database session
    
    Returns:
        BootstrapResponse with initialization data
    
    Raises:
        403 FORBIDDEN_ROLE_SCOPE: If shopper tries includeOps=true
    """
    customer, role = current_user
    
    service = BootstrapService(db)
    return service.get_bootstrap_data(customer.customer_id, role, include_ops)
