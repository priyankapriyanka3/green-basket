"""Unit tests for authentication module."""
from datetime import UTC, datetime, timedelta

import jwt
import pytest

from app.auth.schemas import LoginRequest
from app.auth.services import (
    create_access_token,
    hash_password,
    verify_password,
    verify_token,
)
from app.errors import AuthenticationError, PhoneFormatError, TokenExpiredError


def test_hash_password_uses_bcrypt_cost_12():
    """Verify passwords are hashed with bcrypt cost factor >= 12."""
    password = "test_password_123"
    hashed = hash_password(password)
    
    # bcrypt hashes start with $2b$12$ for cost factor 12
    assert hashed.startswith("$2b$12$"), "Password hash must use bcrypt cost factor 12"
    assert len(hashed) == 60, "bcrypt hash should be 60 characters"


def test_verify_password_succeeds_for_correct_password():
    """Verify correct password validation."""
    password = "correct_password"
    hashed = hash_password(password)
    
    assert verify_password(password, hashed) is True


def test_verify_password_fails_for_incorrect_password():
    """Verify incorrect password rejection."""
    password = "correct_password"
    hashed = hash_password(password)
    
    assert verify_password("wrong_password", hashed) is False


def test_create_access_token_includes_exp_claim():
    """Verify JWT tokens include exp (expiry) claim."""
    customer_id = "cust-001"
    role = "shopper"
    
    token, _expires_in = create_access_token(customer_id, role)
    
    # Decode without verification to inspect claims
    decoded = jwt.decode(token, options={"verify_signature": False})
    
    assert "exp" in decoded, "JWT must include exp claim"
    assert "sub" in decoded, "JWT must include sub claim"
    assert "role" in decoded, "JWT must include role claim"
    assert decoded["sub"] == customer_id
    assert decoded["role"] == role
    
    # Verify expiry is in the future
    exp_timestamp = decoded["exp"]
    now = datetime.now(UTC).timestamp()
    assert exp_timestamp > now, "Token expiry must be in the future"


def test_create_access_token_includes_role_claim():
    """Verify JWT tokens include role claim."""
    customer_id = "cust-002"
    role = "operator"
    
    token, _ = create_access_token(customer_id, role)
    
    decoded = jwt.decode(token, options={"verify_signature": False})
    
    assert decoded["role"] == "operator"


def test_verify_token_succeeds_for_valid_token():
    """Verify valid token verification."""
    customer_id = "cust-003"
    role = "shopper"
    
    token, _ = create_access_token(customer_id, role)
    
    payload = verify_token(token)
    
    assert payload["sub"] == customer_id
    assert payload["role"] == role


def test_verify_token_raises_for_expired_token():
    """Verify expired token raises TokenExpiredError."""
    from app.config import settings
    
    # Create token that expired 1 hour ago
    expired_time = datetime.now(UTC) - timedelta(hours=1)
    payload = {
        "sub": "cust-004",
        "role": "shopper",
        "exp": expired_time
    }
    
    token = jwt.encode(payload, settings.jwt_secret, algorithm="HS256")
    
    with pytest.raises(TokenExpiredError):
        verify_token(token)


def test_verify_token_raises_for_invalid_signature():
    """Verify token with invalid signature raises AuthenticationError."""
    token = jwt.encode({"sub": "cust-005", "role": "shopper"}, "wrong_secret", algorithm="HS256")
    
    with pytest.raises(AuthenticationError):
        verify_token(token)


def test_phone_number_validation_accepts_valid_e164():
    """Verify +91 E.164 format phone validation."""
    valid_phones = [
        "+919876543210",
        "+919123456789",
        "+918000000000"
    ]
    
    for phone in valid_phones:
        request = LoginRequest(
            phone_number=phone,
            otp_or_password="test123",
            role_hint="shopper"
        )
        assert request.phone_number == phone


def test_phone_number_validation_rejects_invalid_formats():
    """Verify invalid phone number formats are rejected."""
    invalid_phones = [
        "9876543210",           # Missing +91
        "+91 9876543210",       # Space
        "+91-9876-543210",      # Hyphens
        "+910876543210",        # Starts with 0
        "+9198765432",          # Too short
        "+919876543210123",     # Too long
        "919876543210",         # Missing +
        "+1234567890",          # Wrong country code
    ]
    
    for phone in invalid_phones:
        with pytest.raises(PhoneFormatError):
            LoginRequest(
                phone_number=phone,
                otp_or_password="test123",
                role_hint="shopper"
            )


def test_login_request_validates_role_hint():
    """Verify role_hint must be shopper or operator."""
    # Valid role hints
    LoginRequest(phone_number="+919876543210", otp_or_password="test", role_hint="shopper")
    LoginRequest(phone_number="+919876543210", otp_or_password="test", role_hint="operator")
    
    # Invalid role hint should fail Pydantic validation
    with pytest.raises(Exception):  # Pydantic ValidationError
        LoginRequest(phone_number="+919876543210", otp_or_password="test", role_hint="admin")
