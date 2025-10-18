from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class BurgerSKUBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    size: str = "REGULAR"
    is_available: bool = True


class BurgerSKUCreate(BurgerSKUBase):
    pass


class BurgerSKUUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    size: Optional[str] = None
    is_available: Optional[bool] = None


class BurgerSKUOut(BurgerSKUBase):
    id: int

    class Config:
        from_attributes = True


class OrderItemIn(BaseModel):
    sku_id: int
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    items: List[OrderItemIn]


class OrderItemOut(BaseModel):
    sku_id: int
    quantity: int


class OrderOut(BaseModel):
    id: str
    user_id: int
    status: str
    total_amount: float
    created_at: datetime
    items: List[OrderItemOut]

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: str
