from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from .order_details import OrderDetail, OrderDetailCreate


class OrderBase(BaseModel):
    customer_id: Optional[int] = None
    description: Optional[str] = None


class OrderCreate(OrderBase):
    order_details: List[OrderDetailCreate]


class OrderUpdate(BaseModel):
    customer_id: Optional[int] = None
    description: Optional[str] = None
    order_details: Optional[List[OrderDetailCreate]] = None


class Order(OrderBase):
    id: int
    order_date: datetime
    total_price: float
    order_details: List[OrderDetail] = []

    class ConfigDict:
        from_attributes = True