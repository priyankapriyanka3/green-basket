"""Auth dependencies for route protection."""
from typing import Annotated

from fastapi import Depends, Header
from sqlalchemy.orm import Session

from app.auth.services import verify_token
from app.database import get_db
from app.errors import AuthenticationError, ForbiddenRoleScopeError
from app.models.customer import Customer


def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    db: Session = Depends(get_db)
) -> tuple[Customer, str]:
    """
    Extract and validate JWT token from Authorization header.
    
    Returns:
        Tuple of (Customer, role)
    
    Raises:
        AuthenticationError: If token is missing, invalid, or expired
    """
    if not authorization:
        raise AuthenticationError(message="Authorization header missing")
    
    if not authorization.startswith("Bearer "):
        raise AuthenticationError(message="Invalid authorization header format")
    
    token = authorization.replace("Bearer ", "")
    
    # Verify and decode token
    payload = verify_token(token)
    
    customer_id = payload.get("sub")
    role = payload.get("role", "shopper")
    
    if not customer_id:
        raise AuthenticationError(message="Invalid token payload")
    
    # Fetch customer from database
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    
    if not customer:
        raise AuthenticationError(message="Customer not found")
    
    if customer.status != "active":
        raise AuthenticationError(message="Account is inactive")
    
    return customer, role


def require_shopper(
    current_user: Annotated[tuple[Customer, str], Depends(get_current_user)]
) -> Customer:
    """Require shopper role."""
    customer, role = current_user
    if role not in ["shopper", "operator"]:
        raise ForbiddenRoleScopeError(message="Shopper access required")
    return customer


def require_operator(
    current_user: Annotated[tuple[Customer, str], Depends(get_current_user)]
) -> Customer:
    """Require operator role."""
    customer, role = current_user
    if role != "operator":
        raise ForbiddenRoleScopeError(message="Operator access required")
    return customer
