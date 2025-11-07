from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail

class PaymentsBase(BaseModel):
    customer_name: str
    payment_type: str
    transaction_status: str
    card_info: int
    card_date: str
    card_pin: int

class PaymentsCreate(PaymentsBase):
    pass

class PaymentsUpdate(PaymentsBase):
    customer_name: Optional[str]
    payment_type: Optional[str]
    transaction_status: Optional[str]
    card_info: Optional[int]
    card_date: Optional[str]
    card_pin: Optional[int]


class Payments(PaymentsBase):
    id: int
