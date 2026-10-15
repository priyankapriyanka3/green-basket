import re

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ServiceabilityInfo(BaseModel):
    """Serviceability validation result"""
    is_serviceable: bool = Field(..., alias="isServiceable")
    service_zone: str | None = Field(None, alias="serviceZone")
    reason: str

    model_config = ConfigDict(populate_by_name=True)


class AddressResponse(BaseModel):
    """Address information with serviceability"""
    address_id: str = Field(..., alias="addressId")
    customer_id: str = Field(..., alias="customerId")
    label: str
    street: str
    city: str
    state: str
    postal_code: str = Field(..., alias="postalCode")
    country: str
    latitude: float | None = None
    longitude: float | None = None
    is_default: bool = Field(..., alias="isDefault")
    serviceability: ServiceabilityInfo
    updated_at: str = Field(..., alias="updatedAt")

    model_config = ConfigDict(populate_by_name=True)


class AddressCreateRequest(BaseModel):
    """Create new address"""
    label: str = Field(..., min_length=1, max_length=50)
    street: str = Field(..., min_length=1, max_length=200)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=1, max_length=100)
    postal_code: str = Field(..., alias="postalCode", min_length=6, max_length=6)
    country: str = Field(default="India", max_length=100)
    latitude: float | None = None
    longitude: float | None = None
    is_default: bool = Field(default=False, alias="isDefault")

    @field_validator("postal_code")
    @classmethod
    def validate_postal_code(cls, v: str) -> str:
        """Validate postal code format (6 digits)"""
        if not re.match(r"^\d{6}$", v):
            raise ValueError("Postal code must be exactly 6 digits")
        return v

    model_config = ConfigDict(populate_by_name=True)


class AddressUpdateRequest(BaseModel):
    """Update existing address"""
    label: str | None = Field(None, min_length=1, max_length=50)
    street: str | None = Field(None, min_length=1, max_length=200)
    city: str | None = Field(None, min_length=1, max_length=100)
    state: str | None = Field(None, min_length=1, max_length=100)
    postal_code: str | None = Field(None, alias="postalCode", min_length=6, max_length=6)
    country: str | None = Field(None, max_length=100)
    latitude: float | None = None
    longitude: float | None = None
    is_default: bool | None = Field(None, alias="isDefault")

    @field_validator("postal_code")
    @classmethod
    def validate_postal_code(cls, v: str | None) -> str | None:
        """Validate postal code format (6 digits)"""
        if v is not None and not re.match(r"^\d{6}$", v):
            raise ValueError("Postal code must be exactly 6 digits")
        return v

    model_config = ConfigDict(populate_by_name=True)


class ServiceabilityCheckRequest(BaseModel):
    """Explicit serviceability check"""
    postal_code: str = Field(..., alias="postalCode", min_length=6, max_length=6)
    latitude: float | None = None
    longitude: float | None = None
    city: str | None = None

    @field_validator("postal_code")
    @classmethod
    def validate_postal_code(cls, v: str) -> str:
        """Validate postal code format (6 digits)"""
        if not re.match(r"^\d{6}$", v):
            raise ValueError("Postal code must be exactly 6 digits")
        return v

    model_config = ConfigDict(populate_by_name=True)
