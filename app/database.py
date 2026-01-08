from sqlalchemy.ext.declarative import declarative_base
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

from core.config import DATABASE_URL

connect_args = {}

if "neon.tech" in DATABASE_URL:
    connect_args["ssl"] = True

engine = create_async_engine(DATABASE_URL, echo=False, future=True, connect_args=connect_args)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async with AsyncSession(engine) as session:
        yield session