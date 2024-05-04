import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher

from config import config
from db.database import create_db, delete_db
from handlers.adding_quote_handler import quote_router
from middlewares import AuthMiddleware, ApschedulerMiddleware, ThrottlingMiddleware


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    dp.update.outer_middleware(AuthMiddleware())
    dp.update.middleware(ApschedulerMiddleware())
    dp.update.middleware(ThrottlingMiddleware())
    dp.include_router(quote_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        print("Bot stopped")

# delete_db()
# create_db()
