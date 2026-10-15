"""Auth service layer with password hashing and JWT generation."""
from datetime import UTC, datetime, timedelta

import bcrypt
import jwt
from sqlalchemy.orm import Session

from app.config import settings
from app.errors import AuthenticationError
from app.models.customer import Customer


def hash_password(password: str) -> str:
    """Hash password with bcrypt cost factor 12."""
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against bcrypt hash."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(customer_id: str, role: str) -> tuple[str, int]:
    """
    Create JWT access token with exp and role claims.
    
    Returns:
        Tuple of (token, expires_in_seconds)
    """
    expires_in = settings.jwt_expiry_seconds
    expiry = datetime.now(UTC) + timedelta(seconds=expires_in)
    
    payload = {
        "sub": customer_id,
        "role": role,
        "exp": expiry
    }
    
    token = jwt.encode(payload, settings.jwt_secret, algorithm="HS256")
    return token, expires_in


def verify_token(token: str) -> dict:
    """
    Verify and decode JWT token.
    
    Raises:
        AuthenticationError: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        from app.errors import TokenExpiredError
        raise TokenExpiredError()
    except jwt.InvalidTokenError:
        raise AuthenticationError(message="Invalid token")


def authenticate_customer(db: Session, phone_number: str, password: str, role_hint: str) -> Customer | None:
    """
    Authenticate customer by phone number and password.
    
    For MVP: password stored in email field (temporary workaround).
    In production: separate password field or use OTP.
    
    Returns:
        Customer if authenticated, None otherwise
    """
    customer = db.query(Customer).filter(Customer.phone_number == phone_number).first()
    
    if not customer:
        return None
    
    # For MVP: password stored in email field as bcrypt hash
    # This is a temporary design for demo purposes
    # All passwords must be bcrypt-hashed; no plaintext fallback
    if not (customer.email and customer.email.startswith("$2b$")):
        return None
    
    if not verify_password(password, customer.email):
        return None
    
    # Verify role matches (for operator accounts)
    # For MVP: role stored in dietary_preference field as "role:operator"
    if role_hint == "operator":
        if not (customer.dietary_preference and customer.dietary_preference.startswith("role:operator")):
            return None
    
    return customer
