from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware


# Authentication — changing the message for admins and employees
class AccessMiddleware(BaseMiddleware):
    def __init__(self, admins: list[int], emps: list[int]):
        self.admins_ids = admins
        self.emp_ids = emps
        super().__init__()

    async def __call__(self, handler, event: types.Message, data: dict):
        user_id = event.from_user.id

        if user_id not in self.admins_ids + self.emp_ids:
            await event.answer("Access Denied")
            return # Stopping execution without calling handler

        return await handler(event, data)
