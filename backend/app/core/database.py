from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from ..models.models import Base

DATABASE_URL = "postgresql+asyncpg://myuser:mypassword@localhost/nibblenet"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async_session = SessionLocal()
    try:
        yield async_session
    except Exception:
        await async_session.rollback()
        raise
    finally:
        await async_session.close()