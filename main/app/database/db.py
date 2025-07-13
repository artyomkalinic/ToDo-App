import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

url = os.getenv("DATABASE_URL")
engine = create_async_engine(url, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False, autocommit=False
)

Base = declarative_base()

async def get_db_connection():
    async with AsyncSessionLocal() as session:
        yield session
