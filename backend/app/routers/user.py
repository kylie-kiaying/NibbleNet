from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from..schemas.user_schemas import UserDisplay, UserUpdate
from..services.user_service import get_user_by_id, update_user, delete_user
from..core.security import get_current_user
from..models.models import User
from..core.database import get_db

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/profile", response_model=UserDisplay)
async def get_current_user_profile(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    current_user = await get_current_user(token=token, db=db)
    return current_user

@router.put("/profile", response_model=UserDisplay)
async def update_current_user_profile(user_update: UserUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="User not found or not logged in")
    updated_user = await update_user(db, current_user.id, user_update)
    return updated_user

@router.delete("/profile")
async def delete_current_user_profile(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await delete_user(db, current_user.id)
    return {"message": "User account deleted successfully"}

@router.get("/{user_id}", response_model=UserDisplay)
async def get_user_profile(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user