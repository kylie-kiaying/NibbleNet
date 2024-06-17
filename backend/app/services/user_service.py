from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from ..models.models import User
from ..schemas.user_schemas import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 
    
async def get_user_by_email(db: AsyncSession, email: str):
    async with db as session:
        result = await session.execute(select(User).filter(User.email == email))
        return result.scalars().first()
    
async def get_user_by_id(db: AsyncSession, user_id: int):
    async with db as session:
        result = await session.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()

async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    async with db as session:
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
    return db_user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.username is not None:
        user.username = user_update.username
    if user_update.password is not None:
        user.hashed_password = pwd_context.hash(user_update.password)
    if user_update.profile_picture_url is not None:
        user.profile_picture_url = user_update.profile_picture_url

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(db: AsyncSession, user_id: int):
    async with db as session:
        user = await get_user_by_id(db, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        await session.delete(user)
        await session.commit()