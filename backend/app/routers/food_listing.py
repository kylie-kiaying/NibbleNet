from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.food_listing_schemas import FoodListingCreate, FoodListingDisplay, FoodListingUpdate
from ..services.food_listing_service import create_listing, get_listing, update_listing, delete_listing, get_all_listings
from ..core.database import get_db
from ..core.security import get_current_user
from ..models.models import User

router = APIRouter()

@router.post("/", response_model=FoodListingDisplay)
async def create_food_listing(listing: FoodListingCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await create_listing(db, listing, current_user.id)

@router.get("/", response_model=list[FoodListingDisplay])
async def read_food_listings(db: AsyncSession = Depends(get_db)):
    return await get_all_listings(db)

@router.get("/{listing_id}", response_model=FoodListingDisplay)
async def read_food_listing(listing_id: int, db: AsyncSession = Depends(get_db)):
    return await get_listing(db, listing_id)

@router.put("/{listing_id}", response_model=FoodListingDisplay)
async def update_food_listing(listing_id: int, listing: FoodListingUpdate, db: AsyncSession = Depends(get_db)):
    return await update_listing(db, listing_id, listing)

@router.delete("/{listing_id}", response_model=dict)
async def delete_food_listing(listing_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_listing(db, listing_id)