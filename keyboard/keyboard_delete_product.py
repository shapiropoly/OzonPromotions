from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.message import btn


class DeleteProductCallbackFactory(CallbackData, prefix="delete_product"):
    product_id: int
    action_id: int
    company_id: int


def make_keyboard_delete_products(product, company_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=btn("promotions", "0"),
                   callback_data=DeleteProductCallbackFactory(product_id=product['id'],
                                                              action_id=product['action_id'],
                                                              company_id=company_id))
    builder.adjust(1)
    return builder.as_markup()
