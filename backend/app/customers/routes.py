"""Customer profile routes."""
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.audit.services import log_audit_event
from app.auth.dependencies import require_shopper
from app.customers.schemas import CustomerProfileResponse, CustomerUpdateRequest
from app.customers.services import get_customer_profile, update_customer_profile
from app.database import get_db
from app.models.customer import Customer
from app.models.order import Order

router = APIRouter()


@router.get("/me", response_model=CustomerProfileResponse)
def get_my_profile(
    current_user: Annotated[Customer, Depends(require_shopper)],
    db: Session = Depends(get_db)
):
    """
    Get current customer profile.
    
    GET /api/v1/customers/me
    
    Requires: JWT bearer token (shopper or operator role)
    
    Response:
        Customer profile with dietary preferences, allergies, loyalty points
    """
    return get_customer_profile(db, current_user.customer_id)


@router.put("/me", response_model=CustomerProfileResponse)
def update_my_profile(
    updates: CustomerUpdateRequest,
    current_user: Annotated[Customer, Depends(require_shopper)],
    db: Session = Depends(get_db)
):
    """
    Update current customer profile.
    
    PUT /api/v1/customers/me
    
    Requires: JWT bearer token
    
    Request:
        full_name: Optional full name
        email: Optional email
        preferred_language: Optional 2-letter language code
        dietary_preference: Optional dietary preference
        allergies: Optional list of allergy strings
    
    Response:
        Updated customer profile
    
    Side Effects:
        Creates audit log entry for profile change
    """
    profile = update_customer_profile(db, current_user.customer_id, updates)
    
    # Log audit event for profile change
    log_audit_event(
        db=db,
        entity_type="customer",
        entity_id=current_user.customer_id,
        action="profile_update",
        actor_id=current_user.customer_id,
        payload=updates.model_dump(exclude_none=True)
    )
    
    return profile
