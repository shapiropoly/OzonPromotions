import json
import os

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

MESSAGES = json.load(open("texts/message.json", encoding="utf-8"))
BUTTONS = json.load(open("texts/button.json", encoding="utf-8"))

load_dotenv("data/token.env")
storage = MemoryStorage()
BOT_TOKEN = os.getenv('token')

bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
