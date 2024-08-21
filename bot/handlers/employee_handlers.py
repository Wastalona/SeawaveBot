from aiogram import types, Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from icecream import ic

from ..tools.states import SendReports
from ..tools.keyboards import *
from ..tools.texts import SUCC_LOAD, FAIL_LOAD
from ..tools.db import DataManager


employee_router = Router()
damage = DataManager()


# ~~~ SIMPLE ROUTES ~~~
@employee_router.message(F.text.lower() == "photo")
@employee_router.message(F.text.lower() == "📷")
async def photo_report_handler(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(SendReports.photo)
    await msg.answer("Send me your photo report. Make sure that you have selected image compression.")

@employee_router.message(F.text.lower() == "video")
@employee_router.message(F.text.lower() == "📹")
async def video_report_handler(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(SendReports.video)
    await msg.answer("Send me your video report.")
# ~~~ END SIMPLE ROUTES ~~~


# ~~~ ROUTES WITH STATES ~~~
@employee_router.message(F.photo, SendReports.photo)
async def getting_photo_report_handler(msg: Message, state: FSMContext) -> None:
    try:
        await damage.update_key(msg.from_user.id, "photos", msg.photo[-1].file_id)
        await msg.answer(SUCC_LOAD)
    except Exception as err:
        await msg.answer(FAIL_LOAD)
        ic(err)
    finally:
        await state.clear()

@employee_router.message(F.video, SendReports.video)
async def getting_video_report_handler(msg: Message, state: FSMContext) -> None:
    try:
        await damage.update_key(msg.from_user.id, "videos", msg.video.file_id)
        await msg.answer(SUCC_LOAD)
    except Exception as err:
        await msg.answer(FAIL_LOAD)
        ic(err)
    finally:
        await state.clear()
# ~~~ END ROUTES WITH STATES ~~~
