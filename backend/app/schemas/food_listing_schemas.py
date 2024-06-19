from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..models.models import ListingStatus

class FoodListingBase(BaseModel):
    title: str
    description: str
    location: str

class FoodListingCreate(FoodListingBase):
    pass

class FoodListingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    status: Optional[ListingStatus] = None

class FoodListingDisplay(FoodListingBase):
    id: int
    user_id: int
    status: ListingStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
