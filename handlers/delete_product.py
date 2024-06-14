import asyncio

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from sqlalchemy import select, and_

from data.config import bot
from handlers.connect_store import db_compare_products, db_add_products
from handlers.registration import Registration
from keyboard.account_keyboard import keyboard
from keyboard.keyboard_account import CompanyCallbackFactory
from keyboard.keyboard_delete_product import make_keyboard_delete_products, DeleteProductCallbackFactory
from models import User, Company, Product
from models.db_session import session_db
from ozon.utils import Utils
from keyboard.inline_keyboard import make_keyboard
from utils.checking import checking_user_company, checking_user_client_id, checking_user_api_key
from utils.message import btn, msg
from sqlalchemy.ext.asyncio import AsyncSession
from utils.product_message import product_message

router = Router()


# async def send_daily_message(message, session, user_id: int):
#     try:
#         while True:
#             user = await User.get_user(message.from_user.id, session)
#             companies = user.companies
#             for company in companies:
#
#                 api_key = await checking_user_api_key(user, company)
#                 client_id = await checking_user_client_id(user, company)
#
#                 util = Utils(api_key, client_id)
#
#                 products = await util.connection()
#
#                 new_products = await db_compare_products(util, products, session)
#
#                 await db_add_products(session, util, company, products)
#
#                 for new_product in new_products:
#                     product_msg = product_message(new_product)
#                     await bot.send_message(chat_id=user_id, text=product_msg,
#                                            reply_markup=make_keyboard_delete_products(new_product, api_key, client_id))
#
#             await bot.send_message(chat_id=user_id, text="Ежедневное сообщение")
#             #  тут, ниже, время указывается в секундах (сутки – 86400)
#             await asyncio.sleep(30)
#     except Exception as e:
#         print(f"Failed to send message to {user_id}: {e}")


@router.callback_query(DeleteProductCallbackFactory.filter())
@session_db
async def delete_product(callback_data: DeleteProductCallbackFactory,
                         session: AsyncSession):
    util = Utils(callback_data.api_key, callback_data.client_id)
    await util.promos_products_deactivate(callback_data.product_id, callback_data.action_id)
    await Product.delete_product(callback_data.product_id, callback_data.action_id, session)
