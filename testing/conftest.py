from asyncio import get_event_loop
import pytest
import pytest_asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import Redis, RedisStorage
import redis
from decouple import config

from .mocked_bot import MockedBot
from ..bot.tools.db import DataManager


# ===== STORAGES ======
@pytest_asyncio.fixture(scope="session")
async def memory_storage():
    storage = MemoryStorage()
    try:
        yield storage
    finally:
        await storage.close()

@pytest.fixture()
async def redis_storage():
    storage = RedisStorage(Redis(
            host=config("REDIS_HOST"), 
            port=config("REDIS_PORT"), 
            db=config("REDIS_DB_INDEX")
        ))
    try:
        return storage
    finally:
        await storage.close()
# ===== END =====

# ===== BOT =====
@pytest.fixture()
def bot():
    return MockedBot()


@pytest_asyncio.fixture()
async def dispatcher():
    dp = Dispatcher()
    await dp.emit_startup()
    try:
        yield dp
    finally:
        await dp.emit_shutdown()


@pytest.fixture(scope="session")
def even_loop():
    return get_event_loop()
# ===== END =====

# ===== DataManager =====
@pytest_asyncio.fixture
async def damage(scope="session"):
    damage = DataManager()
    damage.get_conn()
    await damage.create_temp_db()
    try:
        yield damage
    finally:
        await damage.conn.flushall()
        await damage.conn.aclose()
# ===== END =====