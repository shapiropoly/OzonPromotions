from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from sqlalchemy import select
from sqlalchemy.orm import session

from models import User, Companies
from models.db_session import session_db
from texts.message import check_connect, account
from keyboard.inline_keyboard import make_keyboard
from utils.message import btn, msg
from sqlalchemy.ext.asyncio import AsyncSession

router = Router()


class Company(StatesGroup):
    writing_name = State()
    writing_client_id = State()
    writing_api_key = State()
    choosing_company = State()
    connection = State()
    choosing_settings = State()
    choosing_moves = State()
    connect = State()


@router.callback_query(Company.choosing_moves, F.data == (btn("hello", "0")))
@session_db
async def name(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    current_telegram_id = callback_query.from_user.id

    result = await session.execute(select(User).filter(User.telegram_id == current_telegram_id))
    user = result.scalars().first()

    if not user:
        await callback_query.message.answer(
            text=msg("account", "0"),
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(Company.writing_name)
    else:
        await state.set_state(Company.connect)


@router.message(Company.writing_name)
async def client_id(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        text=msg("account", "1"),
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Company.writing_client_id)


@router.message(Company.writing_client_id)
@session_db
async def api_key(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(client_id=message.text)
    data = await state.get_data()
    name = data.get("name")

    await message.answer(
        text=msg("account", "2"),
        reply_markup=ReplyKeyboardRemove()
    )
    user = User(name=name, telegram_id=message.from_user.id, username=message.from_user.username)
    await user.save(session=session)

    await state.set_state(Company.writing_api_key)


# TODO добавить проверку наличия пользователя в БД
@router.message(Company.connection)
async def company_name(message: Message, state: FSMContext):
    await state.update_data(company_name=message.text)
    await message.answer(
        text=msg("check_connect", "0"),
        # TODO добавить в b_account компании продавца, полученные из Озона
        reply_markup=make_keyboard([btn("account", "0"), btn("account", "1"), btn("account", "2")])
    )

    await state.set_state(Company.choosing_company)


@router.message(Company.writing_api_key)
@router.callback_query(Company.connect)
@session_db
async def connection(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    client_id = data.get("client_id")
    api_key = data.get("api_key")
    company_name = data.get("company_name")

    await callback_query.message.answer(
        text="Подключение прошло успешно!",
        reply_markup=ReplyKeyboardRemove()
    )

    company = Companies(client_id=client_id, api_key=api_key, company_name=company_name)
    await company.save(session=session)
    await state.set_state(Company.connection)


@router.callback_query(Company.choosing_settings, F.data == (btn("account", "2")))
async def account_settings(message: Message, state: FSMContext):
    # удалить команию, добавить компанию
    # при удалении компании, вывести список компаний в виде кнопок
    # аллерт с подтверждением
    await message.answer(
        text="Настройки аккаунта будут доступны здесь",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Company.choosing_moves)
