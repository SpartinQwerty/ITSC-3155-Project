from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from decimal import Decimal


class ReviewBase(BaseModel):
    customer_id: int
    order_id: Optional[int] = None
    review_text: Optional[str] = None
    score: Decimal = Field(..., ge=0.0, le=5.0, description="Rating from 0.0 to 5.0")


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    review_text: Optional[str] = None
    score: Optional[Decimal] = Field(None, ge=0.0, le=5.0, description="Rating from 0.0 to 5.0")


class Review(ReviewBase):
    id: int
    review_date: datetime

    class ConfigDict:
        from_attributes = True