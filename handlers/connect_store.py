from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from sqlalchemy import select
from sqlalchemy.orm import session

from keyboard.keyboard_account import make_keyboard_account
from models import User, Company
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
    writing_company_name = State()
    check_current_company = State()
    choosing_company = State()
    account = State()
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
            text=msg("registration", "0"),
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(Company.writing_name)
    else:
        await state.set_state(Company.check_current_company)


@router.message(Company.writing_name)
async def client_id(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        text=msg("registration", "1"),
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Company.writing_client_id)


@router.message(Company.writing_client_id)
@session_db
async def api_key(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(client_id=int(message.text))
    data = await state.get_data()
    name = data.get("name")

    await message.answer(
        text=msg("registration", "2"),
        reply_markup=ReplyKeyboardRemove()
    )

    user = User(name=name, telegram_id=message.from_user.id, username=message.from_user.username)
    await user.save(session=session)

    await state.set_state(Company.writing_api_key)


@router.message(Company.writing_api_key)
async def company_name(message: Message, state: FSMContext):
    await state.update_data(api_key=message.text)
    await message.answer(
        text=msg("registration", "3"),
        # TODO добавить в b_account компании продавца, полученные из Озона
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Company.writing_company_name)


@router.message(Company.writing_company_name)
@session_db
async def connection(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(company_name=message.text)
    data = await state.get_data()
    client_id = data.get("client_id")
    api_key = data.get("api_key")
    company_name = data.get("company_name")

    # TODO добавить проверку на актуальность client-id api-key
    # TODO если все ок, перебрасывать на state account, если нет запрашивать повторно

    user = await User.get_user(message.from_user.id, session)
    await message.answer(
        text="Подключение прошло успешно!",
        reply_markup=make_keyboard_account(user.companies)
    )
    company = Company(client_id=client_id, api_key=api_key, company_name=company_name)
    await company.save(session=session)
    await state.set_state(Company.account)


@router.callback_query(Company.check_current_company)
@session_db
async def check_current_company(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    # TODO проверить client-id api-key текущего пользователя в БД
    current_telegram_id = callback_query.from_user.id
    result = await session.execute(select(User).filter(User.telegram_id == current_telegram_id))
    user = result.scalars().first()

    # TODO если с компанией проблемы, то вывести ошибку текущей компании
    if not user:
        await callback_query.message.answer(
            text=msg("registration", "0"),
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(Company.writing_name)
    # TODO если все ок, то вывести список компаний
    else:
        await state.set_state(Company.account)


# TODO добавить проверку наличия пользователя в БД
@router.message(Company.account)
async def account(message: Message, state: FSMContext):
    await message.answer(
        text=msg("account", "0"),
        # TODO сделать кнопки компаний юзера из бд
        reply_markup=make_keyboard([btn("account", "0"), btn("account", "1"), btn("account", "2")])
    )

    await state.set_state(Company.choosing_company)


@router.callback_query(Company.choosing_settings, F.data == (btn("account", "2")))
async def account_settings(message: Message, state: FSMContext):
    # удалить команию, добавить компанию
    # TODO сделать удаление компании из БД по кнопкам (здесь также выводить список кнопок с компаниями)
    # TODO сделать добавление — проводим заново по состояниям добавления компании
    # при удалении компании, вывести список компаний в виде кнопок
    # аллерт с подтверждением
    await message.answer(
        text="Настройки аккаунта будут доступны здесь",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Company.choosing_moves)
