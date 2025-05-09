import asyncio

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data.config import bot
from keyboard.keyboard_delete_product import make_keyboard_delete_products
from keyboard.main_keyboard import keyboard
from models import User, Company, Product
from models.db_session import session_db
from ozon.utils import Utils
from utils.checking import check_connection, check_double
from utils.message import msg
from utils.product_message import product_message

router = Router()


class Process(StatesGroup):
    writing_name = State()
    writing_client_id = State()
    writing_api_key = State()
    writing_company_name = State()
    check_current_company = State()
    choosing_company = State()
    account = State()
    choosing_settings = State()
    choosing_moves = State()
    connect = State()
    manage_promotions = State()
    actual_promotions = State()
    delete = State()


async def send_daily_message(message, session, user_id: int):
    try:
        while True:
            user = await User.get_user(message.from_user.id, session)
            companies = user.companies
            for company in companies:

                company_id = company.id
                api_key = company.api_key
                client_id = company.client_id

                util = Utils(api_key, client_id)
                products = await util.connection()
                new_products = await db_compare_products(util, products, session)

                await db_add_products(session, util, company, products)

                for new_product in new_products:
                    product_msg = product_message(new_product)
                    await bot.send_message(chat_id=user_id, text=product_msg,
                                           reply_markup=make_keyboard_delete_products(new_product, company_id))

            #  тут, ниже, время указывается в секундах (сутки – 86400)
            await asyncio.sleep(86400)
    except Exception as e:
        print(f"Failed to send message to {user_id}: {e}")


@router.message(Process.writing_name)
async def client_id(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        text=msg("registration", "1"),
        reply_markup=keyboard
    )
    await state.set_state(Process.writing_client_id)


@router.message(Process.writing_client_id)
@session_db
async def api_key(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(client_id=message.text)

    current_telegram_id = message.from_user.id
    result = await session.execute(select(User).filter(User.telegram_id == current_telegram_id))
    user = result.scalars().first()

    data = await state.get_data()
    name = data.get("name")

    await message.answer(
        text=msg("registration", "2"),
        reply_markup=keyboard
    )

    if not user:
        user = User(name=name, telegram_id=message.from_user.id, username=message.from_user.username)
        await user.save(session=session)

    await state.set_state(Process.writing_api_key)


@router.message(Process.writing_api_key)
async def company_name(message: Message, state: FSMContext):
    await state.update_data(api_key=message.text)
    await message.answer(
        text=msg("registration", "3"),
        reply_markup=keyboard
    )
    await state.set_state(Process.writing_company_name)


async def db_add_products(session, util, company, products):
    await Product.clear_products_table(client_id=company.client_id, session=session)

    for product in products:
        product['name'] = (await util.product_name(product['id']))['result']['name']
        product_instance = Product(product_id=product['id'],
                                   name=product['name'],
                                   price=product['price'],
                                   action_price=product['action_price'],
                                   action_id=product['action_id'],
                                   action_title=product['action_title'])
        company.products.append(product_instance)

        await product_instance.save(session=session)


async def db_compare_products(util, products, session):
    new_products = []

    for product in products:
        check_product = await Product.get_product(product_id=product['id'], action_id=product['action_id'],
                                                  session=session)
        if not check_product:
            new_products.append(product)

    for product in new_products:
        product['name'] = (await util.product_name(product['id']))['result']['name']

    return new_products


@router.message(Process.writing_company_name)
@session_db
async def connection(message: Message, state: FSMContext, session: AsyncSession):
    # Обновление данных состояния
    await state.update_data(company_name=message.text)
    data = await state.get_data()
    client_id = data.get("client_id")
    api_key = data.get("api_key")
    company_name = data.get("company_name")

    # Получение пользователя
    user = await User.get_user(message.from_user.id, session)

    if await check_connection(client_id, api_key) == 400:
        await message.answer(
            text=msg("registration", "4"),
            reply_markup=keyboard
        )
        await state.set_state(Process.writing_client_id)

    elif await check_double(client_id, api_key, session):

        # Если 2 сотрудника реагют одну компанию с разных аккаунтов

        new_company = await Company.get_by_client_id(client_id, session)

        for company in user.companies:

            if company == new_company:
                # Если пользователь 2 раза регает одну компанию
                await message.answer(
                    text=msg("registration", "5"),
                    reply_markup=keyboard
                )
                await state.set_state(Process.account)

                for message_id in range(6):
                    await message.chat.delete_message(message.message_id - message_id)

                return

        user.companies.append(new_company)

        await new_company.save(session=session)

        for message_id in range(6):
            await message.chat.delete_message(message.message_id - message_id)

        await message.answer(text=msg("download", "0"),
                             reply_markup=keyboard)

        await state.set_state(Process.account)

    else:
        # Создание и добавление компании
        company = Company(client_id=client_id, api_key=api_key, company_name=company_name)
        user.companies.append(company)

        loading_message = await message.answer(text=msg("download", "1"))

        util = Utils(company.api_key, company.client_id)

        # Получение и сохранение продуктов
        products = await util.connection()
        await db_add_products(session, util, company, products)
        await company.save(session=session)

        await loading_message.delete()

        for message_id in range(6):
            await message.chat.delete_message(message.message_id - message_id)

        await message.answer(text=msg("download", "0"),
                             reply_markup=keyboard)

        await state.set_state(Process.account)
