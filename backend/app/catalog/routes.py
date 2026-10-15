
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.catalog.schemas import CatalogResponse
from app.catalog.services import CatalogService
from app.database import get_db

router = APIRouter()


@router.get("/products", response_model=CatalogResponse)
def get_products(
    q: str | None = Query(None, description="Search keyword"),
    category_id: str | None = Query(None, alias="categoryId"),
    is_organic: bool | None = Query(None, alias="isOrganic"),
    featured_only: bool = Query(False, alias="featuredOnly"),
    page: int = Query(1, ge=1),
    page_size: int = Query(24, ge=1, le=100, alias="pageSize"),
    session: Session = Depends(get_db),
):
    """
    Browse/search/filter catalog products
    
    Supports:
    - Keyword search across product name and description
    - Filter by category
    - Filter by organic status
    - Filter by featured status
    - Pagination with configurable page size
    """
    service = CatalogService(session)
    return service.search_products(
        q=q,
        category_id=category_id,
        is_organic=is_organic,
        featured_only=featured_only,
        page=page,
        page_size=page_size,
    )
