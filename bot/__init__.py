import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.redis import RedisStorage, Redis

from decouple import config

from .handlers import *
from .tools.middlewares import AccessMiddleware
from .tools.db import DataManager


_bot_instance: Bot | None = None
_dp_instance: Dispatcher | None = None

def routes_registration(dp: Dispatcher) -> Dispatcher:
    admins = list(map(int, config("ADMINS").split(',')))
    employees = list(map(int, config("EMPLOYEES").split(',')))

    common_router.message.middleware(AccessMiddleware(admins, employees))
    employee_router.message.middleware(AccessMiddleware(admins, employees))
    admin_router.message.middleware(AccessMiddleware(admins, employees))

    dp.include_router(common_router)
    dp.include_router(employee_router)
    dp.include_router(admin_router)

    return dp


def create_bot(cfg_name) -> tuple[Bot, Dispatcher]:
    global _bot_instance, _dp_instance

    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(name)s - %(message)s - %(asctime)s')
    logger = logging.getLogger(__name__)

    if not _bot_instance or not _dp_instance:
        _bot_instance = Bot(token=config("BOT_TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        _dp_instance = Dispatcher(storage=RedisStorage(redis=DataManager().get_conn()))
        _dp_instance = routes_registration(_dp_instance)

    return _bot_instance, _dp_instance
