from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.addresses.schemas import (
    AddressCreateRequest,
    AddressResponse,
    AddressUpdateRequest,
    ServiceabilityInfo,
)
from app.errors import AppException
from app.models.address import Address


class AddressService:
    """Service for address management and serviceability validation"""

    # Supported postal code prefixes (Mumbai 400xxx, Bengaluru 560xxx)
    SUPPORTED_POSTAL_PREFIXES = ["400", "560"]

    def __init__(self, session: Session):
        self.session = session

    def check_serviceability(
        self,
        postal_code: str,
        latitude: float | None = None,
        longitude: float | None = None,
        city: str | None = None,
    ) -> ServiceabilityInfo:
        """
        Check address serviceability based on postal code and coordinates
        
        Rules:
        - Mumbai: 400xxx postal codes
        - Bengaluru: 560xxx postal codes
        - Coordinate-aware eligibility when lat/lon provided
        """
        prefix = postal_code[:3]

        if prefix not in self.SUPPORTED_POSTAL_PREFIXES:
            return ServiceabilityInfo(
                is_serviceable=False,
                service_zone=None,
                reason="unsupported_postal_code",
            )

        # Determine service zone
        if prefix == "400":
            service_zone = f"Mumbai-{postal_code}"
        elif prefix == "560":
            service_zone = f"Bengaluru-{postal_code}"
        else:
            service_zone = None

        # Coordinate-aware validation (if coordinates provided)
        if latitude is not None and longitude is not None:
            # Mumbai coordinate bounds (approximate)
            if prefix == "400":
                if not (18.8 <= latitude <= 19.3 and 72.7 <= longitude <= 73.0):
                    return ServiceabilityInfo(
                        is_serviceable=False,
                        service_zone=service_zone,
                        reason="coordinates_outside_service_area",
                    )
            # Bengaluru coordinate bounds (approximate)
            elif prefix == "560":
                if not (12.8 <= latitude <= 13.2 and 77.4 <= longitude <= 77.8):
                    return ServiceabilityInfo(
                        is_serviceable=False,
                        service_zone=service_zone,
                        reason="coordinates_outside_service_area",
                    )

        return ServiceabilityInfo(
            is_serviceable=True,
            service_zone=service_zone,
            reason="supported_postal_code",
        )

    def list_addresses(self, customer_id: str) -> list[AddressResponse]:
        """List all addresses for a customer"""
        addresses = (
            self.session.query(Address)
            .filter(Address.customer_id == customer_id)
            .all()
        )

        return [self._build_address_response(addr) for addr in addresses]

    def get_address(self, address_id: str, customer_id: str) -> AddressResponse:
        """Get specific address"""
        address = (
            self.session.query(Address)
            .filter(
                Address.address_id == address_id,
                Address.customer_id == customer_id,
            )
            .first()
        )

        if not address:
            raise AppException(
                code="ADDRESS_NOT_FOUND",
                message="Address not found",
                status_code=404,
            )

        return self._build_address_response(address)

    def create_address(
        self,
        customer_id: str,
        data: AddressCreateRequest,
    ) -> AddressResponse:
        """Create new address with serviceability check"""
        # Check serviceability
        serviceability = self.check_serviceability(
            postal_code=data.postal_code,
            latitude=data.latitude,
            longitude=data.longitude,
            city=data.city,
        )

        # Generate address ID
        address_id = self._generate_address_id()

        # If setting as default, clear existing default
        if data.is_default:
            self._clear_default_address(customer_id)

        # Create address record
        address = Address(
            address_id=address_id,
            customer_id=customer_id,
            address_line1=f"{data.label}: {data.street}",  # Store label + street
            address_line2=None,
            city=data.city,
            state=data.state,
            postal_code=data.postal_code,
            country=data.country,
            latitude=data.latitude,
            longitude=data.longitude,
            is_default="true" if data.is_default else "false",
            serviceability_status="serviceable" if serviceability.is_serviceable else "not_serviceable",
            serviceability_reason=serviceability.reason,
            created_at=datetime.now(UTC).isoformat() + "Z",
            updated_at=datetime.now(UTC).isoformat() + "Z",
        )

        self.session.add(address)
        self.session.commit()
        self.session.refresh(address)

        return self._build_address_response(address)

    def update_address(
        self,
        address_id: str,
        customer_id: str,
        data: AddressUpdateRequest,
    ) -> AddressResponse:
        """Update existing address"""
        address = (
            self.session.query(Address)
            .filter(
                Address.address_id == address_id,
                Address.customer_id == customer_id,
            )
            .first()
        )

        if not address:
            raise AppException(
                code="ADDRESS_NOT_FOUND",
                message="Address not found",
                status_code=404,
            )

        # Update fields
        # Extract current label and street if they need to be preserved
        current_label = "Address"
        current_street = address.address_line1
        if ": " in address.address_line1:
            current_label, current_street = address.address_line1.split(": ", 1)
        
        # Update label and/or street
        if data.label is not None:
            current_label = data.label
        if data.street is not None:
            current_street = data.street
        
        # Rebuild address_line1 if label or street changed
        if data.label is not None or data.street is not None:
            address.address_line1 = f"{current_label}: {current_street}"
        
        if data.city is not None:
            address.city = data.city
        if data.state is not None:
            address.state = data.state
        if data.postal_code is not None:
            address.postal_code = data.postal_code
        if data.country is not None:
            address.country = data.country
        if data.latitude is not None:
            address.latitude = data.latitude
        if data.longitude is not None:
            address.longitude = data.longitude

        # Re-check serviceability if postal code or coordinates changed
        if data.postal_code is not None or data.latitude is not None or data.longitude is not None:
            serviceability = self.check_serviceability(
                postal_code=address.postal_code,
                latitude=address.latitude,
                longitude=address.longitude,
                city=address.city,
            )
            address.serviceability_status = "serviceable" if serviceability.is_serviceable else "not_serviceable"
            address.serviceability_reason = serviceability.reason

        # Handle default address change
        if data.is_default is not None:
            if data.is_default:
                self._clear_default_address(customer_id)
                address.is_default = "true"
            else:
                address.is_default = "false"

        address.updated_at = datetime.now(UTC).isoformat() + "Z"

        self.session.commit()
        self.session.refresh(address)

        return self._build_address_response(address)

    def delete_address(self, address_id: str, customer_id: str) -> None:
        """Delete address"""
        address = (
            self.session.query(Address)
            .filter(
                Address.address_id == address_id,
                Address.customer_id == customer_id,
            )
            .first()
        )

        if not address:
            raise AppException(
                code="ADDRESS_NOT_FOUND",
                message="Address not found",
                status_code=404,
            )

        self.session.delete(address)
        self.session.commit()

    def _clear_default_address(self, customer_id: str) -> None:
        """Clear default flag on all addresses for customer"""
        self.session.query(Address).filter(
            Address.customer_id == customer_id,
            Address.is_default == "true",
        ).update({"is_default": "false"})
        self.session.commit()

    def _generate_address_id(self) -> str:
        """Generate address ID with addr- prefix"""
        # Get count of existing addresses
        count = self.session.query(Address).count()
        return f"addr-{count + 1:03d}"

    def _build_address_response(self, address: Address) -> AddressResponse:
        """Build address response with serviceability info"""
        serviceability = ServiceabilityInfo(
            is_serviceable=(address.serviceability_status == "serviceable"),
            service_zone=None,
            reason=address.serviceability_reason or "unknown",
        )

        # Determine service zone from postal code
        if serviceability.is_serviceable:
            prefix = address.postal_code[:3]
            if prefix == "400":
                serviceability.service_zone = f"Mumbai-{address.postal_code}"
            elif prefix == "560":
                serviceability.service_zone = f"Bengaluru-{address.postal_code}"

        # Parse label and street from address_line1 (stored as "label: street")
        label = "Address"
        street = address.address_line1
        if ": " in address.address_line1:
            label, street = address.address_line1.split(": ", 1)

        return AddressResponse(
            address_id=address.address_id,
            customer_id=address.customer_id,
            label=label,
            street=street,
            city=address.city,
            state=address.state,
            postal_code=address.postal_code,
            country=address.country,
            latitude=float(address.latitude) if address.latitude else None,
            longitude=float(address.longitude) if address.longitude else None,
            is_default=(address.is_default == "true"),
            serviceability=serviceability,
            updated_at=address.updated_at,
        )
