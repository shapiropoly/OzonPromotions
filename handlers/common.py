from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove

from handlers.connect_store import Company
from keyboard.inline_keyboard import make_keyboard
from utils.message import msg, btn


router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=msg("hello", "0"),
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        text=msg("system", "0"),
        reply_markup=make_keyboard([btn("hello", "0")])
    )
    await state.set_state(Company.choosing_moves)


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
