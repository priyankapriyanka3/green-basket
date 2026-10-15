import json
from datetime import datetime, timezone

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.catalog.schemas import (
    CatalogResponse,
    CategoryInfo,
    FarmerInfo,
    FreshnessData,
    NutritionData,
    ProductCard,
    ReviewSummary,
)
from app.models.category import Category
from app.models.farmer import Farmer
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.review import Review


class CatalogService:
    """Service for catalog browsing and product detail retrieval"""

    def __init__(self, session: Session):
        self.session = session

    def get_featured_categories(self) -> list[CategoryInfo]:
        """Retrieve featured categories"""
        categories = (
            self.session.query(Category)
            .filter(Category.is_active == "true")
            .all()
        )
        return [
            CategoryInfo(
                category_id=cat.category_id,
                name=cat.name,
                is_featured=(cat.is_active == "true"),
                parent_category_id=cat.parent_category_id,
                icon_url=cat.icon_url,
                description=cat.description,
            )
            for cat in categories
        ]

    def search_products(
        self,
        q: str | None = None,
        category_id: str | None = None,
        is_organic: bool | None = None,
        featured_only: bool = False,
        page: int = 1,
        page_size: int = 24,
    ) -> CatalogResponse:
        """Browse/search/filter products with pagination"""
        # Build query with filters
        query = self.session.query(Product)

        if q:
            search_term = f"%{q}%"
            query = query.filter(
                or_(
                    Product.name.ilike(search_term),
                    Product.description.ilike(search_term),
                )
            )

        if category_id:
            query = query.filter(Product.category_id == category_id)

        if is_organic is not None:
            query = query.filter(Product.is_organic == ("true" if is_organic else "false"))

        if featured_only:
            query = query.filter(Product.is_featured == "true")

        # Get total count before pagination
        total = query.count()

        # Apply pagination
        offset = (page - 1) * page_size
        products = query.offset(offset).limit(page_size).all()

        # Build product cards with enriched data
        product_cards = [self._build_product_card(p) for p in products]

        # Get categories for current filter (or featured if none)
        if category_id:
            category_models = (
                self.session.query(Category)
                .filter(Category.category_id == category_id)
                .all()
            )
            categories = [self._build_category_info(c) for c in category_models]
        else:
            categories = self.get_featured_categories()

        return CatalogResponse(
            categories=categories,
            products=product_cards,
            page=page,
            page_size=page_size,
            total=total,
        )

    def _build_product_card(self, product: Product) -> ProductCard:
        """Build enriched product card with nutrition, freshness, reviews, farmer"""
        # Parse nutrition from JSON
        nutrition = None
        if product.nutrition_json and product.nutrition_json != "{}":
            try:
                nutrition_dict = json.loads(product.nutrition_json)
                nutrition = NutritionData(**nutrition_dict)
            except (json.JSONDecodeError, ValueError):
                pass

        # Parse tags from JSON
        tags = []
        if product.tags_json and product.tags_json != "[]":
            try:
                tags = json.loads(product.tags_json)
            except json.JSONDecodeError:
                pass

        # Get freshness from inventory
        freshness = self._get_freshness_data(product.product_id)

        # Get review summary
        review_summary = self._get_review_summary(product.product_id)

        # Get farmer info
        farmer = None
        if product.farmer_id:
            farmer = self._get_farmer_info(product.farmer_id)

        return ProductCard(
            product_id=product.product_id,
            name=product.name,
            unit=product.unit_type or "kg",
            price_inr=f"{float(product.unit_price):.2f}",
            is_organic=(product.is_organic == "true"),
            is_featured=(product.is_featured == "true"),
            tags=tags,
            nutrition=nutrition,
            freshness=freshness,
            review_summary=review_summary,
            farmer=farmer,
        )

    def _get_freshness_data(self, product_id: str) -> FreshnessData | None:
        """Retrieve freshness indicators from inventory"""
        inventory = (
            self.session.query(Inventory)
            .filter(Inventory.product_id == product_id)
            .first()
        )

        if not inventory:
            return None

        # Parse dates
        harvest_date = None
        if inventory.harvest_date:
            try:
                # Remove trailing 'Z' if present
                date_str = inventory.harvest_date.rstrip('Z')
                harvest_date = datetime.fromisoformat(date_str)
            except (ValueError, AttributeError):
                pass

        expiry_date = None
        if inventory.expiry_date:
            try:
                # Remove trailing 'Z' if present
                date_str = inventory.expiry_date.rstrip('Z')
                expiry_date = datetime.fromisoformat(date_str)
            except (ValueError, AttributeError):
                pass

        # Calculate expiry days from product or inventory
        expiry_days = None
        if expiry_date:
            days_until_expiry = (expiry_date - datetime.now(timezone.utc)).days
            expiry_days = max(0, days_until_expiry)

        return FreshnessData(
            expiry_days=expiry_days,
            harvest_date=harvest_date,
            expiry_date=expiry_date,
            stock_quantity=inventory.stock_quantity,
            availability_status=inventory.availability_status,
        )

    def _get_review_summary(self, product_id: str) -> ReviewSummary | None:
        """Calculate review summary for product"""
        review_stats = (
            self.session.query(
                func.avg(Review.rating).label("avg_rating"),
                func.count(Review.review_id).label("count"),
            )
            .filter(Review.product_id == product_id)
            .first()
        )

        if not review_stats or review_stats.count == 0:
            return None

        # Get sentiment distribution
        sentiment_counts = (
            self.session.query(
                Review.sentiment,
                func.count(Review.review_id).label("count"),
            )
            .filter(Review.product_id == product_id)
            .group_by(Review.sentiment)
            .all()
        )

        # Determine overall sentiment
        sentiment_map = {s.sentiment: s.count for s in sentiment_counts}
        positive_count = sentiment_map.get("positive", 0)
        negative_count = sentiment_map.get("negative", 0)

        if positive_count > negative_count * 2:
            overall_sentiment = "positive"
        elif negative_count > positive_count * 2:
            overall_sentiment = "negative"
        else:
            overall_sentiment = "neutral"

        return ReviewSummary(
            average_rating=float(review_stats.avg_rating or 0),
            sentiment=overall_sentiment,
            review_count=review_stats.count,
        )

    def _get_farmer_info(self, farmer_id: str) -> FarmerInfo | None:
        """Retrieve farmer/source information"""
        farmer = (
            self.session.query(Farmer)
            .filter(Farmer.farmer_id == farmer_id)
            .first()
        )

        if not farmer:
            return None

        return FarmerInfo(
            farmer_id=farmer.farmer_id,
            name=farmer.name,
            is_verified=(farmer.certification_type is not None),
            is_organic_certified=("organic" in (farmer.certification_type or "").lower()),
        )

    def _build_category_info(self, category: Category) -> CategoryInfo:
        """Build CategoryInfo from Category model"""
        return CategoryInfo(
            category_id=category.category_id,
            name=category.name,
            is_featured=(category.is_active == "true"),
            parent_category_id=category.parent_category_id,
            icon_url=category.icon_url,
            description=category.description,
        )

    def get_low_stock_products(self, threshold: int | None = None) -> list[dict]:
        """Operational: get products with low stock or expiring soon"""
        query = (
            self.session.query(Product, Inventory)
            .join(Inventory, Product.product_id == Inventory.product_id)
            .filter(Inventory.availability_status.in_(["low_stock", "unavailable"]))
        )

        results = []
        for product, inventory in query.all():
            results.append({
                "product_id": product.product_id,
                "name": product.name,
                "stock_quantity": inventory.stock_quantity,
                "reorder_level": inventory.reorder_level,
                "availability_status": inventory.availability_status,
                "expiry_date": inventory.expiry_date,
            })

        return results
