"""Bootstrap service for app initialization data."""
import json

from sqlalchemy.orm import Session

from app.bootstrap.schemas import (
    AddressServiceability,
    AddressSummary,
    BootstrapResponse,
    CategorySummary,
    ProfileSummary,
    RecommendationCard,
    ShoppingListSummary,
)
from app.models.address import Address
from app.models.category import Category
from app.models.customer import Customer
from app.models.recommendation import Recommendation
from app.models.shopping_list import ShoppingList, ShoppingListItem
from app.operations.services import OperationsService


class BootstrapService:
    """Service for loading bootstrap data."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_bootstrap_data(
        self,
        customer_id: str,
        role: str,
        include_ops: bool = False
    ) -> BootstrapResponse:
        """Get bootstrap data for authenticated user.
        
        Args:
            customer_id: Customer ID from JWT token
            role: User role (shopper or operator)
            include_ops: Whether to include operations summary (operator only)
        
        Returns:
            BootstrapResponse with profile, addresses, categories, recommendations, lists, and optional ops summary
        
        Raises:
            HTTPException: 403 if shopper tries to access includeOps=true
        """
        from app.errors import AppException
        
        # Enforce operator role for ops summary
        if include_ops and role != "operator":
            raise AppException(
                code="FORBIDDEN_ROLE_SCOPE",
                message="Operations data requires operator role",
                status_code=403
            )
        
        # Get customer profile
        customer = self.db.query(Customer).filter(
            Customer.customer_id == customer_id
        ).first()
        
        if not customer:
            raise AppException(
                code="CUSTOMER_NOT_FOUND",
                message="Customer not found",
                status_code=404
            )
        
        # Parse allergies from JSON
        allergies = []
        if customer.allergies_json:
            try:
                allergies = json.loads(customer.allergies_json)
            except (json.JSONDecodeError, TypeError):
                allergies = []
        
        profile = ProfileSummary(
            customer_id=customer.customer_id,
            name=customer.full_name,
            preferred_language=customer.preferred_language,
            dietary_preference=customer.dietary_preference,
            allergies=allergies,
            loyalty_points=int(customer.loyalty_points) if customer.loyalty_points else 0
        )
        
        # Get default address
        default_address = None
        address_record = self.db.query(Address).filter(
            Address.customer_id == customer_id,
            Address.is_default.in_(["1", "true", 1])
        ).first()
        
        if address_record:
            serviceability = AddressServiceability(
                is_serviceable=(address_record.serviceability_status == "serviceable"),
                service_zone=address_record.service_zone,
                reason=address_record.serviceability_reason or "checked"
            )
            
            # Parse label from address_line1 (stored as "label: street")
            label = "Home"
            if ": " in address_record.address_line1:
                label, _ = address_record.address_line1.split(": ", 1)
            
            default_address = AddressSummary(
                address_id=address_record.address_id,
                label=label,
                postal_code=address_record.postal_code,
                serviceability=serviceability
            )
        
        # Get featured categories
        featured_categories = []
        categories = self.db.query(Category).filter(
            Category.is_active.in_(["1", "true", "True"])
        ).order_by(Category.category_id).limit(10).all()
        
        for cat in categories:
            featured_categories.append(
                CategorySummary(
                    category_id=cat.category_id,
                    name=cat.name,
                    icon_url=cat.icon_url
                )
            )
        
        # Get recommendations
        recommendations = []
        reco_records = self.db.query(Recommendation).filter(
            Recommendation.customer_id == customer_id
        ).limit(10).all()
        
        for reco in reco_records:
            recommendations.append(
                RecommendationCard(
                    recommendation_id=reco.recommendation_id,
                    product_id=reco.product_id,
                    score=float(reco.score),
                    reason_tag=reco.reason_tag,
                    reason_text=reco.reason_text or ""
                )
            )
        
        # Get shopping lists
        shopping_lists = []
        list_records = self.db.query(ShoppingList).filter(
            ShoppingList.customer_id == customer_id
        ).all()
        
        for lst in list_records:
            # Count items in this list
            item_count = self.db.query(ShoppingListItem).filter(
                ShoppingListItem.list_id == lst.list_id
            ).count()
            
            shopping_lists.append(
                ShoppingListSummary(
                    list_id=lst.list_id,
                    name=lst.name,
                    is_ai_generated=(lst.is_ai_generated == 1),
                    suggestion_note=lst.suggestion_note,
                    item_count=item_count
                )
            )
        
        # Get ops summary if requested and authorized
        ops_summary = None
        if include_ops:
            ops_service = OperationsService(self.db)
            ops_summary = ops_service.get_ops_summary()
        
        return BootstrapResponse(
            profile=profile,
            default_address=default_address,
            featured_categories=featured_categories,
            recommendations=recommendations,
            shopping_lists=shopping_lists,
            ops_summary=ops_summary
        )
