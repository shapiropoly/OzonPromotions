from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from texts.message import check_connect, account
from texts.button import b_account, b_hello
from keyboard.inline_keyboard import make_keyboard
from utils.message import btn, msg

router = Router()


class Store(StatesGroup):
    writing_name = State()
    writing_client_id = State()
    writing_api_key = State()
    choosing_store = State()
    choosing_settings = State()
    choosing_moves = State()


@router.callback_query(Store.choosing_moves, F.data == (btn("hello", "0")))
async def name(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text=msg("account", "0"),
        reply_markup=ReplyKeyboardRemove()
    )
    # TODO Сделать добавление имени в БД
    await state.set_state(Store.writing_name)


@router.message(Store.writing_name)
async def client_id(message: Message, state: FSMContext):
    await message.answer(
        text=msg("account", "1"),
        reply_markup=ReplyKeyboardRemove()
    )
    # TODO Сделать добавление client-id в БД
    await state.set_state(Store.writing_client_id)


@router.message(Store.writing_client_id)
async def api_key(message: Message, state: FSMContext):
    await message.answer(
        text=msg("account", "2"),
        reply_markup=ReplyKeyboardRemove()
    )
    # TODO Сделать добавление api-key в БД

    await state.set_state(Store.writing_api_key)


# TODO добавить проверку наличия пользователя в БД
@router.message(Store.writing_api_key)
async def store_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_store=message.text.lower())
    await message.answer(
        text=msg("check_connect", "0"),
        # TODO добавить в b_account компании продавца, полученные из Озона
        reply_markup=make_keyboard(btn("account", "0"))
        )
    await state.set_state(Store.choosing_store)


@router.callback_query(Store.choosing_store, F.data == (btn("account", "3")))
async def account_settings(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Настройки аккаунта будут доступны здесь",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Store.choosing_settings)
