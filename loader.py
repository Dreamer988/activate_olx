from aiogram import Bot, Dispatcher, types
from data import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)