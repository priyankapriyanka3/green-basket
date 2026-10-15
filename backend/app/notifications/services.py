"""Notification service layer with multi-channel dispatch."""
import logging
from datetime import datetime

from sqlalchemy.orm import Session

from app.adapters.notification_provider import NotificationProviderAdapter
from app.models.notification import Notification

logger = logging.getLogger(__name__)


class NotificationService:
    """
    Notification service with dispatch method for push/email/in_app channels.
    Dispatch failures logged but do not block transactions.
    """
    
    def __init__(self, db: Session):
        """Initialize notification service."""
        self.db = db
        self.notification_adapter = NotificationProviderAdapter()
    
    def generate_notification(
        self,
        customer_id: str,
        notification_type: str,
        title: str,
        message: str,
        channel: str,
        order_id: str | None = None
    ) -> Notification:
        """
        Generate and persist notification record.
        
        Args:
            customer_id: Customer identifier
            notification_type: Notification type (order_update, delivery_update, etc.)
            title: Notification title
            message: Notification message
            channel: Channel (push, email, in_app)
            order_id: Optional order identifier
        
        Returns:
            Created notification record
        """
        # Generate notification ID
        notification_id = f"ntf-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        
        # Create notification record
        notification = Notification(
            notification_id=notification_id,
            customer_id=customer_id,
            order_id=order_id,
            type=notification_type,
            title=title,
            message=message,
            channel=channel,
            is_read="false",
            dispatch_status="pending",
            created_at=datetime.now().isoformat()
        )
        
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        
        return notification
    
    def dispatch_notification(self, notification: Notification) -> bool:
        """
        Dispatch notification to external provider.
        
        Args:
            notification: Notification record to dispatch
        
        Returns:
            True if dispatch successful, False otherwise
        """
        try:
            # Call notification provider adapter
            dispatch_result = self.notification_adapter.dispatch(
                notification_id=notification.notification_id,
                customer_id=notification.customer_id,
                channel=notification.channel,
                template_type=notification.type,
                title=notification.title,
                message=notification.message,
                context={"order_id": notification.order_id}
            )
            
            # Update dispatch status
            notification.dispatch_status = dispatch_result["dispatch_status"]
            self.db.commit()
            
            logger.info(f"Dispatched notification {notification.notification_id} with status {dispatch_result['dispatch_status']}")
            
            return dispatch_result["dispatch_status"] == "sent"
        
        except Exception as e:
            # Log failure but don't throw - dispatch failures must not block transactions
            logger.error(f"Failed to dispatch notification {notification.notification_id}: {e!s}")
            notification.dispatch_status = "failed"
            self.db.commit()
            return False
    
    def generate_order_notification(
        self,
        customer_id: str,
        order_id: str,
        event_type: str,
        channels: list[str] | None = None
    ):
        """
        Generate notifications for order/payment events.
        
        Notification trigger generation within 60-second target.
        
        Args:
            customer_id: Customer identifier
            order_id: Order identifier
            event_type: Event type (order_confirmed, payment_success, etc.)
            channels: Notification channels (default: push, in_app)
        """
        if channels is None:
            channels = ["push", "in_app"]
        
        # Determine notification content based on event type
        title_map = {
            "order_confirmed": "Order Confirmed",
            "payment_success": "Payment Successful",
            "order_packed": "Order Packed",
            "order_dispatched": "Out for Delivery",
            "order_delivered": "Order Delivered"
        }
        
        message_map = {
            "order_confirmed": f"Your order {order_id} has been confirmed.",
            "payment_success": f"Payment for order {order_id} was successful.",
            "order_packed": f"Your order {order_id} has been packed.",
            "order_dispatched": f"Your order {order_id} is out for delivery.",
            "order_delivered": f"Your order {order_id} has been delivered."
        }
        
        title = title_map.get(event_type, "Order Update")
        message = message_map.get(event_type, f"Update for order {order_id}")
        
        # Generate and dispatch notifications for each channel
        for channel in channels:
            notification = self.generate_notification(
                customer_id=customer_id,
                notification_type="order_update",
                title=title,
                message=message,
                channel=channel,
                order_id=order_id
            )
            
            # Dispatch if not in_app (in_app notifications don't need external dispatch)
            if channel != "in_app":
                self.dispatch_notification(notification)
    
    def get_customer_notifications(
        self,
        customer_id: str,
        limit: int = 20,
        unread_only: bool = False
    ) -> list[Notification]:
        """
        Get notifications for a customer.
        
        Args:
            customer_id: Customer identifier
            limit: Maximum number of notifications to return
            unread_only: If True, return only unread notifications
        
        Returns:
            List of notification records
        """
        query = self.db.query(Notification).filter(
            Notification.customer_id == customer_id
        )
        
        if unread_only:
            query = query.filter(Notification.is_read == "false")
        
        notifications = query.order_by(Notification.created_at.desc()).limit(limit).all()
        
        return notifications
    
    def mark_notification_read(self, notification_id: str, customer_id: str) -> bool:
        """
        Mark notification as read.
        
        Args:
            notification_id: Notification identifier
            customer_id: Customer identifier (for ownership check)
        
        Returns:
            True if marked read, False if not found or not owned
        """
        notification = self.db.query(Notification).filter(
            Notification.notification_id == notification_id,
            Notification.customer_id == customer_id
        ).first()
        
        if not notification:
            return False
        
        notification.is_read = "true"
        self.db.commit()
        
        return True
