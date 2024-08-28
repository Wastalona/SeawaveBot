import unittest
import pytest
import asyncio
import json
from os import listdir

from aiogram.fsm.storage.redis import Redis
from decouple import config
from icecream import ic

from ..utils import DB_ADMIN, DB_USER, DB_USER_0, parse_bytes, TEST_MSG
from ...bot import DataManager, create_bot
from ...bot.tools.utils import Professions


# ===== Test db init ===== 
def test_init_db(damage: DataManager):
    assert isinstance(damage, DataManager)

@pytest.mark.asyncio
async def test_create_conn(damage: DataManager):
    assert await damage.conn.ping()

@pytest.mark.asyncio
async def test_create_temp_db(damage: DataManager):
    sets = await damage.fetch_redis_sets()
    admins, blocked, employees = list(map(parse_bytes, (sets)))
    assert config("OWNER") in admins
    assert len(blocked) == 1 and blocked[-1] == ''
    assert len(employees) == 1 and employees[-1] == ''
# ===== END DB INIT =====

# ===== Test CRUD Methods =====
# ----- HIRE -----
@pytest.mark.asyncio
async def test_hire_admin(damage: DataManager):
    await damage.hire_person(DB_ADMIN.get("id"), DB_ADMIN.get("profession").value)
    admins = parse_bytes(await damage.conn.smembers("_admins"))
    
    assert DB_ADMIN.get("id") in admins

@pytest.mark.asyncio
async def test_hire_empl(damage: DataManager):
    await damage.hire_person(DB_USER.get("id"), DB_USER.get("profession").value)
    empls = parse_bytes(await damage.conn.smembers("employees_ids"))
    empl_info = ic(json.loads(await damage.conn.hget(DB_USER.get("id"), "info")))
    
    assert DB_USER.get("id") in empls
    assert DB_USER.get("profession").value == empl_info.get("profession")
    assert empl_info.get("videos") == []
    assert empl_info.get("photos") == []
# ----- END HIRE -----

# ----- RELEASE -----
@pytest.mark.asyncio
async def test_release_empl(damage: DataManager):
    await damage.hire_person(DB_USER.get("id"), DB_USER.get("profession").value)
    await damage.release_person(DB_USER.get("id"))
    empls = parse_bytes(await damage.conn.smembers("employees_ids"))
    empl_info = ic(await damage.conn.hget(DB_USER.get("id"), "info"))
    
    assert DB_USER.get("id") not in empls
    assert empl_info is None

@pytest.mark.asyncio
async def test_release_admin(damage: DataManager):
    await damage.hire_person(DB_ADMIN.get("id"), DB_ADMIN.get("profession").value)
    await damage.release_person(DB_ADMIN.get("id"))
    admins = parse_bytes(await damage.conn.smembers("_admins"))

    assert DB_ADMIN.get("id") not in admins
# ----- END EMPLOYESS -----

# ----- TRANSFER -----
@pytest.mark.asyncio
async def test_transfer_empl_to_empl(damage: DataManager):
    ID = DB_USER.get("id")

    await damage.hire_person(ID, DB_USER.get("profession").value)
    await damage.transfer_emp(ID, DB_USER.get("new_profession").value)
    
    prof_ids = parse_bytes(await damage.conn.smembers("employees_ids"))
    new_prof = await damage.get_prof(ID)

    assert ID in prof_ids
    assert new_prof == DB_USER.get("new_profession").value

@pytest.mark.asyncio
async def test_transfer_empl_to_admin(damage: DataManager):
    ID = DB_USER_0.get("id")

    await damage.hire_person(ID, DB_USER_0.get("profession").value)
    await damage.transfer_emp(ID, DB_USER_0.get("new_profession").value)
    
    old_prof_ids = parse_bytes(await damage.conn.smembers("employees_ids"))
    new_prof_ids = parse_bytes(await damage.conn.smembers("_admins"))
    new_prof = await damage.get_prof(ID)

    assert ID not in old_prof_ids
    assert ID in new_prof_ids
    assert new_prof == DB_USER_0.get("new_profession").value

@pytest.mark.asyncio
async def test_transfer_admin_to_empl(damage: DataManager):
    ID = DB_ADMIN.get("id")

    await damage.hire_person(ID, DB_ADMIN.get("profession").value)
    await damage.transfer_emp(ID, DB_ADMIN.get("new_profession").value)
    
    old_prof_ids = parse_bytes(await damage.conn.smembers("_admins"))
    new_prof_ids = parse_bytes(await damage.conn.smembers("employees_ids"))
    new_prof = await damage.get_prof(ID)

    assert ID not in old_prof_ids
    assert ID in new_prof_ids
    assert new_prof == DB_ADMIN.get("new_profession").value

@pytest.mark.asyncio
async def test_transfer_owner_to_another(damage: DataManager):
    await damage.transfer_emp(config("OWNER"), Professions.ADMIN.value)
    admins_ids = parse_bytes(await damage.conn.smembers("_admins"))
    empls_ids = parse_bytes(await damage.conn.smembers("employees_ids"))

    assert config("OWNER") in admins_ids
    assert config("OWNER") not in empls_ids
    assert await damage.get_prof(config("OWNER")) == Professions.ADMIN.value
# ----- END TRANSFER -----

# ----- COMMON -----
@pytest.mark.asyncio
async def test_get_prof(damage: DataManager):
    await damage.hire_person(DB_ADMIN.get("id"), DB_ADMIN.get("profession").value)
    await damage.hire_person(DB_USER.get("id"), DB_USER.get("profession").value)

    admin = await damage.get_prof(DB_ADMIN.get("id"))
    empl = await damage.get_prof(DB_USER.get("id"))

    assert admin == DB_ADMIN.get("profession").value
    assert empl == DB_USER.get("profession").value

@pytest.mark.asyncio
async def test_set_notify(damage: DataManager):
    await damage.set_notify(TEST_MSG)
    msg = await damage.conn.get("notify")
    assert msg.decode() == TEST_MSG
# ----- END COMMON ----
# ===== END CRUD =====