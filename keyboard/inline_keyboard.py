from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def make_keyboard(items: list[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in items:
        builder.add(types.InlineKeyboardButton(
            text=item,
            callback_data=f"{item}")
        )
    builder.adjust(1)
    return builder.as_markup()
