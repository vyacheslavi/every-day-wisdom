from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.dispatcher.flags import get_flag

from db.redis_tools import redis
from config import settings

WARNING_MSG = "Допустимо 1 сообщение в 1 секунду"


class ThrottlingMiddleware(BaseMiddleware):

    def __init__(self) -> None:
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        user = f"user{event.message.from_user.id}"

        result = await redis.get(user)

        if result:
            return await event.message.answer(WARNING_MSG)
        else:
            await redis.set(name=user, value=1, ex=settings.anti_spam_seconds)
            return await handler(event, data)
