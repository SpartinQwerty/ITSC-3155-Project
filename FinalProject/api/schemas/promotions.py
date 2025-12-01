from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail

class PromotionBase(BaseModel):
    promo_code: str
    expiration_date: datetime
    description: Optional[str] = None
    discount_amount: float

class PromotionCreate(PromotionBase):
    pass

class PromotionUpdate(BaseModel):
    promo_code: Optional[str] = None
    expiration_date: Optional[datetime] = None
    description: Optional[str] = None
    discount_amount: Optional[float] = None

class PromotionRead(PromotionBase):
    id: int

    class ConfigDict:
        from_attributes = True