import logging
import json
import base64

from aiogram.fsm.storage.redis import Redis
from decouple import config
from cryptography.fernet import Fernet
from icecream import ic

from .helpers import redis_exceptions, wrap_data


conn: Redis | None = None


def get_fernet() -> Fernet:
    secret_key = config("FILES_SECRET_KEY").encode()
    return Fernet(secret_key)  


@redis_exceptions
async def save_local(conn: Redis) -> None:
    admins: set = await conn.smembers("_admins")
    blocked: set = await conn.smembers("blocked")
    empls: set = await conn.smembers("employees_ids")
    reports: dict = {}

    if empls:
        for emp_id in empls:
            if not emp_id: continue
            # Ensure emp_id is decoded from bytes if necessary
            emp_id_decoded = emp_id.decode() if isinstance(emp_id, bytes) else emp_id
            employee_data = json.loads(await conn.hget(emp_id, "reports"))
            reports[emp_id_decoded] = employee_data

    json_data: dict = wrap_data(admins, blocked, empls, reports)
    ic(json_data)    
    data = get_fernet().encrypt(json.dumps(json_data).encode())

    with open('db.bin', 'wb') as db:
        db.write(data)

    logging.info("The data has been successfully encrypted and saved!")


def load_from_local() -> dict:    
    with open('db.bin', 'rb') as db:
        ec_data = db.read()

    data = get_fernet().decrypt(ec_data).decode()
    
    logging.info("The data from the file has been successfully decrypted and uploaded!")
    return ic(json.loads(data))

@redis_exceptions
async def push_to_redis(conn: Redis) -> None:
    data: dict = load_from_local()

    await conn.flushall()
    await conn.lpush("_admins", ' '.join(data.pop("_admins")))
    await conn.lpush("blocked", ' '.join(data.pop("blocked")))
    await conn.lpush("employees_ids", ' '.join(data.pop("employees_ids")))
    
    for key, value in data.items():
        await conn.hset(key, "reports", f"{value}")


@redis_exceptions
async def create_temp_db(conn: Redis) -> None | Exception:
    await conn.flushall()
    await conn.sadd("blocked", "")
    await conn.sadd("employees_ids", "")
    await conn.sadd("_admins", config("OWNER"))
    await conn.expire(name="blocked", time=3600)
    await conn.expire(name="_admins", time=3600)


def get_conn() -> Redis:
    global conn

    if conn is None:
        conn = Redis(
            host=config("REDIS_HOST"), 
            port=config("REDIS_PORT"), 
            db=config("REDIS_DB_INDEX")
        )

    return conn
