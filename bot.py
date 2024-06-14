import asyncio
import logging
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import common, connect_store, account
from data.config import bot
from models.db_session import global_init


async def main():
    await global_init()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(common.router, connect_store.router, account.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
