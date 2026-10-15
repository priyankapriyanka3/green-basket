"""Shopping list routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.customer import Customer
from app.shopping_lists.schemas import (
    GenerateShoppingListRequest,
    GenerateShoppingListResponse,
    ShoppingListResponse,
)
from app.shopping_lists.services import ShoppingListService

router = APIRouter(prefix="/api/v1/shopping-lists", tags=["shopping_lists"])


@router.get("/", response_model=list[ShoppingListResponse])
def get_shopping_lists(
    current_user: tuple[Customer, str] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all shopping lists for the current customer."""
    customer, _role = current_user
    service = ShoppingListService(db)
    return service.get_customer_lists(customer_id=customer.customer_id)


@router.get("/{list_id}", response_model=ShoppingListResponse)
def get_shopping_list(
    list_id: str,
    current_user: tuple[Customer, str] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific shopping list."""
    customer, _role = current_user
    service = ShoppingListService(db)
    shopping_list = service.get_list_by_id(
        list_id=list_id,
        customer_id=customer.customer_id
    )
    
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    
    return shopping_list


@router.post("/generate", response_model=GenerateShoppingListResponse, status_code=201)
def generate_shopping_list(
    request: GenerateShoppingListRequest,
    current_user: tuple[Customer, str] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate an AI shopping list based on order history and mode.
    
    - **mode**: Generation mode (weekly_reorder, diet_boost, seasonal_refresh)
    - **source_order_window_days**: Order history window in days (7-90, default 42)
    - **target_list_name**: Name for the generated list
    """
    customer, _role = current_user
    service = ShoppingListService(db)
    
    try:
        shopping_list, suggestion_note, items_added = service.generate_shopping_list(
            customer_id=customer.customer_id,
            request=request
        )
        
        return GenerateShoppingListResponse(
            list=shopping_list,
            suggestion_note=suggestion_note,
            items_added=items_added
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
