from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.addresses.schemas import (
    AddressCreateRequest,
    AddressResponse,
    AddressUpdateRequest,
    ServiceabilityCheckRequest,
    ServiceabilityInfo,
)
from app.addresses.services import AddressService
from app.auth.dependencies import get_current_user
from app.database import get_db

router = APIRouter()


@router.get("/", response_model=list[AddressResponse])
def list_addresses(
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    """List all addresses for the authenticated customer"""
    service = AddressService(session)
    return service.list_addresses(current_user["user_id"])


@router.post("/", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
def create_address(
    data: AddressCreateRequest,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    """Create a new address for the authenticated customer"""
    service = AddressService(session)
    return service.create_address(current_user["user_id"], data)


@router.get("/{address_id}", response_model=AddressResponse)
def get_address(
    address_id: str,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    """Get specific address details"""
    service = AddressService(session)
    return service.get_address(address_id, current_user["user_id"])


@router.put("/{address_id}", response_model=AddressResponse)
def update_address(
    address_id: str,
    data: AddressUpdateRequest,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    """Update an existing address"""
    service = AddressService(session)
    return service.update_address(address_id, current_user["user_id"], data)


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(
    address_id: str,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    """Delete an address"""
    service = AddressService(session)
    service.delete_address(address_id, current_user["user_id"])


@router.post("/check-serviceability", response_model=ServiceabilityInfo)
def check_serviceability(
    data: ServiceabilityCheckRequest,
    session: Session = Depends(get_db),
):
    """
    Check serviceability for a postal code and coordinates
    
    Public endpoint for pre-validation before address creation
    """
    service = AddressService(session)
    return service.check_serviceability(
        postal_code=data.postal_code,
        latitude=data.latitude,
        longitude=data.longitude,
        city=data.city,
    )
