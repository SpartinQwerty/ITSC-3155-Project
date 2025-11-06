from typing import Optional
from pydantic import BaseModel, EmailStr


class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: Optional[str] = None
    address: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None


class Customer(CustomerBase):
    id: int

    class ConfigDict:
        from_attributes = True