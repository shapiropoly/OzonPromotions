import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config_reader import config
from handlers import common, personal_account, connect_store


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(config.bot_token.get_secret_value())

    dp.include_routers(common.router, personal_account.router, connect_store.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
