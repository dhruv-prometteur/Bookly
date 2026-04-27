from typing import AsyncGenerator

from sqlmodel import create_engine
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from src.config import Config
from sqlalchemy.orm import sessionmaker





async_engine = create_async_engine(
    url=Config.DataBase_URL,
    echo=False,

)

async def init_db():
    async with async_engine.begin() as conn:
        from src.db.models import Book
        from src.db.models import User
        await conn.run_sync(Book.metadata.create_all)
        await conn.run_sync(User.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    Session=sessionmaker(bind=async_engine,class_=AsyncSession,expire_on_commit=False)

    async with Session() as session:
        yield session


        

 