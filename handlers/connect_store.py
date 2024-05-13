from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from handlers.common import Common
from texts.message import check_connect, account
from texts.button import b_account, b_hello
from keyboard.inline_keyboard import make_keyboard


router = Router()


class Store(StatesGroup):
    writing_name = State()
    writing_client_id = State()
    writing_api_key = State()
    choosing_store = State()
    choosing_settings = State()


@router.callback_query(Common.choosing_moves, F.data == (b_hello[0]))
async def name(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text=account[0],
        reply_markup=ReplyKeyboardRemove()
    )
    # TODO Сделать добавление имени в БД
    await state.set_state(Store.writing_name)


@router.message(Store.writing_name)
async def surname(message: Message, state: FSMContext):
    await message.answer(
        text=account[2],
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        text=account[3],
        reply_markup=ReplyKeyboardRemove()
    )
    # TODO Сделать добавление client-id в БД
    await state.set_state(Store.writing_client_id)


@router.message(Store.writing_client_id)
async def surname(message: Message, state: FSMContext):
    await message.answer(
        text=account[4],
        reply_markup=ReplyKeyboardRemove()
    )
    # TODO Сделать добавление api-key в БД

    await state.set_state(Store.writing_api_key)


# TODO добавить проверку наличия пользователя в БД
@router.message(Store.writing_api_key)
async def store_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_store=message.text.lower())
    await message.answer(
        text=check_connect[0],
        # TODO добавить в b_account компании продавца, полученные из Озона
        reply_markup=make_keyboard(b_account)
    )
    await state.set_state(Store.choosing_store)


@router.callback_query(Store.choosing_store, F.data == (b_account[-1]))
async def account_settings(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Настройки аккаунта будут доступны здесь",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Store.choosing_settings)
