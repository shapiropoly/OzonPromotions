import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import common, connect_store
from data.config import bot


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(common.router, connect_store.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())