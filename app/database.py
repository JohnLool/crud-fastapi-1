import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, create_engine, text
from config import settings
from models import metadata_obj


engine = create_async_engine(
    url=settings.database_url,
    echo = True
)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(metadata_obj.create_all)