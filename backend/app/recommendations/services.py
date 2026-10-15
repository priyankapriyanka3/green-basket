"""Recommendation service."""
import json
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.recommendation import Recommendation
from app.recommendations.schemas import ProductRecommendationCard


class RecommendationService:
    """Service for generating and retrieving recommendations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_customer_recommendations(
        self, 
        customer_id: str,
        limit: int = 10
    ) -> list[ProductRecommendationCard]:
        """Get recommendations for a customer with product details."""
        # Get recent recommendations
        recommendations = (
            self.db.query(Recommendation)
            .filter(Recommendation.customer_id == customer_id)
            .order_by(Recommendation.score.desc(), Recommendation.generated_at.desc())
            .limit(limit)
            .all()
        )
        
        # Build product cards with recommendation context
        cards = []
        for rec in recommendations:
            product = self.db.query(Product).filter(
                Product.product_id == rec.product_id
            ).first()
            
            if product:
                cards.append(ProductRecommendationCard(
                    product_id=product.product_id,
                    name=product.name,
                    unit_price=float(product.unit_price),
                    unit_type=product.unit_type,
                    is_organic=product.is_organic == "true",
                    image_url=product.image_url,
                    average_rating=float(product.average_rating) if product.average_rating else None,
                    reason_tag=rec.reason_tag,
                    reason_text=rec.reason_text,
                    score=float(rec.score)
                ))
        
        return cards
    
    def generate_recommendations(
        self,
        customer_id: str,
        force_refresh: bool = False
    ) -> list[Recommendation]:
        """Generate recommendations for a customer."""
        # Check if recent recommendations exist
        if not force_refresh:
            existing = (
                self.db.query(Recommendation)
                .filter(Recommendation.customer_id == customer_id)
                .first()
            )
            if existing:
                return self._get_all_recommendations(customer_id)
        else:
            # Delete existing recommendations when force refreshing
            self.db.query(Recommendation).filter(
                Recommendation.customer_id == customer_id
            ).delete()
            self.db.commit()
        
        # Get customer profile
        customer = self.db.query(Customer).filter(
            Customer.customer_id == customer_id
        ).first()
        
        if not customer:
            return []
        
        # Parse dietary preferences and allergies
        dietary_preference = customer.dietary_preference
        try:
            allergies = json.loads(customer.allergies_json) if customer.allergies_json else []
        except json.JSONDecodeError:
            allergies = []
        
        # Get customer's order history
        order_history = (
            self.db.query(OrderItem.product_id)
            .join(Order, Order.order_id == OrderItem.order_id)
            .filter(Order.customer_id == customer_id)
            .filter(Order.status.in_(["confirmed", "packed", "out_for_delivery", "delivered"]))
            .all()
        )
        
        purchased_product_ids = [item.product_id for item in order_history]
        
        # Generate recommendations based on different strategies
        recommendations = []
        
        # Strategy 1: Frequently bought (reorder reminders)
        if purchased_product_ids:
            recommendations.extend(
                self._generate_reorder_recommendations(customer_id, purchased_product_ids, allergies)
            )
        
        # Strategy 2: Diet-based recommendations
        if dietary_preference:
            recommendations.extend(
                self._generate_diet_recommendations(customer_id, dietary_preference, allergies)
            )
        
        # Strategy 3: Trending products
        recommendations.extend(
            self._generate_trending_recommendations(customer_id, allergies)
        )
        
        # Strategy 4: Seasonal products
        recommendations.extend(
            self._generate_seasonal_recommendations(customer_id, allergies)
        )
        
        # Persist recommendations
        for rec in recommendations:
            self.db.add(rec)
        
        self.db.commit()
        
        return recommendations
    
    def _get_all_recommendations(self, customer_id: str) -> list[Recommendation]:
        """Get all recommendations for a customer."""
        return (
            self.db.query(Recommendation)
            .filter(Recommendation.customer_id == customer_id)
            .order_by(Recommendation.score.desc())
            .all()
        )
    
    def _generate_reorder_recommendations(
        self,
        customer_id: str,
        purchased_product_ids: list[str],
        allergies: list[str]
    ) -> list[Recommendation]:
        """Generate reorder recommendations based on purchase history."""
        recommendations = []
        
        # Get top purchased products
        product_counts = {}
        for pid in purchased_product_ids:
            product_counts[pid] = product_counts.get(pid, 0) + 1
        
        # Sort by frequency
        top_products = sorted(
            product_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        for product_id, count in top_products:
            product = self.db.query(Product).filter(
                Product.product_id == product_id
            ).first()
            
            if product and not self._contains_allergen(product.name, allergies):
                rec_id = f"rec-{customer_id}-{product_id}-reorder"
                score = min(0.9, 0.5 + (count * 0.1))
                
                recommendations.append(Recommendation(
                    recommendation_id=rec_id,
                    customer_id=customer_id,
                    product_id=product_id,
                    score=score,
                    reason_tag="reorder_reminder",
                    reason_text=f"You've ordered {product.name} {count} times before",
                    generated_at=datetime.now(UTC).isoformat()
                ))
        
        return recommendations
    
    def _contains_allergen(self, product_name: str, allergies: list[str]) -> bool:
        """Check if product name contains any allergens."""
        product_name_lower = product_name.lower()
        return any(
            allergen.lower() in product_name_lower
            for allergen in allergies
        )
    
    def _generate_diet_recommendations(
        self,
        customer_id: str,
        dietary_preference: str,
        allergies: list[str]
    ) -> list[Recommendation]:
        """Generate recommendations based on dietary preferences."""
        recommendations = []
        
        # Find products matching dietary preference
        query = self.db.query(Product)
        
        # Filter based on dietary preference
        if dietary_preference == "vegetarian":
            # Favor organic produce and vegetables
            query = query.filter(Product.is_organic == "true")
        elif dietary_preference == "vegan":
            # Similar to vegetarian but stricter
            query = query.filter(Product.is_organic == "true")
        
        # Get top-rated products
        products = (
            query.order_by(Product.average_rating.desc())
            .limit(3)
            .all()
        )
        
        for product in products:
            # Skip products with allergens (simplified)
            product_name_lower = product.name.lower()
            if any(allergen.lower() in product_name_lower for allergen in allergies):
                continue
            
            rec_id = f"rec-{customer_id}-{product.product_id}-diet"
            
            recommendations.append(Recommendation(
                recommendation_id=rec_id,
                customer_id=customer_id,
                product_id=product.product_id,
                score=0.8,
                reason_tag="based_on_diet",
                reason_text=f"Matches your {dietary_preference} preference",
                generated_at=datetime.now(UTC).isoformat()
            ))
        
        return recommendations
    
    def _generate_trending_recommendations(
        self,
        customer_id: str,
        allergies: list[str]
    ) -> list[Recommendation]:
        """Generate recommendations for trending products."""
        recommendations = []
        
        # Get products with high ratings and review counts
        trending_products = (
            self.db.query(Product)
            .filter(Product.review_count > 0)
            .order_by(
                Product.average_rating.desc(),
                Product.review_count.desc()
            )
            .limit(3)
            .all()
        )
        
        for product in trending_products:
            if not self._contains_allergen(product.name, allergies):
                rec_id = f"rec-{customer_id}-{product.product_id}-trending"
                
                recommendations.append(Recommendation(
                    recommendation_id=rec_id,
                    customer_id=customer_id,
                    product_id=product.product_id,
                    score=0.7,
                    reason_tag="trending",
                    reason_text=f"Popular with {product.review_count} reviews",
                    generated_at=datetime.now(UTC).isoformat()
                ))
        
        return recommendations
    
    def _generate_seasonal_recommendations(
        self,
        customer_id: str,
        allergies: list[str]
    ) -> list[Recommendation]:
        """Generate seasonal product recommendations."""
        recommendations = []
        
        # Get featured seasonal products
        seasonal_products = (
            self.db.query(Product)
            .filter(Product.is_featured == "true")
            .order_by(Product.average_rating.desc())
            .limit(2)
            .all()
        )
        
        for product in seasonal_products:
            if not self._contains_allergen(product.name, allergies):
                rec_id = f"rec-{customer_id}-{product.product_id}-seasonal"
                
                recommendations.append(Recommendation(
                    recommendation_id=rec_id,
                    customer_id=customer_id,
                    product_id=product.product_id,
                    score=0.75,
                    reason_tag="seasonal",
                    reason_text=f"{product.name} is in season now",
                    generated_at=datetime.now(UTC).isoformat()
                ))
        
        return recommendations
    
    def get_reason_distribution(self) -> dict:
        """Get distribution of recommendation reason tags for operations."""
        reason_counts = {}
        
        recommendations = self.db.query(Recommendation).all()
        
        for rec in recommendations:
            reason_counts[rec.reason_tag] = reason_counts.get(rec.reason_tag, 0) + 1
        
        return reason_counts
