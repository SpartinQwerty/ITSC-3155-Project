from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail


class MenuBase(BaseModel):
    dish: str
    ingredients: str
    price: float
    calories: float
    category: str
    description: Optional[str] = None
    is_vegetarian: Optional[bool] = None


class MenuCreate(MenuBase):
    pass


class MenuUpdate(BaseModel):
    dish: Optional[str]
    ingredients: Optional[str]
    price: Optional[float]
    calories: Optional[float]
    category: Optional[str]
    description: Optional[str] = None
    is_vegetarian: Optional[bool] = None

class Menu(MenuBase):
    id: int

    class ConfigDict:
        from_attributes = True
