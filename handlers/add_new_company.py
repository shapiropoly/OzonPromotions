from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.connect_store import Process
from keyboard.main_keyboard import keyboard
from utils.message import msg

router = Router()


@router.callback_query(lambda c: c.data == "add_company")
async def client_id(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await callback_query.message.answer(
        text=msg("registration", "1"),
        reply_markup=keyboard
    )
    await state.set_state(Process.writing_client_id)
