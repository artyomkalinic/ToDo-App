import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.database.db import Base, get_db_connection
from app.main import app
from fastapi.testclient import TestClient

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db" 

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True, echo=True)
TestingSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db_connection] = override_get_db


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    async def init_models():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(init_models())
    yield

    async def drop_models():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    asyncio.run(drop_models())


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
