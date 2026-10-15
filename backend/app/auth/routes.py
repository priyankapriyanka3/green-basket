"""Auth routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.schemas import LoginRequest, LoginResponse, UserProfile
from app.auth.services import authenticate_customer, create_access_token
from app.database import get_db
from app.errors import AuthenticationError

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate customer and issue JWT token.
    
    POST /api/v1/auth/login
    
    Request:
        phone_number: +91 E.164 format
        otp_or_password: OTP or password
        role_hint: "shopper" or "operator"
    
    Response:
        access_token: JWT bearer token
        token_type: "Bearer"
        expires_in_seconds: Token expiry duration
        user: Customer profile with role
    
    Errors:
        401 INVALID_CREDENTIALS: Authentication failed
        422 PHONE_FORMAT_INVALID: Invalid phone number format
    """
    customer = authenticate_customer(
        db,
        request.phone_number,
        request.otp_or_password,
        request.role_hint
    )
    
    if not customer:
        raise AuthenticationError(message="Invalid phone number or password")
    
    # Determine role from dietary_preference field
    role = "operator" if (customer.dietary_preference and customer.dietary_preference.startswith("role:operator")) else "shopper"
    
    # Create JWT token
    token, expires_in = create_access_token(customer.customer_id, role)
    
    # Build user profile
    user = UserProfile(
        customer_id=customer.customer_id,
        full_name=customer.full_name,
        phone_number=customer.phone_number,
        email=None if (customer.email and customer.email.startswith("$2b$")) else customer.email,
        role=role
    )
    
    return LoginResponse(
        access_token=token,
        expires_in_seconds=expires_in,
        user=user
    )
