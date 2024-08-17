                    
import logging
import pytz
from datetime import datetime
from functools import wraps

from icecream import ic

from redis.exceptions import ConnectionError
from cryptography.fernet import InvalidToken


def get_time(tz:str = "Europe/Moscow", ts_view:bool = False):
    """
    tz - time zone
    ts_view - return the result in timestamp format
    This function returns the time in the selected time zone.
    """
    _tz = pytz.all_timezones(tz) # Setting the time zone
    return datetime.now(_tz) if ts_view else datetime.now(_tz).timestamp()


def redis_exceptions(func):
    """Error handling when working with redis"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            await func(*args, **kwargs)
        except InvalidToken as err:
            logging.error("Invalid token.")
            ic(err, err.__class__)
            return err
        except ConnectionError as err:
            logging.error("Connection error, check your internet connection or server connection.")
            ic(err, err.__class__)
            return err
        except Exception as err:
            logging.error(f"Something went wrong: {err}.\nClass error = {err.__class__}")
            ic(err, err.__class__)
            return err
        finally:
            await args[0].close()

    return wrapper


def wrap_data(*data) -> dict:
    try:
        json_data: dict = dict()
        json_data["_admins"] = [admin.decode() for admin in data[0]]
        json_data["blocked"] = [block.decode() for block in data[1]]
        json_data["employees_ids"] = [empl_id.decode() for empl_id in data[2]]
    except IndexError as err:
        ic(err, err.__class__)
    
    merge = {**json_data, **data[3]}
    return merge