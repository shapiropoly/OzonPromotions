import asyncio

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from sqlalchemy import select, and_

from data.config import bot
# from handlers.delete_product import send_daily_message
from handlers.registration import Registration
from keyboard.main_keyboard import keyboard
from keyboard.keyboard_account import CompanyCallbackFactory
from keyboard.keyboard_delete_product import make_keyboard_delete_products
from models import User, Company, Product
from models.db_session import session_db
from ozon.utils import Utils
from keyboard.inline_keyboard import make_keyboard
from utils.checking import checking_user_company, checking_user_client_id, checking_user_api_key, checking_connection
from utils.message import btn, msg
from sqlalchemy.ext.asyncio import AsyncSession
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

            await bot.send_message(chat_id=user_id, text="Ежедневное сообщение")
            #  тут, ниже, время указывается в секундах (сутки – 86400)
            await asyncio.sleep(10)
    except Exception as e:
        print(f"Failed to send message to {user_id}: {e}")


@router.message(Process.choosing_moves, F.text == (btn("hello", "0")))
@session_db
async def name(message: Message, state: FSMContext, session: AsyncSession):
    current_telegram_id = message.from_user.id
    result = await session.execute(select(User).filter(User.telegram_id == current_telegram_id))
    user = result.scalars().first()

    if user:
        print("Вы – юзер")
        company = user.companies

        if company:
            if checking_connection(user, company) == 200:
                print("Подключение к озону прошло успешно")
                # перекидываем в личный кабинет
                await state.set_state(Process.account)
            else:
                # перекинуть на повторный ввод клиент-айди и апи-кей, название оставляем то же самое
                print("У вас зарегана компания, но она не подключается к озону")
        # перекинуть на регистрацию компании
        else:
            print("Вы — юзер, но у вас нет компаний. зарегайте компанию")

    # перекидываем на регистрацию
    else:
        print("Вы — не юзер")
        await message.answer(
            text=msg("registration", "0"),
            reply_markup=keyboard
        )
        await state.set_state(Process.writing_name)


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
    await state.update_data(client_id=int(message.text))
    data = await state.get_data()
    name = data.get("name")

    await message.answer(
        text=msg("registration", "2"),
        reply_markup=keyboard
    )

    user = User(name=name, telegram_id=message.from_user.id, username=message.from_user.username)
    await user.save(session=session)

    await state.set_state(Process.writing_api_key)


@router.message(Process.writing_api_key)
async def company_name(message: Message, state: FSMContext):
    await state.update_data(api_key=message.text)
    # TODO сделать проверку на клиент айди + апи кей в бд.
    #  Если они есть в бд, то не регистрируем компанию и не просим вводить название
    #  + сказать, что компания есть в БД

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
                                   action_id=product['action_id'])
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
@router.message(Registration.writing_company_name)
@session_db
async def connection(message: Message, state: FSMContext, session: AsyncSession):
    # Отправка сообщения "Загрузка"
    loading_message = await message.answer(text="Подождите чуть-чуть, идет загрузка ваших товаров...")

    # Обновление данных состояния
    await state.update_data(company_name=message.text)
    data = await state.get_data()
    client_id = data.get("client_id")
    api_key = data.get("api_key")
    company_name = data.get("company_name")

    # Получение пользователя
    user = await User.get_user(message.from_user.id, session)

    # Создание и добавление компании
    company = Company(client_id=client_id, api_key=api_key, company_name=company_name)
    user.companies.append(company)

    # TODO добавить Проверку подключения client_id и api_key к озону

    util = Utils(api_key, client_id)

    # Получение и сохранение продуктов
    products = await util.connection()

    await db_add_products(session, util, company, products)

    await company.save(session=session)

    # Установка нового состояния
    await state.set_state(Process.account)

    await loading_message.delete()

    await message.answer(text="Подключение прошло успешно!",
                         reply_markup=keyboard)

    await asyncio.create_task(send_daily_message(message=message, session=session, user_id=message.from_user.id))



@router.callback_query(Process.choosing_company)
async def account_settings(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer(
        text=msg("account", "1"),
        reply_markup=make_keyboard([btn("settings", "0"), btn("settings", "1")])
    )
    await state.set_state(Process.choosing_settings)