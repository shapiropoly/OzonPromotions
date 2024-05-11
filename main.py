import asyncio
import logging
# from aiogram import Dispatcher
# from aiogram.fsm.state import StatesGroup, State
#
# from data.config import bot
# from data.config import storage
# from models.db_session import global_init
# from handlers import start
# from utils.language import LangMiddleware
#
#
# class MailMessage(StatesGroup):
#     message = State()
#
#
# # Включаем логирование, чтобы не пропустить важные сообщения
# logging.basicConfig(level=logging.INFO)
# # Объект бота
#
# # Диспетчер
# dp = Dispatcher(storage=storage)
#
# dp.include_routers(start.router, select_language.router, fill_profile.router, edit_photo.router,
#                    edit_description.router, view_profiles.router, send_reaction.router, respond_reaction.router,
#                    my_profile.router, enable_disable_profile.router, disagree_profile.router, mail.router)
#
#
#
# async def main():
#     await global_init()
#     await dp.start_polling(bot)
#
#
# if __name__ == "__main__":
#     asyncio.run(main())