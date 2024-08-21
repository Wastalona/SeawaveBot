from enum import Enum


class Professions(Enum):
    CHEF: str = "CHEF"
    WAITER: str = "WAITER"
    BDISHWASHER: str = "BDISHWASHER"
    WDISHWASHER: str = "WDISHWASHER"
    CLEANER: str = "CLEANER"
    BACKER: str = "BACKER"
    ADMIN: str = "ADMIN"


class DaysPeriods(Enum):
    Morning = list(range(6, 11))
    Afternoon = list(range(11, 15))
    Dinner = list(range(15, 22))


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


__all__ = ["Professions", "Singleton"]