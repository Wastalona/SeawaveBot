from __future__ import annotations
import asyncio

from bot import create_bot


async def shutdown(dispatcher: Dispatcher) -> None:
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

async def main() -> None:
    bot, dp = create_bot('testing')

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot, 
        allowed_updates=dp.resolve_used_update_types(),
        on_shutdown=shutdown
    )

if __name__ == '__main__':
    asyncio.run(main())