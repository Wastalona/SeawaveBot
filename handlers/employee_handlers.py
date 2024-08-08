from aiogram import types, Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from tools.states import SendReports, Shifts
from tools.keyboards import *


employee_router = Router()

@employee_router.message(F.text.lower() == "photos")
@employee_router.message(F.text.lower() == "📷 photo")
async def photo_report_handler(msg: Message, state: FSMContext) -> None:
    await msg.answer("Send a photo. Make sure that you have selected image compression.")

@employee_router.message(SendReports.photo)
@employee_router.message(F.photo)
async def getting_photo_report_handler(msg: Message, state: FSMContext) -> None:
    await msg.answer(f"{msg.photo[-1]}")


@employee_router.message(F.text.lower() == "videos")
@employee_router.message(F.text.lower() == "🎬 video")
async def video_report_handler(msg: Message, state: FSMContext) -> None:
    pass

@employee_router.message(SendReports.video)
async def getting_video_report_handler(msg: Message, state: FSMContext) -> None:
    pass


@employee_router.message(F.text.lower() == "open shift")
@employee_router.message(F.text.lower() == "open_shift")
async def open_shift_handler(msg: Message, state: FSMContext) -> None:
    pass


@employee_router.message(F.text.lower() == "close shift")
@employee_router.message(F.text.lower() == "close_shift")
@employee_router.message()
async def close_shift_handler(msg: Message, state: FSMContext) -> None:
    pass
