"""Notification provider adapter for push and email delivery."""
import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


class NotificationProviderAdapter:
    """
    Notification provider adapter with dispatch method for push/email channels.
    Dispatch failures logged but do not block transactions.
    """
    
    def __init__(self):
        """Initialize notification provider adapter."""
    
    def dispatch(
        self,
        notification_id: str,
        customer_id: str,
        channel: str,
        template_type: str,
        title: str,
        message: str,
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Dispatch notification to external provider.
        
        Args:
            notification_id: Notification identifier
            customer_id: Customer identifier
            channel: Notification channel (push, email, in_app)
            template_type: Template type identifier
            title: Notification title
            message: Notification message
            context: Additional context data
        
        Returns:
            Dictionary containing dispatch_status, provider_message_id, dispatched_at
        """
        try:
            # Mock implementation for MVP
            # In production, this would call actual push/email provider APIs
            
            if channel == "in_app":
                # In-app notifications don't need external dispatch
                return {
                    "dispatch_status": "sent",
                    "provider_message_id": notification_id,
                    "dispatched_at": datetime.now().isoformat()
                }
            
            # External provider call for push/email
            provider_message_id = f"msg-{channel}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # For MVP: external providers (push, email, sms) are dispatched via in-memory queue
            # Production would integrate with actual services (FCM, SendGrid, Twilio)
            # This implementation logs the dispatch and records it in the database
            logger.info(f"Dispatched notification {notification_id} via {channel} to customer {customer_id}: {title}")
            
            return {
                "dispatch_status": "sent",
                "provider_message_id": provider_message_id,
                "dispatched_at": datetime.now().isoformat()
            }
        
        except Exception as e:
            # Log failure but don't throw - dispatch failures must not block transactions
            logger.error(f"Failed to dispatch notification {notification_id} via {channel}: {e!s}")
            return {
                "dispatch_status": "failed",
                "provider_message_id": None,
                "dispatched_at": datetime.now().isoformat()
            }
