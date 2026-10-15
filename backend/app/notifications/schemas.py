"""Notification request and response schemas."""

from pydantic import BaseModel


class NotificationResponse(BaseModel):
    """Notification response."""
    notification_id: str
    customer_id: str
    order_id: str | None = None
    type: str
    title: str
    message: str
    channel: str
    is_read: bool
    dispatch_status: str
    created_at: str


class NotificationListResponse(BaseModel):
    """Notification list response."""
    notifications: list[NotificationResponse]
    total: int
    unread_count: int
