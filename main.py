import asyncio
from aiogram import Bot, Dispatcher

from config import config
from handler import router


async def main():
    print(config.bot_token.get_secret_value())
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
