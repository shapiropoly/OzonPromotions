import asyncio

from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from handlers.connect_store import Process, send_daily_message
from keyboard.keyboard_account import make_keyboard_account
from models import User
from models.db_session import session_db
from utils.message import btn, msg

router = Router()


@router.message(Process.account)
@router.message(Process.account, F.text == (btn("hello", "0")))
@session_db
async def account(message: Message, session: AsyncSession):
    await message.delete()
    user = await User.get_user(message.from_user.id, session)
    companies = user.companies
    await message.answer(
        text=msg("account", "0"),
        reply_markup=make_keyboard_account(companies)
    )
    await asyncio.create_task(send_daily_message(message=message, session=session, user_id=message.from_user.id))
