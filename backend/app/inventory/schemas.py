from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class InventoryStatus(BaseModel):
    """Inventory status for a product"""
    inventory_id: str = Field(..., alias="inventoryId")
    product_id: str = Field(..., alias="productId")
    stock_quantity: int = Field(..., alias="stockQuantity")
    reorder_level: int = Field(..., alias="reorderLevel")
    harvest_date: datetime | None = Field(None, alias="harvestDate")
    expiry_date: datetime | None = Field(None, alias="expiryDate")
    warehouse_zone: str | None = Field(None, alias="warehouseZone")
    last_updated_at: datetime = Field(..., alias="lastUpdatedAt")
    availability_status: str = Field(..., alias="availabilityStatus")

    model_config = ConfigDict(populate_by_name=True)


class LowStockAlert(BaseModel):
    """Low stock alert for operations"""
    product_id: str = Field(..., alias="productId")
    product_name: str = Field(..., alias="productName")
    stock_quantity: int = Field(..., alias="stockQuantity")
    reorder_level: int = Field(..., alias="reorderLevel")
    availability_status: str = Field(..., alias="availabilityStatus")
    warehouse_zone: str | None = Field(None, alias="warehouseZone")

    model_config = ConfigDict(populate_by_name=True)


class ExpiryAlert(BaseModel):
    """Expiring product alert for operations"""
    product_id: str = Field(..., alias="productId")
    product_name: str = Field(..., alias="productName")
    expiry_date: datetime = Field(..., alias="expiryDate")
    days_until_expiry: int = Field(..., alias="daysUntilExpiry")
    stock_quantity: int = Field(..., alias="stockQuantity")
    warehouse_zone: str | None = Field(None, alias="warehouseZone")

    model_config = ConfigDict(populate_by_name=True)
