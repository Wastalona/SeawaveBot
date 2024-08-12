from unittest.mock import AsyncMock
import pytest
from datetime import datetime

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from bot.handlers.common_handlers import (
    start_handler, close_menu, cancel_state
)
from bot.tools.keyboards import *
from bot.tools.texts import ADMIN_CMDS, EMPL_CMDS

from ..utils import *



@pytest.mark.asyncio
async def test_emp_start_handler(memory_storage, bot):
    message: Message = AsyncMock(
        id = 1,
        date = datetime.now(),
        chat = TEST_CHAT,
        from_user = TEST_EMP,
        text = "start"
    )

    state: FSMContext = FSMContext(
        storage=memory_storage,
        key=StorageKey(
            bot_id=bot.id,
            chat_id=TEST_CHAT.id,
            user_id=TEST_EMP.id
        )
    )

    await start_handler(msg=message, state=state)
    assert await state.get_state() is None
    message.answer.assert_called_with(EMPL_CMDS, reply_markup=employee_kb)

@pytest.mark.asyncio
async def test_admin_start_handler(memory_storage, bot):
    message: Message = AsyncMock(
        id = 1,
        date = datetime.now(),
        chat = TEST_CHAT,
        from_user = TEST_ADMIN,
        text = "start"
    )

    state: FSMContext = FSMContext(
        storage=memory_storage,
        key=StorageKey(
            bot_id=bot.id,
            chat_id=TEST_CHAT.id,
            user_id=TEST_ADMIN.id
        )
    )

    await start_handler(msg=message, state=state)
    assert await state.get_state() is None
    message.answer.assert_called_with(ADMIN_CMDS, reply_markup=admin_kb)

@pytest.mark.asyncio
async def test_user_start_handler(memory_storage, bot):
    message: Message = AsyncMock(
        id = 1,
        date = datetime.now(),
        chat = TEST_CHAT,
        from_user = TEST_USER,
        text = "start"
    )

    state: FSMContext = FSMContext(
        storage=memory_storage,
        key=StorageKey(
            bot_id=bot.id,
            chat_id=TEST_CHAT.id,
            user_id=TEST_USER.id
        )
    )

    await start_handler(msg=message, state=state)
    assert await state.get_state() is None
    message.answer.assert_not_called()

@pytest.mark.asyncio
async def test_close_menu_handler(memory_storage, bot):
    message = AsyncMock(
        id = 3,
        date = datetime.now(),
        chat = TEST_CHAT,
        from_user = TEST_ADMIN,
        text = "✖ close"
    )

    state: FSMContext = FSMContext(
        storage=memory_storage,
        key=StorageKey(
            bot_id=bot.id,
            chat_id=TEST_CHAT.id,
            user_id=TEST_ADMIN.id
        )
    )

    await close_menu(msg=message, state=state)
    assert await state.get_state() is None
    message.answer.assert_awaited_with("Closing menu...", reply_markup=ReplyKeyboardRemove())

@pytest.mark.asyncio
async def test_close_menu_by_user_handler(memory_storage, bot):
    message: Message = AsyncMock(
        id = 1,
        date = datetime.now(),
        chat = TEST_CHAT,
        from_user = TEST_ADMIN,
        text = "start"
    )

    state: FSMContext = FSMContext(
        storage=memory_storage,
        key=StorageKey(
            bot_id=bot.id,
            chat_id=TEST_CHAT.id,
            user_id=TEST_ADMIN.id
        )
    )

    await close_menu(msg=message, state=state)
    assert await state.get_state() is None
    message.assert_not_called()

@pytest.mark.asyncio
async def test_cancel_handler(memory_storage, bot):
    message = AsyncMock(
        id = 3,
        date = datetime.now(),
        chat = TEST_CHAT,
        from_user = TEST_ADMIN,
        text = "cancel"
    )

    state: FSMContext = FSMContext(
        storage=memory_storage,
        key=StorageKey(
            bot_id=bot.id,
            chat_id=TEST_CHAT.id,
            user_id=TEST_ADMIN.id
        )
    )

    await cancel_state(msg=message, state=state)
    assert await state.get_state() is None
    message.answer.assert_called_with("The operation was cancelled")
