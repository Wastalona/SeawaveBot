from aiogram import types, Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from icecream import ic

from tools.states import SendReports, Shifts
from tools.keyboards import *
from tools.texts import (
    SUCC_LOAD, FAIL_LOAD, 
    WORK_SHIFT, REST_SHIFT, 
    COM_WORK_MES, COM_REST_MES
)


employee_router = Router()


# ~~~ SIMPLE ROUTES ~~~
@employee_router.message(F.text.lower() == "photos")
@employee_router.message(F.text.lower() == "📷 photo")
async def photo_report_handler(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(SendReports.photo)
    await msg.answer("Send me your photo report. Make sure that you have selected image compression.")

@employee_router.message(F.text.lower() == "videos")
@employee_router.message(F.text.lower() == "🎬 video")
async def video_report_handler(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(SendReports.video)
    await msg.answer("Send me your video report.")

@employee_router.message(F.text.lower() == "open shift")
@employee_router.message(F.text.lower() == "open_shift")
async def open_shift_handler(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(Shifts.open_)
    await msg.answer(COM_WORK_MES)

@employee_router.message(F.text.lower() == "close shift")
@employee_router.message(F.text.lower() == "close_shift")
async def close_shift_handler(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(Shifts.close_)
    await msg.answer(COM_REST_MES)
# ~~~ END SIMPLE ROUTES ~~~


# ~~~ ROUTES WITH STATES ~~~
@employee_router.message(F.photo, SendReports.photo)
async def getting_photo_report_handler(msg: Message, state: FSMContext) -> None:
    try:
        ic([img.file_id for img in msg.photo])
        # insert logic
        await msg.answer(SUCC_LOAD)
    except Exception as err:
        await msg.answer(FAIL_LOAD)
        ic(err)
    finally:
        await state.clear()

@employee_router.message(F.video, SendReports.video)
async def getting_video_report_handler(msg: Message, state: FSMContext) -> None:
    try:
        ic([vid.file_id for vid in msg.video])
        # insert logic
        await msg.answer(SUCC_LOAD)
    except Exception as err:
        await msg.answer(FAIL_LOAD)
        ic(err)
    finally:
        await state.clear()

@employee_router.message(F.text == "coming on shift", Shifts.open_)
async def commit_the_comming_on(msg: Message, state: FSMContext):
    # insert logic
    await msg.answer(WORK_SHIFT)
    await state.clear()

@employee_router.message(F.text == "coming off shift", Shifts.close_)
async def commit_the_comming_off(msg: Message, state: FSMContext):
    # insert logic
    await msg.answer(REST_SHIFT)
    await state.clear()
# ~~~ END ROUTES WITH STATES ~~~
