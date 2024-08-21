from aiogram.fsm.state import StatesGroup, State


# ~~~ EMPLOYEE ~~~
class SendReports(StatesGroup):
    photo = State()
    video = State()
    

# ~~~ ADMIN ~~~
class StaffEditor(StatesGroup):
    hire = State()
    release = State()
    transfer = State()
    view_empl = State()


class Notification(StatesGroup):
    notify = State()
