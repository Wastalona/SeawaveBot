from os import getenv

from aiogram import types, Router, F
from aiogram.types import Message
from aiogram.filters import Command
from icecream import ic

from .middlewares import AccessMiddleware
from .texts import ADMIN_CMDS, EMPL_CMDS


# Get lists of administrators and employees from environment variables
admins = list(map(int, getenv("ADMINS", "").split(",")))
employees = list(map(int, getenv("EMPLOYEES", "").split(",")))

common_router = Router()
employee_router = Router()
admin_router = Router()

common_router.message.middleware(AccessMiddleware(admins, employees))
employee_router.message.middleware(AccessMiddleware(admins, employees))
admin_router.message.middleware(AccessMiddleware(admins, employees))


@common_router.message(F.text.lower() == "menu")
@common_router.message(Command("start"))
async def start_handler(msg: Message):
    user_id = msg.from_user.id

    if user_id in admins:
        await msg.answer(ADMIN_CMDS)
    else:
        await msg.answer(EMPL_CMDS)


''' ~~~ EMPLOYEE ~~~ '''
@employee_router.message(F.text.lower() == "photos")
@employee_router.message(F.text.lower() == "photo")
async def photo_report_handler(msg: Message):
    pass

@employee_router.message(F.text.lower() == "video")
@employee_router.message(F.text.lower() == "videos")
async def video_report_handler(msg: Message):
    pass

@employee_router.message(F.text.lower() == "open shift")
@employee_router.message(F.text.lower() == "open_shift")
async def open_shift_handler(msg: Message):
    pass

@employee_router.message(F.text.lower() == "close shift")
@employee_router.message(F.text.lower() == "close_shift")
@employee_router.message()
async def close_shift_handler(msg: Message):
    pass


''' ~~~ ADMIN ~~~ '''
@admin_router.message(F.text.lower()  == "reports")
@admin_router.message()
async def reports_handler(msg: Message):
    pass

@admin_router.message(F.text.lower()  == "report card")
@admin_router.message(F.text.lower()  == "report_card")
@admin_router.message()
async def report_card_handler(msg: Message):
    pass

@admin_router.message(F.text.lower()  == "notify")
@admin_router.message()
async def notify_handler(msg: Message):
    pass

@admin_router.message(F.text.lower()  == "add emp")
@admin_router.message(F.text.lower()  == "add employee")
@admin_router.message(F.text.lower()  == "add")
@admin_router.message()
async def add_emp_handler(msg: Message):
    pass

@admin_router.message(F.text.lower()  == "release emp")
@admin_router.message(F.text.lower()  == "release employee")
@admin_router.message(F.text.lower()  == "release")
@admin_router.message(F.text.lower()  == "remove emp")
@admin_router.message(F.text.lower()  == "remove employee")
@admin_router.message(F.text.lower()  == "remove")
async def rem_emp_handler(msg: Message):
    pass

@admin_router.message(F.text.lower() == "trasnfer emp")
@admin_router.message(F.text.lower() == "trasnfer employee")
@admin_router.message(F.text.lower() == "trasnfer")
async def transfer_emp_handler(msg: Message):
    pass

@admin_router.message(F.text.lower() == "emp list")
@admin_router.message(F.text.lower() == "employees")
@admin_router.message(F.text.lower() == "employee list")
async def emp_list_handler(msg: Message):
    pass



__all__ = ["common_router", "employee_router", "admin_router"]