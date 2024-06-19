from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from ..models.models import FoodListing, ListingStatus
from ..schemas.food_listing_schemas import FoodListingCreate, FoodListingUpdate

async def create_listing(db: AsyncSession, listing_data: FoodListingCreate, user_id: int):
    new_listing = FoodListing(**listing_data.dict(), user_id=user_id, status=ListingStatus.available)
    db.add(new_listing)
    await db.commit()
    await db.refresh(new_listing)
    return new_listing

async def get_all_listings(db: AsyncSession):
    result = await db.execute(select(FoodListing))
    listings = result.scalars().all()
    return listings

async def get_listing(db: AsyncSession, listing_id: int):
    result = await db.execute(select(FoodListing).filter(FoodListing.id == listing_id))
    listing = result.scalars().first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing

async def update_listing(db: AsyncSession, listing_id: int, listing_data: FoodListingUpdate):
    async with db as session:
        result = await session.execute(select(FoodListing).filter(FoodListing.id == listing_id))
        listing = result.scalars().first()
        if not listing:
            raise HTTPException(status_code=404, detail="Listing not found")
        
        for var, value in listing_data.dict(exclude_unset=True).items():
            setattr(listing, var, value)  
        
        session.add(listing)
        await session.commit()
        await session.refresh(listing)
    return listing

async def delete_listing(db: AsyncSession, listing_id: int):
    result = await db.execute(select(FoodListing).filter(FoodListing.id == listing_id))
    listing = result.scalars().first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    db.delete(listing)
    await db.commit()
    return {"message": "Listing deleted successfully"}
