"""Loyalty and orders list API routes."""
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.order import Order

router = APIRouter()


@router.get("/api/v1/loyalty")
def get_loyalty_data(
    current_user: tuple = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get loyalty points and transaction history for authenticated customer."""
    customer, _role = current_user
    
    # Get loyalty transactions from order history
    orders = db.query(Order).filter(
        Order.customer_id == customer.customer_id,
        Order.status.in_(["delivered", "completed"])
    ).order_by(Order.order_date.desc()).limit(20).all()
    
    transactions = []
    for order in orders:
        # Calculate points earned (1 point per ₹10 spent)
        points_earned = int(float(order.final_amount) / 10)
        transactions.append({
            "transaction_id": f"txn-{order.order_id}",
            "points_change": points_earned,
            "balance_after": customer.loyalty_points,
            "reason": f"Order {order.order_id}",
            "created_at": order.order_date
        })
    
    # Determine tier based on points
    tier = "Bronze"
    if customer.loyalty_points >= 1000:
        tier = "Platinum"
    elif customer.loyalty_points >= 500:
        tier = "Gold"
    elif customer.loyalty_points >= 200:
        tier = "Silver"
    
    return {
        "balance": customer.loyalty_points,
        "tier": tier,
        "transactions": transactions
    }


@router.get("/api/v1/orders")
def get_orders_list(
    current_user: tuple = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of orders for authenticated customer."""
    customer, _role = current_user
    
    orders = db.query(Order).filter(
        Order.customer_id == customer.customer_id
    ).order_by(Order.order_date.desc()).all()
    
    orders_list = []
    for order in orders:
        # Count items in this order
        items_count = db.execute(
            text("""
            SELECT COUNT(*) 
            FROM order_items 
            WHERE order_id = :order_id
            """),
            {"order_id": order.order_id}
        ).scalar() or 0
        
        orders_list.append({
            "order_id": order.order_id,
            "status": order.status,
            "total_amount": float(order.final_amount),
            "created_at": order.order_date,
            "items_count": items_count
        })
    
    return {"orders": orders_list}
