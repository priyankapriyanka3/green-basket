"""Operations response schemas."""
from pydantic import BaseModel


class OpsSummaryResponse(BaseModel):
    """Operations summary KPIs for dashboard."""
    open_slot_alerts: int
    promotion_warnings: int
    negative_sentiment_products: int
