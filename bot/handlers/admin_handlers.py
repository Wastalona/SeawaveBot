import logging

from aiogram import types, Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from icecream import ic

from ..tools.keyboards import *
from ..tools.states import Notification, StaffEditor
from ..tools.texts import *
from ..tools.db import DataManager
from ..tools.utils import Professions
from ..tools.exceptions import ProfessionException


admin_router = Router()
damage = DataManager()

# ~~~ SIMPLE ROUTES ~~~
@admin_router.message(F.text.lower()  == "reports")
async def reports_handler(msg: Message) -> None:
    try:
        answer, reports = ic(await damage.get_info(False))
        await msg.answer(answer)
        if not reports:
            return
        if reports[0]:
            [await msg.answer_photo(rep) for rep in reports[0]]
        if reports[1]:
            [await msg.answer_video(rep) for rep in reports[1]]
    except Exception as err:
        await msg.answer(FAIL_LOAD_REP)
        logging.error(f"{LOG_ERR} {err}")
        ic(err, err.__class__)

@admin_router.message(F.text.lower()  == "set notify")
async def set_notify_text_handler(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(Notification.notify)
    await msg.answer(SET_NOTIFY_TEXT)

@admin_router.message(F.text.lower()  == "notify")
async def notify_handler(msg: Message) -> bool:
    try:
        text = "The message has been sent." if await damage.notify() else "You forgot to set up the notification."
        await msg.answer(text)
        return True
    except Exception as err:
        await msg.answer(NOTIFY_ERR)
        logging.error(f"{LOG_ERR} {err}")
        ic(err)
        return False

@admin_router.message(F.text.lower()  == "hire staff")
@admin_router.message(F.text.lower()  == "hire")
async def hire_staff_handler(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(StaffEditor.hire)
    await msg.answer(STAFF_HIRE)

@admin_router.message(F.text.lower()  == "release staff")
@admin_router.message(F.text.lower()  == "release")
async def release_staff_handler(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(StaffEditor.release)
    await msg.answer(STAFF_RELEASE)

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
        await msg.answer(await damage.get_info(True))
    except Exception as err:
        await msg.answer(STAFF_LOAD_ERR)
        logging.error(f"{LOG_ERR} {err}")
        ic(err)
# ~~~ END SIMPLE ROUTES ~~~

# ~~~ ROUTES WITH STATES ~~~
@admin_router.message(Notification.notify)
async def setting_notift_text_handler(msg: Message, state: FSMContext):
    try:
        await damage.set_notify(msg.text)
        await msg.answer(NOTIFY_TEXT)
    except Exception as err:
        await msg.answer(SET_NOTIFY_ERR)
        logging.error(f"{LOG_ERR} {err}")
        ic(err)
    finally:
        await state.clear()

@admin_router.message(StaffEditor.hire)
async def hiring_staff_handler(msg: Message, state: FSMContext):
    try:
        _id, profession = msg.text.split(' ')
        ic(_id, profession)
        if profession.upper() not in Professions:
            raise ProfessionException()
        
        await damage.hire_person(_id, profession)
        await msg.answer(STAFF_SUC_ADD)
    except ProfessionException:
        await msg.answer("Error - wrong profession.")
        logging.error(LOG_ERR + "Wrong profession.")
    except Exception as err:
        await msg.answer(STAFF_ERR)
        logging.error(f"{LOG_ERR} {err}")
        ic(err)
    finally:
        await state.clear()

@admin_router.message(StaffEditor.release)
async def releasing_staff_handler(msg: Message, state: FSMContext):
    try:
        await damage.release_person(msg.text)
        await msg.answer(STAFF_SUC_REL)
    except Exception as err:
        await msg.answer(STAFF_ERR)
        logging.error(f"{LOG_ERR} {err}")
        ic(err)
    finally:
        await state.clear()

@admin_router.message(StaffEditor.transfer)
async def transfering_staff_handler(msg: Message, state: FSMContext):
    try:
        _id, dest = msg.text.split(' ')
        await damage.transfer_emp(_id, dest)
        await msg.answer(STAFF_SUC_TRS)
    except Exception as err:
        await msg.answer(STAFF_ERR)
        logging.error(f"{LOG_ERR} {err}")
        ic(err)
    finally:
        await state.clear()
# ~~~ END ROUTES WITH STATES ~~~

@admin_router.message()
async def not_found(msg: Message):
    await msg.reply("Sorry... The command was not recognized.")