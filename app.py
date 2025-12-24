import os
import logging
import asyncio

# Fix for Python 3.11/3.12 event loop issue
asyncio.set_event_loop(asyncio.new_event_loop())

from aiogram import executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from data import config
from loader import dp, db, bot
import filters

# Setup filters
filters.setup(dp)

WEBAPP_HOST = "0.0.0.0"  # Host for webhook
WEBAPP_PORT = int(os.environ.get("PORT", 5000))  # Port for webhook
user_message = 'Customer Mode'
admin_message = 'Admin Mode'


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(user_message, admin_message)

    await message.answer(
        '''Welcome to HowzItBud2026 👋

🤖 I’m your store bot for browsing and buying products.

🛍️ To view the catalog and pick items you like, use the command /menu.

💰 You can top up your balance via supported payment methods.

❓ Got questions? Use /sos to contact the admins — we’ll respond as quickly as possible.

🤝 Want a similar bot for your own business? Contact the developer <a href="https://t.me/NikolaySimakov">Nikolay Simakov</a>.
        ''',
        reply_markup=markup
    )


@dp.message_handler(text=user_message)
async def user_mode(message: types.Message):
    cid = message.chat.id
    if cid in config.ADMINS:
        config.ADMINS.remove(cid)
    await message.answer('Customer mode enabled.', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(text=admin_message)
async def admin_mode(message: types.Message):
    cid = message.chat.id
    if cid not in config.ADMINS:
        config.ADMINS.append(cid)
    await message.answer('Admin mode enabled.', reply_markup=ReplyKeyboardRemove())


async def on_startup(dp):
    logging.basicConfig(level=logging.INFO)
    db.create_tables()
    await bot.delete_webhook()
    if config.WEBHOOK_URL:
        await bot.set_webhook(config.WEBHOOK_URL)


async def on_shutdown(dp):
    logging.warning("Shutting down..")
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning("Bot down")


if __name__ == '__main__':
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=config.WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT
    )
