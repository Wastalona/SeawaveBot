from aiogram import types, Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from tools.keyboards import *


admin_router = Router()

@admin_router.message(F.text.lower()  == "reports")
@admin_router.message()
async def reports_handler(msg: Message) -> None:
    pass

@admin_router.message(F.text.lower()  == "report card")
@admin_router.message(F.text.lower()  == "report_card")
@admin_router.message()
async def report_card_handler(msg: Message) -> None:
    pass

@admin_router.message(F.text.lower()  == "notify")
@admin_router.message()
async def notify_handler(msg: Message) -> None:
    pass

@admin_router.message(F.text.lower()  == "hire emp")
@admin_router.message(F.text.lower()  == "hire employee")
@admin_router.message(F.text.lower()  == "hire")
@admin_router.message()
async def hire_emp_handler(msg: Message) -> None:
    pass

@admin_router.message(F.text.lower()  == "release emp")
@admin_router.message(F.text.lower()  == "release employee")
@admin_router.message(F.text.lower()  == "release")
@admin_router.message(F.text.lower()  == "remove emp")
@admin_router.message(F.text.lower()  == "remove employee")
@admin_router.message(F.text.lower()  == "remove")
async def release_emp_handler(msg: Message) -> None:
    pass

@admin_router.message(F.text.lower() == "trasnfer emp")
@admin_router.message(F.text.lower() == "trasnfer employee")
@admin_router.message(F.text.lower() == "trasnfer")
async def transfer_emp_handler(msg: Message) -> None:
    pass

@admin_router.message(F.text.lower() == "emp list")
@admin_router.message(F.text.lower() == "employees")
@admin_router.message(F.text.lower() == "employee list")
async def emp_list_handler(msg: Message) -> None:
    pass
