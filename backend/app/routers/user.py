from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import schemas
from ..models import BurgerSKU, Order, OrderItem, OrderStatus, User
from ..deps import get_db, get_current_user

router = APIRouter(prefix="/user", tags=["user"]) 


@router.get("/menu", response_model=List[schemas.BurgerSKUOut])
def get_menu(db: Session = Depends(get_db)):
    return db.query(BurgerSKU).filter(BurgerSKU.is_available == True).order_by(BurgerSKU.id).all()


@router.post("/order", response_model=schemas.OrderOut)
def place_order(payload: schemas.OrderCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    skus = db.query(BurgerSKU).filter(BurgerSKU.id.in_([i.sku_id for i in payload.items])).all()
    sku_map = {sku.id: sku for sku in skus}
    if len(sku_map) != len(payload.items):
        raise HTTPException(status_code=400, detail="Invalid SKU in items")

    total = 0.0
    for item in payload.items:
        sku = sku_map[item.sku_id]
        if not sku.is_available:
            raise HTTPException(status_code=400, detail=f"SKU {sku.id} unavailable")
        total += sku.price * item.quantity

    order = Order(user_id=user.id, total_amount=total, status=OrderStatus.PENDING)
    db.add(order)
    db.flush()

    for item in payload.items:
        db.add(OrderItem(order_id=order.id, sku_id=item.sku_id, quantity=item.quantity))

    db.commit()
    db.refresh(order)
    return order


@router.get("/orders", response_model=List[schemas.OrderOut])
def my_orders(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    orders = (
        db.query(Order)
        .filter(Order.user_id == user.id)
        .order_by(Order.created_at.desc())
        .all()
    )
    for o in orders:
        _ = o.items
    return orders
