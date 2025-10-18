from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime
import json
from confluent_kafka import Producer

from services.shared.models import BurgerMenuItem, Order, OrderItem, OrderResponse, MENU_ITEMS
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(title="User Service", description="User-facing API for burger orders", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os
producer = Producer({"bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")})


def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(f"Delivered to {msg.topic()} [{msg.partition()}] @ {msg.offset()}")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/menu", response_model=List[BurgerMenuItem])
async def get_menu():
    return MENU_ITEMS


class OrderRequest(BaseModel):
    items: List[OrderItem]
    customer_name: str


@app.post("/order", response_model=OrderResponse)
async def place_order(order_req: OrderRequest):
    total = 0.0
    for item in order_req.items:
        burger = next((m for m in MENU_ITEMS if m.id == item.burger_id), None)
        if burger is None:
            raise HTTPException(status_code=400, detail=f"Invalid burger_id: {item.burger_id}")
        if not burger.is_available:
            raise HTTPException(status_code=400, detail=f"Burger {burger.name} unavailable")
        total += burger.price * item.quantity

    order = Order(
        order_id=uuid4(),
        items=order_req.items,
        customer_name=order_req.customer_name,
        total_amount=total,
        status="pending",
        created_at=datetime.now(),
    )

    try:
        payload = order.model_dump()
        payload["order_id"] = str(payload["order_id"])  # UUID to str
        payload["created_at"] = payload["created_at"].isoformat()
        producer.produce("burger-orders", value=json.dumps(payload).encode("utf-8"))
        producer.flush(5)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kafka error: {e}")

    return OrderResponse(
        order_id=order.order_id,
        status="accepted",
        estimated_wait_time=15,
        message="Order accepted",
    )

# serve static dashboard
app.mount("/", StaticFiles(directory=str(Path(__file__).parent / "static"), html=True), name="static")
