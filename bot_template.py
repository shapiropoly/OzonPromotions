import asyncio
import aiogram
from aiogram import Bot, Dispatcher, types
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import State, StatesGroup
import aiopg
from models.db_session import get_database_url
from data.config import BOT_TOKEN, db_url


async def create_pool(url):
    return await aiopg.create_pool(dsn=url)


async def insert_user_data(name, surname, api_key, client_id):
    async with create_pool(db_url) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT INTO users (name, surname, api-key, client_id) VALUES (%s, %s, %s)",
                    (name, surname, api_key, client_id)
                )
                await conn.commit()


async def start_handler(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    button_personal_cabinet = types.InlineKeyboardButton("Личный кабинет", callback_data="personal_cabinet")
    button_connect_shop = types.InlineKeyboardButton("Подключить магазин", callback_data="connect_shop")
    keyboard.add(button_personal_cabinet, button_connect_shop)
    await message.answer("Выберите действие:", reply_markup=keyboard)


async def connect_shop(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Для регистрации введите своё имя:")
    await RegisterStates.name.set()


async def register_name(message: types.Message, state: aiogram.dispatcher.FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer("Теперь введите свою фамилию:")
    await RegisterStates.surname.set()


async def register_surname(message: types.Message, state: aiogram.dispatcher.FSMContext):
    async with state.proxy() as data:
        data['surname'] = message.text
    await message.answer("Отлично! Теперь введите ваш api-key:")
    await RegisterStates.id.set()


async def register_id(message: types.Message, state: aiogram.dispatcher.FSMContext):
    async with state.proxy() as data:
        data['api'] = message.text
        await insert_user_data(data['name'], data['surname'], data['api'], message.from_user.id)
    await message.answer("Спасибо за регистрацию! Теперь вы можете перейти в личный кабинет.")


async def personal_cabinet(callback_query: types.CallbackQuery):
    # Здесь запросить данные о компаниях продавца из базы данных
    companies = ["Компания 1", "Компания 2", "Компания 3"]

    # Создаем inline клавиатуру с кнопками для каждой компании
    keyboard = types.InlineKeyboardMarkup()
    for company in companies:
        keyboard.add(types.InlineKeyboardButton(company, callback_data=f"company_{company.replace(' ', '_')}"))
    keyboard.add(types.InlineKeyboardButton("Настройки аккаунта", callback_data="account_settings"))

    # Отправляем сообщение с кнопками
    await callback_query.message.answer("Список компаний продавца:", reply_markup=keyboard)


# Обработчики для кнопок компаний и настроек аккаунта
async def company_button_handler(callback_query: types.CallbackQuery):
    company_name = callback_query.data.split("_", 1)[1].replace('_', ' ')
    await callback_query.answer(f"Вы выбрали компанию: {company_name}")


async def account_settings(callback_query: types.CallbackQuery):
    await callback_query.answer("Настройки аккаунта будут доступны здесь")


async def main():
    # Инициализация бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)

    # Регистрация хэндлеров
    dp.register_message_handler(start_handler, commands="start")
    dp.register_message_handler(register_name, state=RegisterStates.name)
    dp.register_message_handler(register_surname, state=RegisterStates.surname)
    dp.register_message_handler(register_id, state=RegisterStates.id)
    dp.register_callback_query_handler(connect_shop, text="connect_shop")
    dp.register_callback_query_handler(personal_cabinet, text="personal_cabinet")
    dp.register_callback_query_handler(company_button_handler, lambda c: c.data.startswith('company_'))
    dp.register_callback_query_handler(account_settings, text="account_settings")

    # Запуск бота
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())