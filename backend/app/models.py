from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum as SAEnum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from .database import Base


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(SAEnum(UserRole), nullable=False, default=UserRole.USER)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    orders = relationship("Order", back_populates="user", cascade="all,delete-orphan")


class BurgerSKU(Base):
    __tablename__ = "burger_skus"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    size = Column(String(20), nullable=False, default="REGULAR")
    is_available = Column(Boolean, nullable=False, default=True)

    order_items = relationship("OrderItem", back_populates="sku")

    __table_args__ = (
        UniqueConstraint("name", "size", name="uq_sku_name_size"),
    )


class OrderStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(SAEnum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    total_amount = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all,delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(String(36), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    sku_id = Column(Integer, ForeignKey("burger_skus.id", ondelete="RESTRICT"), nullable=False)
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")
    sku = relationship("BurgerSKU", back_populates="order_items")
