from .common_handlers import common_router
from .admin_handlers import admin_router
from .employee_handlers import employee_router


__all__ = ["common_router", "employee_router", "admin_router"]