from typing import Optional

from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from models import Company
from utils.message import btn


class CompanyCallbackFactory(CallbackData, prefix="company"):
    id: int


def make_keyboard_account(companies: list[Company]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for company in companies:
        builder.button(text=btn("account", "0"), callback_data=CompanyCallbackFactory(id=company.id))
    builder.adjust(1)
    return builder.as_markup()