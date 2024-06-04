from aiogram import types

from utils.message import btn

keyboard = types.ReplyKeyboardMarkup(
    keyboard=[[types.KeyboardButton(text=btn("hello", "0"))]],
    resize_keyboard=True,
    one_time_keyboard=False
)
