import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from Config import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

loop = asyncio.get_event_loop()
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
