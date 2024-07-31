import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import settings
from handlers import (
    send_quote_router,
    add_quote_router,
    delete_quote_router,
)
from middlewares import (
    ApschedulerMiddleware,
    ThrottlingMiddleware,
)


async def main():
    bot = Bot(
        token=settings.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

    dp.update.middleware(ApschedulerMiddleware(scheduler=scheduler))
    dp.update.middleware(ThrottlingMiddleware())

    dp.include_routers(
        send_quote_router,
        add_quote_router,
        delete_quote_router,
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        print("Bot stopped")
