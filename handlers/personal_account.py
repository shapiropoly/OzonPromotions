from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from handlers.common import Common
from texts.button import b_hello
from texts.message import account

router = Router()


class Person(StatesGroup):
    writing_name = State()
    writing_surname = State()
    writing_client_id = State()
    writing_api_key = State()


@router.callback_query(Common.choosing_moves, F.data == (b_hello[0]))
async def name(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text=account[0],
        reply_markup=ReplyKeyboardRemove()
    )
    # TODO Сделать добавление имени в БД
    await state.set_state(Person.writing_name)


@router.message(Person.writing_name)
async def surname(message: Message, state: FSMContext):
    await message.answer(
        text=account[1],
        reply_markup=ReplyKeyboardRemove()
    )
    # TODO Сделать добавление фамилии в БД
    await state.set_state(Person.writing_surname)


@router.message(Person.writing_surname)
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
    await state.set_state(Person.writing_client_id)


@router.message(Person.writing_client_id)
async def surname(message: Message, state: FSMContext):
    await message.answer(
        text=account[4],
        reply_markup=ReplyKeyboardRemove()
    )
    # TODO Сделать добавление api-key в БД

    await state.set_state(Person.writing_api_key)
