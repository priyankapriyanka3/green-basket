"""Auth request and response schemas."""
import re
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.errors import PhoneFormatError

# Phone number validation pattern: +91 E.164-style format
PHONE_PATTERN = re.compile(r'^\+91[1-9]\d{9}$')


class LoginRequest(BaseModel):
    """Login request payload."""
    phone_number: str = Field(..., description="Phone number in +91 E.164 format")
    otp_or_password: str = Field(..., min_length=4, description="OTP or password")
    role_hint: Literal["shopper", "operator"] = Field(default="shopper", description="Role hint for login")
    
    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        """Validate phone number format."""
        if not PHONE_PATTERN.match(v):
            raise PhoneFormatError(
                message="Phone number must be in +91 E.164 format (e.g., +919876543210)",
                details=[{"field": "phone_number", "reason": "invalid_format"}]
            )
        return v


class UserProfile(BaseModel):
    """User profile in auth response."""
    customer_id: str
    full_name: str
    phone_number: str
    email: str | None
    role: Literal["shopper", "operator"]


class LoginResponse(BaseModel):
    """Login response with JWT token."""
    access_token: str
    token_type: str = "Bearer"
    expires_in_seconds: int
    user: UserProfile
