from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from keyboard.main_keyboard import keyboard
from utils.message import msg

router = Router()


class Registration(StatesGroup):
    writing_client_id = State()
    writing_api_key = State()
    writing_company_name = State()


@router.callback_query(lambda c: c.data == "add_company")
async def client_id(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer(
        text=msg("registration", "1"),
        reply_markup=keyboard
    )
    await state.set_state(Registration.writing_client_id)


@router.message(Registration.writing_client_id)
async def api_key(message: Message, state: FSMContext):
    await state.update_data(client_id=int(message.text))

    await message.answer(
        text=msg("registration", "2"),
        reply_markup=keyboard
    )

    await state.set_state(Registration.writing_api_key)


@router.message(Registration.writing_api_key)
async def company_name(message: Message, state: FSMContext):
    await state.update_data(api_key=message.text)
    # TODO сделать проверку на клиент айди + апи кей в бд.
    #  Если они есть в бд, то не регистрируем компанию и не просим вводить название
    #  + сказать, что компания есть в БД

    await message.answer(
        text=msg("registration", "3"),
        reply_markup=keyboard
    )
    await state.set_state(Registration.writing_company_name)
