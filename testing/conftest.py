import pytest
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession

from bot. import main, routes_registration
from bot.config import config


@pytest.fixture
def event_loop():
    return asyncio.get_event_loop()

@pytest.fixture
async def bot() -> Bot:
    bot = Bot(token=config['testing'].BOT_TOKEN, session=AiohttpSession(), default=DefaultBotProperties())
    yield bot
    await bot.session.close()

@pytest.fixture
async def dispatcher(bot: Bot) -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())
    dp = routes_registration(dp)
    yield dp
    await dp.storage.close()
    await dp.storage.wait_closed()
