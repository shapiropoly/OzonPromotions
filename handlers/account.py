import asyncio

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from sqlalchemy import select, and_

from data.config import bot
from handlers.connect_store import Process
from keyboard.account_keyboard import keyboard
from keyboard.keyboard_account import CompanyCallbackFactory, make_keyboard_account
from models import User, Company, Product
from models.db_session import session_db
from ozon.utils import Utils
from keyboard.inline_keyboard import make_keyboard
from utils.checking import checking_user_company, checking_user_client_id, checking_user_api_key
from utils.message import btn, msg
from sqlalchemy.ext.asyncio import AsyncSession
from utils.product_message import product_message

router = Router()


@router.message(Process.account, F.text == (btn("hello", "0")))
@session_db
async def account(message: Message, session: AsyncSession):
    user = await User.get_user(message.from_user.id, session)
    companies = user.companies
    print(companies)
    await message.answer(
        text=msg("account", "0"),
        reply_markup=make_keyboard_account(companies)
    )
