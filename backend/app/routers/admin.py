from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import schemas
from ..models import BurgerSKU, Order, OrderItem, OrderStatus
from ..services import notify_if_completed
from ..deps import get_db, require_admin

router = APIRouter(prefix="/admin", tags=["admin"]) 


@router.get("/skus", response_model=List[schemas.BurgerSKUOut])
def list_skus(db: Session = Depends(get_db), _: None = Depends(require_admin)):
    return db.query(BurgerSKU).order_by(BurgerSKU.id).all()


@router.post("/skus", response_model=schemas.BurgerSKUOut)
def create_sku(payload: schemas.BurgerSKUCreate, db: Session = Depends(get_db), _: None = Depends(require_admin)):
    sku = BurgerSKU(**payload.model_dump())
    db.add(sku)
    db.commit()
    db.refresh(sku)
    return sku


@router.put("/skus/{sku_id}", response_model=schemas.BurgerSKUOut)
def update_sku(sku_id: int, payload: schemas.BurgerSKUUpdate, db: Session = Depends(get_db), _: None = Depends(require_admin)):
    sku = db.get(BurgerSKU, sku_id)
    if not sku:
        raise HTTPException(status_code=404, detail="SKU not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(sku, field, value)
    db.commit()
    db.refresh(sku)
    return sku


@router.get("/orders", response_model=List[schemas.OrderOut])
def list_orders(db: Session = Depends(get_db), _: None = Depends(require_admin)):
    orders = db.query(Order).order_by(Order.created_at.desc()).all()
    # Ensure items loaded
    for o in orders:
        _ = o.items
    return orders


@router.put("/orders/{order_id}", response_model=schemas.OrderOut)
def update_order(order_id: str, payload: schemas.OrderStatusUpdate, db: Session = Depends(get_db), _: None = Depends(require_admin)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    try:
        order.status = OrderStatus(payload.status)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid status")
    db.commit()
    db.refresh(order)
    notify_if_completed(db, order)
    return order
