import asyncio
from aiogram import Router, types
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from keyboard.keyboard_account import CompanyCallbackFactory
from models import Company, Product
from models.db_session import session_db
from ozon.utils import Utils

router = Router()


# Обработчик для вывода alert с кнопками "Да" и "Нет"
@router.callback_query(CompanyCallbackFactory.filter())
async def delete_company(callback: CallbackQuery, callback_data: CompanyCallbackFactory):
    await callback.message.delete()
    # Создание inline-клавиатуры с кнопками "Да" и "Нет"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data=f"confirm_delete_company:{callback_data.id}"),
            InlineKeyboardButton(text="Нет", callback_data="cancel_delete_company")
        ]
    ])

    await callback.message.answer("Удалить компанию?", reply_markup=keyboard)


# Обработчик для подтверждения удаления компании
@router.callback_query(lambda c: c.data and c.data.startswith("confirm_delete_company"))
@session_db
async def confirm_delete_company(callback: CallbackQuery, session: AsyncSession):
    id = int(callback.data.split(":")[1])

    company = await Company.get_by_id(id, session)
    if company:
        await company.delete_company(id, session)
        await callback.message.answer(f'Компания "{company.company_name}" успешно удалена')
    else:
        await callback.message.answer("Компания не найдена")

    await callback.message.delete()


# Обработчик для отмены удаления компании
@router.callback_query(lambda c: c.data == "cancel_delete_company")
async def cancel_delete_company(callback: CallbackQuery):
    await callback.message.delete()
