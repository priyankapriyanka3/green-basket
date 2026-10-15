"""Unified error envelope and error code taxonomy."""
from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """Field-level validation error detail."""
    field: str
    reason: str


class ErrorResponse(BaseModel):
    """Unified error envelope."""
    code: str
    message: str
    trace_id: str = Field(default_factory=lambda: f"trc-{datetime.now().strftime('%Y%m%d')}-{uuid4().hex[:8]}")
    details: list[ErrorDetail] | None = None


class AppException(Exception):
    """Base application exception with error envelope support."""
    
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
        details: list[ErrorDetail] | None = None
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)
    
    def to_response(self) -> ErrorResponse:
        """Convert to error response envelope."""
        return ErrorResponse(
            code=self.code,
            message=self.message,
            details=self.details
        )


# Error taxonomy from LLD Section 9.1
class AuthenticationError(AppException):
    """Authentication failures (401)."""
    def __init__(self, message: str = "Invalid credentials", details: list[ErrorDetail] | None = None):
        super().__init__("INVALID_CREDENTIALS", message, 401, details)


class TokenExpiredError(AppException):
    """Token expiry (401)."""
    def __init__(self, message: str = "Token has expired", details: list[ErrorDetail] | None = None):
        super().__init__("TOKEN_EXPIRED", message, 401, details)


class ForbiddenRoleScopeError(AppException):
    """Role-based access denial (403)."""
    def __init__(self, message: str = "Insufficient role permissions", details: list[ErrorDetail] | None = None):
        super().__init__("FORBIDDEN_ROLE_SCOPE", message, 403, details)


class ValidationError(AppException):
    """Input validation failures (422)."""
    def __init__(self, message: str = "Validation failed", details: list[ErrorDetail] | None = None):
        super().__init__("VALIDATION_FAILED", message, 422, details)


class PhoneFormatError(AppException):
    """Phone number validation (422)."""
    def __init__(self, message: str = "Invalid phone number format", details: list[ErrorDetail] | None = None):
        super().__init__("PHONE_FORMAT_INVALID", message, 422, details)


class ConflictError(AppException):
    """Business rule conflicts (409)."""
    def __init__(self, code: str, message: str, details: list[ErrorDetail] | None = None):
        super().__init__(code, message, 409, details)


class NotFoundError(AppException):
    """Resource not found (404)."""
    def __init__(self, message: str = "Resource not found", details: list[ErrorDetail] | None = None):
        super().__init__("NOT_FOUND", message, 404, details)
