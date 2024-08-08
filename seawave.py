from os import getenv
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from icecream import ic

from config import config
from handlers import *
from tools.middlewares import AccessMiddleware


async def shutdown(dispatcher: Dispatcher) -> None:
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


def routes_registration(dp: Dispatcher) -> Dispatcher:
    admins = list(map(int, getenv("ADMINS", "").split(',')))
    employees = list(map(int, getenv("EMPLOYEES", "").split(',')))

    common_router.message.middleware(AccessMiddleware(admins, employees))
    employee_router.message.middleware(AccessMiddleware(admins, employees))
    admin_router.message.middleware(AccessMiddleware(admins, employees))

    dp.include_router(common_router)
    dp.include_router(employee_router)
    dp.include_router(admin_router)

    return dp


async def main(cfg_name:str):
    bot = Bot(token=config[cfg_name].BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage()) # Change memory storage to Redis

    # Routes registration
    admins = list(map(int, getenv("ADMINS", "").split(',')))
    employees = list(map(int, getenv("EMPLOYEES", "").split(',')))
    employee_router.message.middleware(AccessMiddleware(admins, employees))

    dp = routes_registration(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot, 
        allowed_updates=dp.resolve_used_update_types(),
        on_shutdown=shutdown
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main("development"))