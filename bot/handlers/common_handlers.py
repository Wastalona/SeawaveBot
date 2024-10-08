from aiogram import types, Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from decouple import config

from ..tools.keyboards import *
from ..tools.texts import ADMIN_CMDS, EMPL_CMDS


admins = list(map(int, config("ADMINS").split(',')))
employees = list(map(int, config("EMPLOYEES").split(',')))

common_router = Router()

@common_router.message(F.text.lower() == "menu")
@common_router.message(Command("start", "menu"))
async def start_handler(msg: Message, state: FSMContext) -> None:
    await state.clear()

    user_id = msg.from_user.id
    if user_id in admins: await msg.answer(ADMIN_CMDS, reply_markup=admin_kb)
    elif user_id in employees: await msg.answer(EMPL_CMDS, reply_markup=employee_kb)
    else: return


@common_router.message(F.text.lower() == "✖ close")
@common_router.message(Command("close"))
async def close_menu(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await msg.answer("Closing menu...", reply_markup=ReplyKeyboardRemove())


@common_router.message(F.text.lower() == "cancel")
@common_router.message(Command("cancel"))
async def cancel_state(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await msg.answer("The operation was cancelled")
