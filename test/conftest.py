import asyncio
from typing import AsyncGenerator

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.main import app
from src.database.db import AsyncSessionLocal, get_async_session


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session

@pytest.fixture(scope='session')
async def async_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
        await session.close()

@pytest.fixture(scope="session", autouse=True)
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    redis = aioredis.from_url(
        'redis://localhost',
        encoding='utf-8',
        decode_response=True
    )
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac
    await redis.close()
