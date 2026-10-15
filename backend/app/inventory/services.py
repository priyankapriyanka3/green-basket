from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from app.inventory.schemas import (
    ExpiryAlert,
    InventoryStatus,
    LowStockAlert,
)
from app.models.inventory import Inventory
from app.models.product import Product


class InventoryService:
    """Service for inventory tracking and freshness monitoring"""

    def __init__(self, session: Session):
        self.session = session

    def get_inventory_status(self, product_id: str) -> InventoryStatus | None:
        """Get inventory status for a product"""
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
                harvest_date = datetime.fromisoformat(inventory.harvest_date)
            except (ValueError, AttributeError):
                pass

        expiry_date = None
        if inventory.expiry_date:
            try:
                expiry_date = datetime.fromisoformat(inventory.expiry_date)
            except (ValueError, AttributeError):
                pass

        last_updated_at = datetime.fromisoformat(inventory.last_updated_at)

        return InventoryStatus(
            inventory_id=inventory.inventory_id,
            product_id=inventory.product_id,
            stock_quantity=inventory.stock_quantity,
            reorder_level=inventory.reorder_level,
            harvest_date=harvest_date,
            expiry_date=expiry_date,
            warehouse_zone=inventory.warehouse_zone,
            last_updated_at=last_updated_at,
            availability_status=inventory.availability_status,
        )

    def update_availability_status(
        self,
        product_id: str,
        stock_quantity: int | None = None,
    ) -> None:
        """
        Update inventory availability status based on stock levels
        
        Rules:
        - available: stock > reorder_level
        - low_stock: 0 < stock <= reorder_level
        - unavailable: stock == 0
        """
        inventory = (
            self.session.query(Inventory)
            .filter(Inventory.product_id == product_id)
            .first()
        )

        if not inventory:
            return

        if stock_quantity is not None:
            inventory.stock_quantity = stock_quantity

        # Determine availability status
        if inventory.stock_quantity == 0:
            inventory.availability_status = "unavailable"
        elif inventory.stock_quantity <= inventory.reorder_level:
            inventory.availability_status = "low_stock"
        else:
            inventory.availability_status = "available"

        inventory.last_updated_at = datetime.now(UTC).isoformat() + "Z"

        self.session.commit()

    def get_low_stock_alerts(self, threshold_multiplier: float = 1.0) -> list[LowStockAlert]:
        """
        Get products with low stock or unavailable status
        
        Used by operations to monitor inventory and trigger reorders
        """
        query = (
            self.session.query(Inventory, Product)
            .join(Product, Inventory.product_id == Product.product_id)
            .filter(
                Inventory.availability_status.in_(["low_stock", "unavailable"])
            )
        )

        alerts = []
        for inventory, product in query.all():
            alerts.append(
                LowStockAlert(
                    product_id=product.product_id,
                    product_name=product.name,
                    stock_quantity=inventory.stock_quantity,
                    reorder_level=inventory.reorder_level,
                    availability_status=inventory.availability_status,
                    warehouse_zone=inventory.warehouse_zone,
                )
            )

        return alerts

    def get_expiry_alerts(self, days_threshold: int = 7) -> list[ExpiryAlert]:
        """
        Get products expiring within threshold days
        
        Used by operations to monitor freshness and prevent waste
        """
        now = datetime.now(UTC)
        threshold_date = now + timedelta(days=days_threshold)

        query = (
            self.session.query(Inventory, Product)
            .join(Product, Inventory.product_id == Product.product_id)
            .filter(Inventory.expiry_date.isnot(None))
        )

        alerts = []
        for inventory, product in query.all():
            if not inventory.expiry_date:
                continue

            try:
                expiry_dt = datetime.fromisoformat(inventory.expiry_date)
            except (ValueError, AttributeError):
                continue

            # Check if expiring within threshold
            if expiry_dt <= threshold_date:
                days_until_expiry = (expiry_dt - now).days

                alerts.append(
                    ExpiryAlert(
                        product_id=product.product_id,
                        product_name=product.name,
                        expiry_date=expiry_dt,
                        days_until_expiry=max(0, days_until_expiry),
                        stock_quantity=inventory.stock_quantity,
                        warehouse_zone=inventory.warehouse_zone,
                    )
                )

        # Sort by days until expiry (most urgent first)
        alerts.sort(key=lambda x: x.days_until_expiry)

        return alerts

    def calculate_freshness_indicator(
        self,
        inventory: Inventory,
    ) -> tuple[str, str]:
        """
        Calculate freshness indicator and color for display
        
        Returns:
        - (indicator_text, color_code)
        
        Colors:
        - green: fresh, harvested recently
        - marigold: expiring soon or low stock
        - grey: unavailable
        """
        if inventory.availability_status == "unavailable":
            return ("Unavailable", "grey")

        if inventory.availability_status == "low_stock":
            return (f"Low stock: {inventory.stock_quantity} left", "marigold")

        # Check harvest date first (prioritize freshness indicator for recently harvested)
        if inventory.harvest_date:
            try:
                harvest_dt = datetime.fromisoformat(inventory.harvest_date)
                days_since_harvest = (datetime.now(UTC) - harvest_dt).days

                if days_since_harvest <= 2:
                    harvest_str = harvest_dt.strftime("%d %b")

                    # Calculate best-within days from expiry if available
                    if inventory.expiry_date:
                        expiry_dt = datetime.fromisoformat(inventory.expiry_date)
                        best_within_days = (expiry_dt - harvest_dt).days
                        return (f"Harvested {harvest_str}, best within {best_within_days} days", "green")
                    else:
                        return (f"Harvested {harvest_str}", "green")
            except (ValueError, AttributeError):
                pass

        # Check expiry (only if not recently harvested)
        if inventory.expiry_date:
            try:
                expiry_dt = datetime.fromisoformat(inventory.expiry_date)
                days_until_expiry = (expiry_dt - datetime.now(UTC)).days

                if days_until_expiry <= 1:
                    return (f"Expires in {days_until_expiry} day(s)", "marigold")
                elif days_until_expiry <= 7:
                    return (f"Expires in {days_until_expiry} days", "marigold")
            except (ValueError, AttributeError):
                pass

        # Default to available
        return ("Available", "green")
