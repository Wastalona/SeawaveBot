import logging

from aiogram import types, Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from icecream import ic

from ..tools.keyboards import *
from ..tools.states import Notification, StaffEditor
from ..tools.texts import *


admin_router = Router()

# ~~~ SIMPLE ROUTES ~~~
@admin_router.message(F.text.lower()  == "reports")
async def reports_handler(msg: Message) -> None:
    try:
        # insert logic
        await msg.answer("Report")
    except Exception as err:
        await msg.answer(FAIL_LOAD_REP)
        logging.error(f"Somthing went wrong: {err}")
        ic(err, err.__class__)


@admin_router.message(F.text.lower()  == "report card")
@admin_router.message(F.text.lower()  == "repcard")
async def report_card_handler(msg: Message) -> None:
    try:
        # insert logic
        await msg.answer("Report card")
    except Exception as err:
        await msg.answer(FAIL_LOAD_REPCARD)
        logging.error(LOG_ERR + err)
        ic(err)

@admin_router.message(F.text.lower()  == "set notify")
async def set_notify_text_handler(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(Notification.notify)
    await msg.answer(SET_NOTIFY_TEXT)

@admin_router.message(F.text.lower()  == "notify")
async def notify_handler(msg: Message) -> None:
    try:
        # receive notification text and employee lists
        await msg.answer("Notify")
    except Exception as err:
        await msg.answer(NOTIFY_ERR)
        logging.error(LOG_ERR + err)
        ic(err)

@admin_router.message(F.text.lower()  == "hire staff")
@admin_router.message(F.text.lower()  == "hire")
async def hire_staff_handler(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(StaffEditor.hire)
    await msg.answer(STAFF_EDIT)

@admin_router.message(F.text.lower()  == "release staff")
@admin_router.message(F.text.lower()  == "release")
async def release_staff_handler(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(StaffEditor.release)
    await msg.answer(STAFF_EDIT)

@admin_router.message(F.text.lower() == "transfer staff")
@admin_router.message(F.text.lower() == "transfer")
async def transfer_staff_handler(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(StaffEditor.transfer)
    await msg.answer(STAFF_TRS)

@admin_router.message(F.text.lower() == "staff list")
@admin_router.message(F.text.lower() == "staff")
async def staff_list_handler(msg: Message) -> None:
    try:
        # getting staff from db
        await msg.answer("staff")
    except Exception as err:
        await msg.answer(STAFF_LOAD_ERR)
        logging.error(LOG_ERR + err)
        ic(err)
# ~~~ END SIMPLE ROUTES ~~~

# ~~~ ROUTES WITH STATES ~~~
@admin_router.message(Notification.notify)
async def setting_notift_text_handler(msg: Message, state: FSMContext):
    try:
        # insert logic
        await msg.answer(NOTIFY_TEXT)
    except Exception as err:
        await msg.answer(SET_NOTIFY_ERR)
        logging.error(LOG_ERR + err)
        ic(err)
    finally:
        await state.clear()

@admin_router.message(StaffEditor.hire)
async def hiring_staff_handler(msg: Message, state: FSMContext):
    try:
        # insert logic
        await msg.answer(STAFF_SUC_ADD)
    except Exception as err:
        await msg.answer(STAFF_ERR)
        logging.error(LOG_ERR + err)
        ic(err)
    finally:
        await state.clear()

@admin_router.message(StaffEditor.release)
async def releasing_staff_handler(msg: Message, state: FSMContext):
    try:
        # insert logic
        await msg.answer(STAFF_SUC_REL)
    except Exception as err:
        await msg.answer(STAFF_ERR)
        logging.error(LOG_ERR + err)
        ic(err)
    finally:
        await state.clear()

@admin_router.message(StaffEditor.transfer)
async def transfering_staff_handler(msg: Message, state: FSMContext):
    try:
        # insert logic
        await msg.answer(STAFF_SUC_TRS)
    except Exception as err:
        await msg.answer(STAFF_ERR)
        logging.error(LOG_ERR + err)
        ic(err)
    finally:
        await state.clear()
# ~~~ END ROUTES WITH STATES ~~~

@admin_router.message()
async def not_found(msg: Message):
    await msg.reply("Sorry... The command was not recognized.")