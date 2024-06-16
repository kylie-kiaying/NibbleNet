from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.user_schemas import UserCreate, UserLogin, UserDisplay
from ..services.user_service import create_user, get_user_by_email, verify_password
from ..core.database import get_db
from ..core.security import create_access_token

router = APIRouter()

@router.post("/register", response_model=UserDisplay)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await create_user(db, user)

@router.post("/login", response_model=dict)
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(db, email=credentials.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(credentials.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    access_token = create_access_token(data={"sub": db_user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }