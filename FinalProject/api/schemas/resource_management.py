from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ResourceManagementBase(BaseModel):
    ingredient: str
    amount: int
    unit: str

class ResourceManagementCreate(ResourceManagementBase):
    pass

class ResourceManagementUpdate(BaseModel):
    ingredient: Optional[str] = None
    amount: Optional[int] = None
    unit: Optional[str] = None

class ResourceManagementRead(ResourceManagementBase):
    id: int

    class ConfigDict:
        from_attributes = True