from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from keyboard.keyboard_delete_product import DeleteProductCallbackFactory
from models import Company, Product
from models.db_session import session_db
from ozon.utils import Utils

router = Router()


@router.callback_query(DeleteProductCallbackFactory.filter())
@session_db
async def delete_product(callback: CallbackQuery, callback_data: DeleteProductCallbackFactory, session: AsyncSession):
    # Извлечение данных из callback_data
    company_id = callback_data.company_id
    product_id = callback_data.product_id
    action_id = callback_data.action_id

    # Получение компании по ID
    company = await Company.get_by_id(company_id, session)
    util = Utils(company.api_key, company.client_id)

    # Деактивация промо продукта
    await util.promos_products_deactivate(action_id, [product_id])

    # Удаление продукта из базы данных
    await Product.delete_product(product_id, action_id, session)

    await callback.message.delete()

    await callback.answer("Продукт удален.")
