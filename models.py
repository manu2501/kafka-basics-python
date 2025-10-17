from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime


class BurgerType(str, Enum):
    CLASSIC = "Classic Burger"
    CHEESE = "Cheeseburger"
    BACON = "Bacon Burger"
    VEGGIE = "Veggie Burger"
    DOUBLE = "Double Burger"
    MUSHROOM = "Mushroom Swiss"


class BurgerSize(str, Enum):
    REGULAR = "Regular"
    LARGE = "Large"


class BurgerMenuItem(BaseModel):
    id: int
    name: BurgerType
    description: str
    price: float
    size: BurgerSize = BurgerSize.REGULAR
    is_available: bool = True


class OrderItem(BaseModel):
    burger_id: int
    quantity: int = Field(gt=0)
    special_instructions: Optional[str] = None


class Order(BaseModel):
    order_id: UUID = Field(default_factory=uuid4)
    items: List[OrderItem]
    customer_name: str
    total_amount: float
    status: str = "pending"
    created_at: datetime = Field(default_factory=datetime.now)


class OrderResponse(BaseModel):
    order_id: UUID
    status: str
    estimated_wait_time: int  # in minutes
    message: str


# Predefined menu items
MENU_ITEMS = [
    BurgerMenuItem(
        id=1,
        name=BurgerType.CLASSIC,
        description="A juicy beef patty with lettuce, tomato, and our special sauce",
        price=8.99,
    ),
    BurgerMenuItem(
        id=2,
        name=BurgerType.CHEESE,
        description="Classic burger topped with melted cheddar cheese",
        price=9.99,
    ),
    BurgerMenuItem(
        id=3,
        name=BurgerType.BACON,
        description="Crispy bacon strips with cheese and BBQ sauce",
        price=11.99,
    ),
    BurgerMenuItem(
        id=4,
        name=BurgerType.VEGGIE,
        description="Plant-based patty with fresh vegetables",
        price=10.99,
    ),
    BurgerMenuItem(
        id=5,
        name=BurgerType.DOUBLE,
        description="Double beef patties with double cheese",
        price=13.99,
    ),
    BurgerMenuItem(
        id=6,
        name=BurgerType.MUSHROOM,
        description="Sautéed mushrooms and Swiss cheese",
        price=11.99,
    ),
]
