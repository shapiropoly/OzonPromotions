import asyncio
import logging
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from handlers import common, connect_store
from data.config import bot
from handlers.connect_store import send_daily_message
from models.db_session import global_init


async def main():
    await global_init()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(common.router, connect_store.router)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_daily_message, CronTrigger(hour=14, minute=52))
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
