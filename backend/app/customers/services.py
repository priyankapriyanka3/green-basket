"""Customer service layer."""
import json
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.customers.schemas import CustomerProfileResponse, CustomerUpdateRequest
from app.errors import NotFoundError
from app.models.customer import Customer


def get_customer_profile(db: Session, customer_id: str) -> CustomerProfileResponse:
    """
    Get customer profile by ID.
    
    Raises:
        NotFoundError: If customer not found
    """
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    
    if not customer:
        raise NotFoundError(message=f"Customer {customer_id} not found")
    
    # Parse allergies from JSON
    allergies = []
    if customer.allergies_json:
        try:
            allergies = json.loads(customer.allergies_json)
        except json.JSONDecodeError:
            allergies = []
    
    return CustomerProfileResponse(
        customer_id=customer.customer_id,
        full_name=customer.full_name,
        phone_number=customer.phone_number,
        email=None if (customer.email and customer.email.startswith("$2b$")) else customer.email,
        preferred_language=customer.preferred_language or "en",
        dietary_preference=None if (customer.dietary_preference and customer.dietary_preference.startswith("role:")) else customer.dietary_preference,
        allergies=allergies,
        loyalty_points=float(customer.loyalty_points or 0),
        status=customer.status or "active",
        created_at=customer.created_at,
        updated_at=customer.updated_at
    )


def update_customer_profile(
    db: Session,
    customer_id: str,
    updates: CustomerUpdateRequest
) -> CustomerProfileResponse:
    """
    Update customer profile.
    
    Raises:
        NotFoundError: If customer not found
    """
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    
    if not customer:
        raise NotFoundError(message=f"Customer {customer_id} not found")
    
    # Apply updates
    if updates.full_name is not None:
        customer.full_name = updates.full_name
    
    if updates.email is not None:
        # Preserve password hash if stored in email field
        if not (customer.email and customer.email.startswith("$2b$")):
            customer.email = updates.email
    
    if updates.preferred_language is not None:
        customer.preferred_language = updates.preferred_language
    
    if updates.dietary_preference is not None:
        # Preserve role prefix if present
        if customer.dietary_preference and customer.dietary_preference.startswith("role:"):
            pass  # Don't overwrite role metadata
        else:
            customer.dietary_preference = updates.dietary_preference
    
    if updates.allergies is not None:
        customer.allergies_json = json.dumps(updates.allergies)
    
    customer.updated_at = datetime.now(UTC).isoformat()
    
    db.commit()
    db.refresh(customer)
    
    return get_customer_profile(db, customer_id)
