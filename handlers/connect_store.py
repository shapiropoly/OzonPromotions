import asyncio

from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from sqlalchemy import select

from data.config import bot
from keyboard.account_keyboard import keyboard
from models import User, Company, Product
from models.db_session import session_db
from ozon.utils import Utils
from keyboard.inline_keyboard import make_keyboard
from utils.checking import checking_user_company, checking_user_client_id, checking_user_api_key
from utils.message import btn, msg
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.filters import Command

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


@session_db
async def send_daily_message(session: AsyncSession):
    # Получение пользователей из базы данных и отправка им сообщения
    users = await session.execute(select(User))
    for user in users.scalars():
        try:
            await bot.send_message(
                chat_id=user.telegram_id,
                text="Ежедневное сообщение",
                reply_markup=keyboard
            )
        except Exception as e:
            print(f"Failed to send message to {user.telegram_id}: {e}")


@router.message(Process.choosing_moves, F.text == (btn("hello", "0")))
@session_db
async def name(message: Message, state: FSMContext, session: AsyncSession):
    current_telegram_id = message.from_user.id
    result = await session.execute(select(User).filter(User.telegram_id == current_telegram_id))
    user = result.scalars().first()

    if user:
        if user.companies:
            # TODO проверить активность компании (т. е. апи-кей и клиент-айди должны подключаться к озону)
            await state.set_state(Process.account)
        else:
            print("Вы — юзер, но компания не активна, добавьте новую компанию")

            # тут проблема: нужно сделать добавление в БД юзера не в функции,
            # где мы забираем api-key, иначе работа идет некорректно

            # await callback_query.message.answer(
            #     text=msg("registration", "1"),
            #     reply_markup=ReplyKeyboardRemove()
            # )
            # await state.set_state(Process.writing_client_id)

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
    await message.answer(
        text=msg("registration", "3"),
        reply_markup=keyboard
    )
    await state.set_state(Process.writing_company_name)


@router.message(Process.writing_company_name)
@session_db
async def connection(message: Message, state: FSMContext, session: AsyncSession):
    # Отправка сообщения "Загрузка"
    loading_message = await message.answer(text="Загрузка...")

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

    # Проверка подключения client_id и api_key к озону
    util = Utils(await checking_user_api_key(user, company),
                 await checking_user_client_id(user, company))

    # Получение и сохранение продуктов
    products = await util.connection()
    for product in products:
        product['name'] = (await util.product_name(product['id']))['result']['name']
        product_instance = Product(product_id=product['id'], name=product['name'], price=product['price'],
                                   action_price=product['action_price'])
        company.products.append(product_instance)
        await product_instance.save(session=session)

    await company.save(session=session)

    # Установка нового состояния
    await state.set_state(Process.account)

    await loading_message.delete()

    await message.answer(text="Подключение прошло успешно!",
                         reply_markup=keyboard)

    # # Обновление сообщения
    # await loading_message.edit_reply_markup(text="Подключение прошло успешно!",
    #                                         reply_markup=keyboard)


# async def check_current_company(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
#     # TODO получить client-id api-key текущего пользователя в БД
#     current_telegram_id = callback_query.from_user.id
#     result = await session.execute(select(User).filter(User.telegram_id == current_telegram_id))
#     user = result.scalars().first()
#     print(user.companies)
#
#     # TODO если с компанией проблемы, то вывести ошибку текущей компании
#     if not user:
#         await callback_query.message.answer(
#             text=msg("registration", "0"),
#             reply_markup=ReplyKeyboardRemove()
#         )
#         await state.set_state(Process.writing_name)
#         print("Прошел вот тут")
#     # Перекидываем на аккаунт
#     else:
#         await state.set_state(Process.account)
#         print("Прошел тут")


# @router.callback_query(Process.check_current_company)
# @session_db
# async def check_current_company(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
#     current_telegram_id = callback_query.from_user.id
#     user = await User.get_user(telegram_id=current_telegram_id, session=session)
#     print(user)
#
#     if user and user.companies:
#         company = user.companies[0]
#         client_id = company.client_id
#         api_key = company.api_key
#         print(f"Client ID: {client_id}, API Key: {api_key}")
#
#         await state.set_state(Process.account)
#         print("Прошел тут")
#     else:
#         await callback_query.message.answer(
#             text=msg("registration", "0"),
#             reply_markup=ReplyKeyboardRemove()
#         )
#         await state.set_state(Process.writing_name)
#         print("Прошел вот тут")


# @router.callback_query(Process.check_current_company)
# @session_db
# async def check_current_company(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
#     user = await User.get_user(telegram_id=callback_query.from_user.id, session=session)
#
#     if user:
#         if user.companies:
#             company = user.companies[0]  # пользователь связан хотя бы с одной компанией
#             client_id = company.client_id
#             api_key = company.api_key
#             print(f"Client ID: {client_id}, API Key: {api_key}")
#
#             await state.set_state(Process.account)
#             print("Прошел тут 1")
#         else:
#             print("No companies associated with user")
#             await callback_query.message.answer(
#                 text=msg("registration", "0"),
#                 reply_markup=ReplyKeyboardRemove()
#             )
#             await state.set_state(Process.writing_name)
#             print("Прошел вот тут 1")
#     else:
#         print("User not found")
#         await callback_query.message.answer(
#             text=msg("registration", "0"),
#             reply_markup=ReplyKeyboardRemove()
#         )
#         await state.set_state(Process.writing_name)
#         print("Прошел вот тут 2")


@router.message(Process.account, F.text == (btn("hello", "0")))
async def account(message: Message, state: FSMContext):
    await message.answer(
        text=msg("account", "0"),
        # TODO сделать кнопки компаний юзера из бд
        reply_markup=make_keyboard([btn("account", "0"), btn("account", "1"), btn("account", "2")])
    )

    await state.set_state(Process.choosing_company)


@router.callback_query(Process.choosing_company, F.data == (btn("account", "2")))
async def account_settings(callback_query: CallbackQuery, state: FSMContext):
    # удалить команию, добавить компанию
    # TODO сделать удаление компании из БД по кнопкам (здесь также выводить список кнопок с компаниями)
    # TODO сделать добавление — проводим заново по состояниям добавления компании
    # при удалении компании, вывести список компаний в виде кнопок
    # аллерт с подтверждением
    await callback_query.message.answer(
        text="Настройки аккаунта будут доступны здесь",
        reply_markup=keyboard
    )
    await state.set_state(Process.account)


@router.callback_query(Process.manage_promotions)
async def actual_promotions(callback_query: CallbackQuery, state: FSMContext):
    # TODO закинуть все товары в акциях в БД
    # Раз в день проходится по новым товарам в акциях и сравнивать их с товарами в БД
    # Извлекаем по одному товару и создаем сообщение с ним с кнопкой
    await callback_query.message.answer(
        text="",
        reply_markup=keyboard
    )
    await state.set_state(Process.actual_promotions)

# @router.message(Command(commands=["1234"]))
# async def delete(message: Message, state: FSMContext):
#     await message.answer(
#         text="Вы точно хотите удалить товар из акции",
#         show_alert=True,
#         reply_markup=make_keyboard([btn("hello", "0")])
#     )
#     await state.set_state(Process.delete)
