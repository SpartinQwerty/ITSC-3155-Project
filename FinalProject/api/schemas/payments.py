from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail

class PaymentsBase(BaseModel):
    payment_type: str
    transaction_status: str
    card_info: str
    card_date: str
    card_pin: str


class PaymentsCreate(PaymentsBase):
    customer_id: int  # only required on CREATE


class PaymentsUpdate(BaseModel):
    customer_id: Optional[int] = None
    payment_type: Optional[str] = None
    transaction_status: Optional[str] = None
    card_info: Optional[str] = None
    card_date: Optional[str] = None
    card_pin: Optional[str] = None


class Payments(PaymentsBase):
    id: int
    customer_id: int   # response must show it

