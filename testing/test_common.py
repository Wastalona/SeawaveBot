from unittest.mock import AsyncMock
import pytest

from bot.handlers.common_handlers import (
    start_handler, close_menu, cancel_state
)
from bot.tools.keyboards import *
from bot.tools.texts import ADMIN_CMDS, EMPL_CMDS


@pytest.mark.asyncio
async def test_emp_start_handler():
    msg = AsyncMock()
    await start_handler(msg)

    msg.answer.assert_called_with(EMPL_CMDS, reply_markup=employee_kb)


@pytest.mark.asyncio
async def test_adm_start_handler():
    msg = AsyncMock()
    await start_handler(msg)

    msg.answer.assert_called_with(ADMIN_CMDS, reply_markup=admin_kb)