from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from texts.message import hello
from texts.button import b_hello

from keyboard.inline_keyboard import make_keyboard

router = Router()


class Common(StatesGroup):
    choosing_moves = State()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=hello[0],
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        text="Выберите действие:",
        reply_markup=make_keyboard(b_hello)
    )
    await state.set_state(Common.choosing_moves)


@router.message(StateFilter(None), Command(commands=["cancel"]))
@router.message(default_state, F.text.lower() == "отмена")
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    await state.set_data({})
    await message.answer(
        text="Нечего отменять",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )
