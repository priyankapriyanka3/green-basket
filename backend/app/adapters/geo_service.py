"""Geolocation and serviceability adapter."""
from datetime import datetime
from typing import Any


class GeoServiceAdapter:
    """
    Geolocation/serviceability adapter for postal code and coordinate validation.
    """
    
    def __init__(self):
        """Initialize geo service adapter."""
    
    def validate_postal_code(
        self,
        postal_code: str,
        latitude: float | None = None,
        longitude: float | None = None,
        city: str | None = None
    ) -> dict[str, Any]:
        """
        Validate postal code and coordinate-aware serviceability.
        
        Args:
            postal_code: 6-digit postal code
            latitude: Optional latitude coordinate
            longitude: Optional longitude coordinate
            city: Optional city name
        
        Returns:
            Dictionary containing is_serviceable, service_zone, reason, checked_at
        """
        # Mock implementation for MVP
        # Supports Mumbai (400xxx) and Bengaluru (560xxx) only
        
        is_serviceable = False
        service_zone = None
        reason = "unsupported_postal_code"
        
        if postal_code.startswith("400"):
            is_serviceable = True
            service_zone = "Mumbai-South" if postal_code.startswith("4000") else "Mumbai-North"
            reason = "supported_postal_code"
        elif postal_code.startswith("560"):
            is_serviceable = True
            service_zone = "Bengaluru-Central"
            reason = "supported_postal_code"
        
        return {
            "is_serviceable": is_serviceable,
            "service_zone": service_zone,
            "reason": reason,
            "checked_at": datetime.now().isoformat()
        }
