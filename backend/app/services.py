from sqlalchemy.orm import Session

from .models import Order, OrderStatus
from .events import publish


def notify_if_completed(db: Session, order: Order) -> None:
    db.refresh(order)
    if order.status == OrderStatus.COMPLETED:
        publish(order.user_id, {"type": "order_completed", "order_id": order.id})
