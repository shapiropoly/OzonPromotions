from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from handlers.connect_store import Process
from keyboard.main_keyboard import keyboard
from models import User
from models.db_session import session_db
from utils.checking import check_connection
from utils.message import msg

router = Router()


@router.message(Command(commands=["start"]))
@session_db
async def cmd_start(message: Message, state: FSMContext, session: AsyncSession):
    await state.clear()
    await message.answer(
        text=msg("hello", "0"),
        reply_markup=keyboard
    )

    current_telegram_id = message.from_user.id
    result = await session.execute(select(User).filter(User.telegram_id == current_telegram_id))
    user = result.scalars().first()

    if user:

        companies = user.companies

        if companies:
            for company in companies:
                if await check_connection(company.client_id, company.api_key) == 400:
                    # Данные для подключения корректны, но ошибка со стороны Озона
                    await message.answer(
                        text=msg("check_connect", "2"),
                        reply_markup=keyboard
                    )
                    return

            await message.answer(
                text=msg("system", "0"),
                reply_markup=keyboard
            )

            await state.set_state(Process.account)

        # перекинуть на регистрацию компании
        else:
            await message.answer(
                text=msg("registration", "1"),
                reply_markup=keyboard
            )
            await state.set_state(Process.writing_client_id)

    else:
        # создать личный кабинет
        await message.answer(
            text=msg("registration", "0"),
            reply_markup=keyboard
        )
        await state.set_state(Process.writing_name)


@router.message(StateFilter(None), Command(commands=["cancel"]))
@router.message(default_state, F.text.lower() == msg("commands", "0"))
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    await state.set_data({})
    await message.answer(
        text=msg("system", "1"),
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == msg("commands", "0"))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=msg("system", "2"),
        reply_markup=ReplyKeyboardRemove()
    )
