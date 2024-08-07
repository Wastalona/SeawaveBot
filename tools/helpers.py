                    
import pytz
from datetime import datetime

from icecream import ic


def get_time(tz:str = "Europe/Moscow", ts_view:bool = False):
    """
    tz - time zone
    ts_view - return the result in timestamp format
    This function returns the time in the selected time zone.
    """
    _tz = pytz.all_timezones(tz) # Setting the time zone
    return ic(datetime.now(_tz)) if ts_view else ic(datetime.now(_tz).timestamp())
