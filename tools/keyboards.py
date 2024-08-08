from aiogram.types import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    KeyboardButton, 
    ReplyKeyboardMarkup, 
)


employee_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Open shift"),
            KeyboardButton(text="Close shift"),
        ],
        [
            KeyboardButton(text="📷 Photo"),
            KeyboardButton(text="🎬 Video"),
        ],
        [
            KeyboardButton(text="✖ Close"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📔 Reports"),
            KeyboardButton(text="📝 Report card"),
            KeyboardButton(text="🔔 Notify"),
        ],
        [
            KeyboardButton(text="Hire employee ⛏"),
            KeyboardButton(text="Release employee ⛏"),
            KeyboardButton(text="Transfer employee ⚒"),
        ],
        [
            KeyboardButton(text="📒 Employees list"),
            KeyboardButton(text="✖ Close"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

s__all__ = ["admin_kb", "employee_kb"]