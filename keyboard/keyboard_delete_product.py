from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.message import btn


class DeleteProductCallbackFactory(CallbackData, prefix="delete_product"):
    product_id: int
    action_id: int
    api_key: str
    client_id: int


def make_keyboard_delete_products(product, api_key, client_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=btn("account", "0"),
                   callback_data=DeleteProductCallbackFactory(product_id=product['product_id'],
                                                              action_price=product['action_id'],
                                                              api_key=api_key,
                                                              client_id=client_id))
    builder.adjust(1)
    return builder.as_markup()
