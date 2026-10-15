from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NutritionData(BaseModel):
    """Structured nutrition information"""
    calories: float | None = None
    protein_g: float | None = Field(None, alias="proteinG")
    carbs_g: float | None = Field(None, alias="carbsG")
    fat_g: float | None = Field(None, alias="fatG")
    fiber_g: float | None = Field(None, alias="fiberG")
    potassium_mg: float | None = Field(None, alias="potassiumMg")
    vitamin_c_mg: float | None = Field(None, alias="vitaminCMg")

    model_config = ConfigDict(populate_by_name=True)


class FreshnessData(BaseModel):
    """Freshness indicators from inventory"""
    expiry_days: int | None = Field(None, alias="expiryDays")
    harvest_date: datetime | None = Field(None, alias="harvestDate")
    expiry_date: datetime | None = Field(None, alias="expiryDate")
    stock_quantity: int = Field(..., alias="stockQuantity")
    availability_status: str = Field(..., alias="availabilityStatus")

    model_config = ConfigDict(populate_by_name=True)


class ReviewSummary(BaseModel):
    """Aggregated review statistics"""
    average_rating: float = Field(..., alias="averageRating")
    sentiment: str
    review_count: int = Field(..., alias="reviewCount")

    model_config = ConfigDict(populate_by_name=True)


class FarmerInfo(BaseModel):
    """Farmer/source information"""
    farmer_id: str = Field(..., alias="farmerId")
    name: str
    is_verified: bool = Field(..., alias="isVerified")
    is_organic_certified: bool = Field(..., alias="isOrganicCertified")

    model_config = ConfigDict(populate_by_name=True)


class ProductCard(BaseModel):
    """Product listing card"""
    product_id: str = Field(..., alias="productId")
    name: str
    unit: str
    price_inr: str = Field(..., alias="priceInr")
    is_organic: bool = Field(..., alias="isOrganic")
    is_featured: bool = Field(..., alias="isFeatured")
    tags: list[str]
    nutrition: NutritionData | None = None
    freshness: FreshnessData | None = None
    review_summary: ReviewSummary | None = Field(None, alias="reviewSummary")
    farmer: FarmerInfo | None = None

    model_config = ConfigDict(populate_by_name=True)


class CategoryInfo(BaseModel):
    """Category information"""
    category_id: str = Field(..., alias="categoryId")
    name: str
    is_featured: bool = Field(..., alias="isFeatured")
    parent_category_id: str | None = Field(None, alias="parentCategoryId")
    icon_url: str | None = Field(None, alias="iconUrl")
    description: str | None = None

    model_config = ConfigDict(populate_by_name=True)


class CatalogResponse(BaseModel):
    """Catalog browse/search response"""
    categories: list[CategoryInfo]
    products: list[ProductCard]
    page: int
    page_size: int = Field(..., alias="pageSize")
    total: int

    model_config = ConfigDict(populate_by_name=True)
