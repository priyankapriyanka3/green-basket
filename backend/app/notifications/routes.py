"""Notification API routes."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.notifications.schemas import NotificationListResponse, NotificationResponse
from app.notifications.services import NotificationService

router = APIRouter()


@router.get("/", response_model=NotificationListResponse)
def get_notifications(
    unread_only: bool = Query(False, description="Return only unread notifications"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of notifications"),
    current_user: tuple = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get notifications for authenticated customer."""
    customer, _role = current_user
    
    service = NotificationService(db)
    notifications = service.get_customer_notifications(
        customer_id=customer.customer_id,
        limit=limit,
        unread_only=unread_only
    )
    
    # Count unread notifications
    all_notifications = service.get_customer_notifications(customer_id=customer.customer_id, limit=1000)
    unread_count = sum(1 for n in all_notifications if n.is_read == "false")
    
    return NotificationListResponse(
        notifications=[
            NotificationResponse(
                notification_id=n.notification_id,
                customer_id=n.customer_id,
                order_id=n.order_id,
                type=n.type,
                title=n.title,
                message=n.message,
                channel=n.channel,
                is_read=n.is_read == "true",
                dispatch_status=n.dispatch_status,
                created_at=n.created_at
            )
            for n in notifications
        ],
        total=len(all_notifications),
        unread_count=unread_count
    )


@router.post("/{notification_id}/read")
def mark_notification_read(
    notification_id: str,
    current_user: tuple = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark notification as read."""
    customer, _role = current_user
    
    service = NotificationService(db)
    success = service.mark_notification_read(notification_id, customer.customer_id)
    
    return {"success": success}
