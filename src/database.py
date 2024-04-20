import databases

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DATABASE_URL = "sqlite+aiosqlite:///./sql_app.db"

database = databases.Database(DATABASE_URL)
Base: DeclarativeBase = declarative_base()
engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(
    engine, class_=AsyncSession,
    expire_on_commit=False
)


async def get_session():
    async with async_session() as session:
        yield session
