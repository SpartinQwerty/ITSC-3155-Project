from pydantic import BaseModel
from typing import Optional


class OrderDetailBase(BaseModel):
    dish_id: int
    amount: int


class OrderDetailCreate(OrderDetailBase):
    pass


class OrderDetailUpdate(BaseModel):
    dish_id: Optional[int] = None
    amount: Optional[int] = None


class OrderDetail(OrderDetailBase):
    id: int

    class ConfigDict:
        from_attributes = True