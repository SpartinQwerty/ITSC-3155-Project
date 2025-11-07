from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail

class ResourceManagementBase(BaseModel):
    ingredient: str
    amount: int
    unit: str

class ResourceManagementCreate(ResourceManagementBase):
    pass

class ResourceManagementRead(ResourceManagementBase):
    id: int

    class ConfigDict:
        from_attributes = True