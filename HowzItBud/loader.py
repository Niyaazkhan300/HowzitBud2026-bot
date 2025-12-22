from utils.db.storage import DatabaseManager
from aiogram import Bot, Dispatcher, types
from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# Use relative path, storage.py will move it to ~/.howzitbud/data/database.db
db = DatabaseManager("data/database.db")
