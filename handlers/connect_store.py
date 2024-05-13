from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from texts.message import check_connect
from texts.button import b_account
from handlers.personal_account import Person
from keyboard.inline_keyboard import make_keyboard


router = Router()


class Store(StatesGroup):
    choosing_store = State()
    choosing_settings = State()


# TODO добавить проверку наличия пользователя в БД
@router.message(Person.writing_api_key)
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
