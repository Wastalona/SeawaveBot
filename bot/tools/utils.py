from enum import Enum


class Professions(Enum):
    CHEF: str = "CHEF"
    WAITER: str = "WAITER"
    BDISHWASHER: str = "BDISHWASHER"
    WDISHWASHER: str = "WDISHWASHER"
    CLEANER: str = "CLEANER"
    BACKER: str = "BACKER"
    ADMIN: str = "ADMIN"


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


__all__ = ["Professions", "Singleton"]