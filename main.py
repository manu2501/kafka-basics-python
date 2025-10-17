from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn
from models import BurgerMenuItem, Order, OrderItem, OrderResponse, MENU_ITEMS
from producer import send_order_to_kafka
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime

app = FastAPI(
    title="Burger Kiosk API",
    description="FastAPI-based burger kiosk with Kafka message queue",
    version="1.0.0",
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to the Burger Kiosk!",
        "endpoints": {
            "GET /menu": "View all available burgers",
            "GET /menu/{burger_id}": "Get details of a specific burger",
            "POST /order": "Place a new burger order",
        },
    }


@app.get("/menu", response_model=List[BurgerMenuItem])
async def get_menu():
    """Get the full menu of available burgers"""
    return MENU_ITEMS


@app.get("/menu/{burger_id}", response_model=BurgerMenuItem)
async def get_burger(burger_id: int):
    """Get details of a specific burger by ID"""
    for burger in MENU_ITEMS:
        if burger.id == burger_id:
            return burger
    raise HTTPException(status_code=404, detail="Burger not found")


class OrderRequest(BaseModel):
    items: List[OrderItem]
    customer_name: str


@app.post("/order", response_model=OrderResponse)
async def place_order(order_req: OrderRequest):
    """Place a new burger order"""
    total = 0.0
    for item in order_req.items:
        burger = None
        for menu_item in MENU_ITEMS:
            if menu_item.id == item.burger_id:
                burger = menu_item
                break
        if not burger:
            raise HTTPException(
                status_code=400, detail=f"Invalid burger_id: {item.burger_id}"
            )
        if not burger.is_available:
            raise HTTPException(
                status_code=400, detail=f"Burger {burger.name} is currently unavailable"
            )
        total += burger.price * item.quantity

    order = Order(
        order_id=uuid4(),
        items=order_req.items,
        customer_name=order_req.customer_name,
        total_amount=total,
        status="pending",
        created_at=datetime.now(),
    )

    success = await send_order_to_kafka(order)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to process order")

    return OrderResponse(
        order_id=order.order_id,
        status="accepted",
        estimated_wait_time=15,
        message="Your order has been accepted and is being processed",
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
