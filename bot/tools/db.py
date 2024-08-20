import logging
import json

from aiogram.fsm.storage.redis import Redis
from decouple import config
from cryptography.fernet import Fernet
from icecream import ic

from .helpers import redis_exceptions, wrap_data, get_time, get_bot_instance
from .utils import Singleton, Professions
from .exceptions import StaffEditException, NotifyException


class DataManager(metaclass=Singleton):
    """
    
    """
    def __init__(self):
        self.conn: Redis | None = None
        self.fernet = self.get_fernet

    @property
    def get_fernet(self) -> Fernet:
        secret_key = config("FILES_SECRET_KEY").encode()
        return Fernet(secret_key)

    # Save to file block
    @redis_exceptions
    async def save_local(self) -> None:
        admins, blocked, empls = await self.fetch_redis_sets()
        reports = await self.fetch_info(empls)

        json_data = wrap_data(admins, blocked, empls, reports)
        ic(json_data)

        self.save_encrypted_data(json_data)
        logging.info("The data has been successfully encrypted and saved!")

    def save_encrypted_data(self, json_data: dict) -> None:
        data = self.fernet.encrypt(json.dumps(json_data).encode())
        with open('db.bin', 'wb') as db:
            db.write(data)
    # END

    # Read from file and transfer to Redis
    def load_from_local(self) -> dict:
        data = self.decrypt_data()
        logging.info("The data from the file has been successfully decrypted and uploaded!")
        return ic(json.loads(data))

    def decrypt_data(self) -> str:
        with open('db.bin', 'rb') as db:
            ec_data = db.read()
        return self.fernet.decrypt(ec_data).decode()

    @redis_exceptions
    async def push_to_redis(self) -> None:
        data = self.load_from_local()
        await self.conn.flushall()
        await self.push_data_to_redis(data)

    async def push_data_to_redis(self, data: dict) -> None:
        await self.conn.lpush("_admins", ' '.join(data.pop("_admins", [])))
        await self.conn.lpush("blocked", ' '.join(data.pop("blocked", [])))
        await self.conn.lpush("employees_ids", ' '.join(data.pop("employees_ids", [])))

        for key, value in data.items():
            await self.conn.hset(key, "info", f"{value}")
    # END
    
    # CRUD methods
    @redis_exceptions
    async def hire_person(self, person_id: str, profession: Professions) -> None:        
        ic(f"--- hire_person ---\n{person_id=}\n{profession=}")
        if profession.lower() == "admin":
            await self.conn.sadd("_admins", person_id)
            return

        person_info: dict = {
            "videos": [],
            "photos": [],
            "profession": profession
        }

        await self.conn.sadd("employees_ids", person_id)
        await self.conn.hset(person_id, "info", ic(json.dumps(person_info)))

    @redis_exceptions
    async def release_person(self, person_id: str) -> None:
        ic(f"--- release_person ---\n{person_id=}")
        profession = ic(await self.get_prof(person_id))
        if profession is None:
            raise StaffEditException("The staff was not found")

        if profession.lower() == "admin":
            await self.del_admin(person_id)
            return

        await self.del_employee(person_id)

    # @redis_exceptions
    async def transfer_emp(self, person_id: int, dest: Professions | str) -> None:
        if dest is None:
            raise StaffEditException("No profession have been found.")
        
        if person_id.lower() == Professions.ADMIN.value:
            await self.del_admin(person_id)
            await self.hire_person(person_id, dest)
            return 
        
        await self.update_key(person_id, "profession", dest)

    async def get_info(self, what_need: bool) -> str:
        """
        what_need = 1 - staff list | 0 - reports
        """
        empls = [i.decode() for i in await self.conn.smembers("employees_ids")]

        if what_need:
            admins = "\n".join([i.decode() for i in await self.conn.smembers("_admins")])
            empls = "\n".join(empls)
            return f"Admins:\n{admins}\nEmployess:{empls}"
        
        time = get_time()
        report = ""
        if time.hour in range(6, 11):
            report = "Morning report"
        elif time.hour in range(11, 15):
            report = "Afternoon report"
        elif time.hour in range(15, 22):
            report = "Dinner report"

        reports = await self.fetch_info(empls)
        ic(reports)
        
        return f"=== {report} - {time} ===\n"

    async def get_prof(self, person_id) -> str | None:
        if person_id in ic([i.decode() for i in await self.conn.smembers("_admins")]):
            return ic(Professions.ADMIN.value)
        
        empl = ic(await self.conn.hget(person_id, "info"))
        if empl is None:
            return None
        
        return ic(json.loads(empl).get("profession"))

    async def push_report(self, empl_id: int | str, report: str) -> None:
        pass
    # END

    # Notifications
    @redis_exceptions
    async def notify(self) -> None:
        msg = await self.conn.get("notify")        
        await get_bot_instance().send_message(config("COMMON_CHAT"), f"=== Notification ===\n\n{msg}")
    
    @redis_exceptions
    async def set_notify(self, notify_msg: str) -> None:
        await self.conn.set("notify", notify_msg)
    # END

    # Common
    # @redis_exceptions
    async def update_key(self, _id: int | str, key: str | int, new_value: str | int) -> None:
        info = ic(await self.fetch_info([_id]))
        info[_id][key] = new_value

        await self.conn.hset(_id, "info", json.dumps(info[_id]))

    @redis_exceptions
    async def del_admin(self, admin: int | str) -> None:
        await self.conn.srem("_admins", admin)

    @redis_exceptions
    async def del_employee(self, emp: int | str):
        await self.conn.srem("employees_ids", emp)
        await self.conn.hdel(emp, "info") # remake
    
    async def fetch_redis_sets(self) -> tuple:
        """extension for the save_local method"""
        admins = await self.conn.smembers("_admins")
        blocked = await self.conn.smembers("blocked")
        empls = await self.conn.smembers("employees_ids")
        return admins, blocked, empls

    async def fetch_info(self, empls: set | list) -> dict:
        """extension for the save_local method"""
        reports = {}
        for emp_id in empls:
            if emp_id:
                emp_id_decoded = emp_id.decode() if isinstance(emp_id, bytes) else emp_id
                employee_data = json.loads(await self.conn.hget(emp_id, "info"))
                reports[emp_id_decoded] = employee_data
        return reports
    #END

    # Basics
    @redis_exceptions
    async def create_temp_db(self) -> None:
        await self.conn.flushall()
        await self.conn.sadd("blocked", "")
        await self.conn.sadd("employees_ids", "")
        await self.conn.sadd("_admins", config("OWNER"))
        await self.set_expiry()

    async def set_expiry(self) -> None:
        await self.conn.expire(name="blocked", time=3600)
        await self.conn.expire(name="_admins", time=3600)

    def get_conn(self) -> Redis:
        if self.conn is None:
            self.conn = Redis(
                host=config("REDIS_HOST"), 
                port=config("REDIS_PORT"), 
                db=config("REDIS_DB_INDEX")
            )
        return self.conn

    def __str__(self) -> str:
        logging.info("[ + ] Getting information about the DataManager for the user")
        return ""
    
    def __repr__(self) -> str:
        logging.info("[ + ] Getting information about the DataManager for the developer")
        return ""

    def __del__(self) -> None:
        self.save_local()
        logging.info("[ + ] The DataManager has been destroyed")
    # END
