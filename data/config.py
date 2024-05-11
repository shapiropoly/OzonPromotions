import json
import os
from pathlib import Path
from os import environ

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from models.db_session import get_database_url


load_dotenv("data/token.env")
load_dotenv("data/data.env")

BOT_TOKEN = os.getenv("token")
db_url = get_database_url
# MESSAGES = json.load(open("texts/message.json", encoding="utf-8"))
# BUTTONS = json.load(open("texts/button.json", encoding="utf-8"))

bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

load_dotenv("data/token.env")
storage = MemoryStorage()

BASE_DIR = Path(__file__).parent.parent
env = environ.get

