"""Shopping list service."""
import json
from datetime import UTC, datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.shopping_list import ShoppingList, ShoppingListItem
from app.shopping_lists.schemas import (
    GenerateShoppingListRequest,
    ShoppingListItemResponse,
    ShoppingListResponse,
)


class ShoppingListService:
    """Service for managing shopping lists."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_customer_lists(self, customer_id: str) -> list[ShoppingListResponse]:
        """Get all shopping lists for a customer."""
        lists = (
            self.db.query(ShoppingList)
            .filter(ShoppingList.customer_id == customer_id)
            .order_by(ShoppingList.created_at.desc())
            .all()
        )
        
        result = []
        for shopping_list in lists:
            items = self._get_list_items(shopping_list.list_id)
            result.append(ShoppingListResponse(
                list_id=shopping_list.list_id,
                customer_id=shopping_list.customer_id,
                name=shopping_list.name,
                is_ai_generated=shopping_list.is_ai_generated == "true",
                suggestion_note=shopping_list.suggestion_note,
                created_at=shopping_list.created_at,
                items=items
            ))
        
        return result
    
    def get_list_by_id(
        self,
        list_id: str,
        customer_id: str
    ) -> ShoppingListResponse | None:
        """Get a specific shopping list."""
        shopping_list = (
            self.db.query(ShoppingList)
            .filter(
                ShoppingList.list_id == list_id,
                ShoppingList.customer_id == customer_id
            )
            .first()
        )
        
        if not shopping_list:
            return None
        
        items = self._get_list_items(list_id)
        
        return ShoppingListResponse(
            list_id=shopping_list.list_id,
            customer_id=shopping_list.customer_id,
            name=shopping_list.name,
            is_ai_generated=shopping_list.is_ai_generated == "true",
            suggestion_note=shopping_list.suggestion_note,
            created_at=shopping_list.created_at,
            items=items
        )
    
    def _get_list_items(self, list_id: str) -> list[ShoppingListItemResponse]:
        """Get items for a shopping list with product details."""
        items = (
            self.db.query(ShoppingListItem, Product)
            .join(Product, Product.product_id == ShoppingListItem.product_id)
            .filter(ShoppingListItem.list_id == list_id)
            .all()
        )
        
        return [
            ShoppingListItemResponse(
                item_id=item.item_id,
                product_id=item.product_id,
                product_name=product.name,
                quantity=item.quantity,
                source_reason_tag=item.source_reason_tag,
                unit_price=float(product.unit_price),
                unit_type=product.unit_type
            )
            for item, product in items
        ]
    
    def generate_shopping_list(
        self,
        customer_id: str,
        request: GenerateShoppingListRequest
    ) -> tuple[ShoppingListResponse, str, int]:
        """Generate an AI shopping list based on order history and mode."""
        # Get customer profile
        customer = self.db.query(Customer).filter(
            Customer.customer_id == customer_id
        ).first()
        
        if not customer:
            raise ValueError("Customer not found")
        
        # Parse customer preferences
        dietary_preference = customer.dietary_preference
        try:
            allergies = json.loads(customer.allergies_json) if customer.allergies_json else []
        except json.JSONDecodeError:
            allergies = []
        
        # Calculate cutoff date for order history
        cutoff_date = (
            datetime.now(UTC) - timedelta(days=request.source_order_window_days)
        ).isoformat()
        
        # Get order history within window
        order_items = (
            self.db.query(
                OrderItem.product_id,
                func.count(OrderItem.product_id).label("order_count"),
                func.sum(OrderItem.quantity).label("total_quantity")
            )
            .join(Order, Order.order_id == OrderItem.order_id)
            .filter(Order.customer_id == customer_id)
            .filter(Order.order_date >= cutoff_date)
            .filter(Order.status.in_(["confirmed", "packed", "out_for_delivery", "delivered"]))
            .group_by(OrderItem.product_id)
            .all()
        )
        
        # Generate list items based on mode
        list_items = []
        suggestion_note = ""
        
        if request.mode == "weekly_reorder":
            list_items, suggestion_note = self._generate_weekly_reorder(
                order_items,
                allergies
            )
        elif request.mode == "diet_boost":
            list_items, suggestion_note = self._generate_diet_boost(
                customer_id,
                dietary_preference,
                allergies,
                order_items
            )
        elif request.mode == "seasonal_refresh":
            list_items, suggestion_note = self._generate_seasonal_refresh(
                allergies
            )
        
        # Create shopping list
        list_id = f"lst-{customer_id}-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}"
        timestamp = datetime.now(UTC).isoformat()
        
        shopping_list = ShoppingList(
            list_id=list_id,
            customer_id=customer_id,
            name=request.target_list_name,
            is_ai_generated="true",
            suggestion_note=suggestion_note,
            created_at=timestamp,
            updated_at=timestamp
        )
        
        self.db.add(shopping_list)
        
        # Add items
        for product_id, quantity, reason_tag in list_items:
            item_id = f"itm-{list_id}-{product_id}"
            item = ShoppingListItem(
                item_id=item_id,
                list_id=list_id,
                product_id=product_id,
                quantity=quantity,
                source_reason_tag=reason_tag,
                added_at=timestamp
            )
            self.db.add(item)
        
        self.db.commit()
        
        # Return the created list
        response = self.get_list_by_id(list_id, customer_id)
        return response, suggestion_note, len(list_items)
    
    def _generate_weekly_reorder(
        self,
        order_items,
        allergies: list[str]
    ) -> tuple[list[tuple[str, int, str]], str]:
        """Generate weekly reorder list from order history."""
        list_items = []
        
        # Sort by order frequency
        sorted_items = sorted(
            order_items,
            key=lambda x: x.order_count,
            reverse=True
        )
        
        for item in sorted_items[:10]:  # Top 10 frequently ordered
            product = self.db.query(Product).filter(
                Product.product_id == item.product_id
            ).first()
            
            if product and not self._contains_allergen(product.name, allergies):
                # Calculate suggested quantity (average per order)
                avg_quantity = max(1, int(item.total_quantity / item.order_count))
                list_items.append((
                    item.product_id,
                    avg_quantity,
                    "frequently_bought"
                ))
        
        suggestion_note = (
            f"Based on your last {len(order_items)} orders. "
            f"These are items you order most frequently."
        )
        
        return list_items, suggestion_note
    
    def _generate_diet_boost(
        self,
        customer_id: str,
        dietary_preference: str,
        allergies: list[str],
        order_items
    ) -> tuple[list[tuple[str, int, str]], str]:
        """Generate diet-focused list."""
        list_items = []
        
        # Include some frequently ordered items
        for item in sorted(order_items, key=lambda x: x.order_count, reverse=True)[:5]:
            product = self.db.query(Product).filter(
                Product.product_id == item.product_id
            ).first()
            
            if product and not self._contains_allergen(product.name, allergies):
                avg_quantity = max(1, int(item.total_quantity / item.order_count))
                list_items.append((
                    item.product_id,
                    avg_quantity,
                    "reorder_reminder"
                ))
        
        # Add diet-aligned products
        query = self.db.query(Product)
        
        if dietary_preference in ["vegetarian", "vegan"]:
            query = query.filter(Product.is_organic == "true")
        
        diet_products = (
            query.order_by(Product.average_rating.desc())
            .limit(5)
            .all()
        )
        
        for product in diet_products:
            if not self._contains_allergen(product.name, allergies):
                # Check if already in list
                if product.product_id not in [item[0] for item in list_items]:
                    list_items.append((
                        product.product_id,
                        1,
                        "based_on_diet"
                    ))
        
        suggestion_note = (
            f"Tailored to your {dietary_preference or 'dietary'} preferences. "
            f"Includes your favorites plus new diet-aligned options."
        )
        
        return list_items, suggestion_note
    
    def _generate_seasonal_refresh(
        self,
        allergies: list[str]
    ) -> tuple[list[tuple[str, int, str]], str]:
        """Generate seasonal product list."""
        list_items = []
        
        # Get featured seasonal products
        seasonal_products = (
            self.db.query(Product)
            .filter(Product.is_featured == "true")
            .order_by(Product.average_rating.desc())
            .limit(10)
            .all()
        )
        
        for product in seasonal_products:
            if not self._contains_allergen(product.name, allergies):
                list_items.append((
                    product.product_id,
                    1,
                    "seasonal"
                ))
        
        suggestion_note = (
            "Fresh seasonal picks that are in their prime right now. "
            "Perfect for trying new flavors."
        )
        
        return list_items, suggestion_note
    
    def _contains_allergen(self, product_name: str, allergies: list[str]) -> bool:
        """Check if product name contains any allergens."""
        product_name_lower = product_name.lower()
        return any(
            allergen.lower() in product_name_lower
            for allergen in allergies
        )
