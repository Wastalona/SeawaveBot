from aiogram.fsm.state import StatesGroup, State


# ~~~ EMPLOYEE ~~~
class SendReports(StatesGroup):
    photo = State()
    video = State()


class Shifts(StatesGroup):
    open_ = State()
    close_ = State()


# ~~~ ADMIN ~~~
class GetReports(StatesGroup):
    reports = State()
    report_card = State()


class EmployeesEditor(StatesGroup):
    hire = State()
    release = State()
    transfer = State()
    view_empl = State()

notify = State()