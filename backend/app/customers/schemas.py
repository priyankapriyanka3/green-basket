"""Customer schemas."""
import re
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.errors import ErrorDetail, ValidationError

PHONE_PATTERN = re.compile(r'^\+91[1-9]\d{9}$')


class CustomerProfileResponse(BaseModel):
    """Customer profile response."""
    customer_id: str
    full_name: str
    phone_number: str
    email: str | None
    preferred_language: str
    dietary_preference: str | None
    allergies: list[str]
    loyalty_points: float
    status: Literal["active", "inactive"]
    created_at: str
    updated_at: str


class CustomerUpdateRequest(BaseModel):
    """Customer profile update request."""
    full_name: str | None = None
    email: str | None = None
    preferred_language: str | None = Field(None, pattern="^[a-z]{2}$")
    dietary_preference: str | None = None
    allergies: list[str] | None = None
    
    @field_validator("allergies")
    @classmethod
    def validate_allergies(cls, v: list[str] | None) -> list[str] | None:
        """Validate allergies list."""
        if v is not None:
            if not isinstance(v, list):
                raise ValidationError(
                    message="Allergies must be a list",
                    details=[ErrorDetail(field="allergies", reason="invalid_type")]
                )
            for item in v:
                if not isinstance(item, str) or not item.strip():
                    raise ValidationError(
                        message="Each allergy must be a non-empty string",
                        details=[ErrorDetail(field="allergies", reason="invalid_item")]
                    )
        return v
