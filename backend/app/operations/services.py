"""Operations KPI calculation services."""
from datetime import UTC, datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.delivery_slot import DeliverySlot
from app.models.notification import Notification
from app.models.product import Product
from app.models.promotion import Promotion
from app.models.recommendation import Recommendation
from app.models.review import Review
from app.operations.schemas import OpsSummaryResponse


class OperationsService:
    """Operations KPI and reporting service."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_slot_utilization(self) -> dict:
        """Calculate delivery slot utilization by zone and window.
        
        Returns dict with slot utilization metrics including capacity warnings.
        """
        slots = self.db.query(DeliverySlot).all()
        
        utilization_data = []
        open_alerts = 0
        
        for slot in slots:
            if slot.max_capacity > 0:
                utilization_pct = (slot.reserved_count / slot.max_capacity) * 100
            else:
                utilization_pct = 0
            
            # Alert if 90%+ capacity or full
            is_alert = utilization_pct >= 90
            if is_alert:
                open_alerts += 1
            
            utilization_data.append({
                "slot_id": slot.slot_id,
                "slot_date": slot.slot_date,
                "service_zone": slot.service_zone,
                "reserved_count": slot.reserved_count,
                "max_capacity": slot.max_capacity,
                "utilization_pct": round(utilization_pct, 2),
                "is_alert": is_alert
            })
        
        return {
            "slots": utilization_data,
            "open_alerts": open_alerts
        }
    
    def get_promotion_warnings(self) -> dict:
        """Identify promotions with low usage or pointing at low-stock products.
        
        Returns dict with promotion warnings count and details.
        """
        
        # Get active promotions
        active_promotions = self.db.query(Promotion).filter(
            Promotion.is_active == "true"
        ).all()
        
        warnings = []
        
        for promo in active_promotions:
            # Check if usage is low relative to limit
            if promo.usage_limit and promo.usage_count < (promo.usage_limit * 0.1):
                warnings.append({
                    "promotion_id": promo.promotion_id,
                    "code": promo.code,
                    "reason": "low_usage",
                    "usage_count": promo.usage_count,
                    "usage_limit": promo.usage_limit
                })
        
        return {
            "warnings": warnings,
            "count": len(warnings)
        }
    
    def get_recommendation_reason_distribution(self) -> dict:
        """Get distribution of recommendation reason tags.
        
        Returns dict with reason tag counts for operations reporting.
        """
        # Get all recommendations from last 30 days
        thirty_days_ago = (datetime.now(UTC) - timedelta(days=30)).isoformat()
        
        reason_counts = self.db.query(
            Recommendation.reason_tag,
            func.count(Recommendation.recommendation_id).label('count')
        ).filter(
            Recommendation.generated_at >= thirty_days_ago
        ).group_by(
            Recommendation.reason_tag
        ).all()
        
        distribution = {row.reason_tag: row.count for row in reason_counts}
        
        return {
            "distribution": distribution,
            "period_days": 30
        }
    
    def get_review_sentiment_by_category(self) -> dict:
        """Analyze review sentiment trends by product category.
        
        Returns dict with sentiment distribution per category.
        """
        from app.models.category import Category
        
        # Join reviews with products and categories
        sentiment_data = self.db.query(
            Category.name.label('category_name'),
            Review.sentiment,
            func.count(Review.review_id).label('count')
        ).join(
            Product, Review.product_id == Product.product_id
        ).join(
            Category, Product.category_id == Category.category_id
        ).group_by(
            Category.name, Review.sentiment
        ).all()
        
        # Organize by category
        by_category = {}
        for row in sentiment_data:
            if row.category_name not in by_category:
                by_category[row.category_name] = {
                    "positive": 0,
                    "neutral": 0,
                    "negative": 0
                }
            by_category[row.category_name][row.sentiment] = row.count
        
        return {
            "by_category": by_category
        }
    
    def get_notification_dispatch_performance(self) -> dict:
        """Monitor notification performance by channel and type.
        
        Returns dict with dispatch success rates by channel.
        """
        # Get notifications from last 7 days
        seven_days_ago = (datetime.now(UTC) - timedelta(days=7)).isoformat()
        
        performance = self.db.query(
            Notification.channel,
            Notification.dispatch_status,
            func.count(Notification.notification_id).label('count')
        ).filter(
            Notification.created_at >= seven_days_ago
        ).group_by(
            Notification.channel, Notification.dispatch_status
        ).all()
        
        # Organize by channel
        by_channel = {}
        for row in performance:
            if row.channel not in by_channel:
                by_channel[row.channel] = {
                    "pending": 0,
                    "sent": 0,
                    "failed": 0
                }
            by_channel[row.channel][row.dispatch_status] = row.count
        
        return {
            "by_channel": by_channel,
            "period_days": 7
        }
    
    def count_negative_sentiment_products(self) -> int:
        """Count products with majority negative reviews.
        
        Returns count of products with negative sentiment issue.
        """
        from sqlalchemy import case
        
        # Get products with at least 3 reviews where >50% are negative
        products_with_reviews = self.db.query(
            Review.product_id,
            func.count(Review.review_id).label('total_reviews'),
            func.sum(case((Review.sentiment == 'negative', 1), else_=0)).label('negative_count')
        ).group_by(
            Review.product_id
        ).having(
            func.count(Review.review_id) >= 3
        ).all()
        
        negative_products = 0
        for row in products_with_reviews:
            if row.negative_count > (row.total_reviews / 2):
                negative_products += 1
        
        return negative_products
    
    def get_ops_summary(self) -> OpsSummaryResponse:
        """Get lightweight operations summary for bootstrap endpoint.
        
        Returns OpsSummaryResponse with key KPI counts.
        """
        slot_util = self.calculate_slot_utilization()
        promo_warnings = self.get_promotion_warnings()
        negative_products = self.count_negative_sentiment_products()
        
        return OpsSummaryResponse(
            open_slot_alerts=slot_util["open_alerts"],
            promotion_warnings=promo_warnings["count"],
            negative_sentiment_products=negative_products
        )
