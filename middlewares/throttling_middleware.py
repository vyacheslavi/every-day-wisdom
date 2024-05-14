from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from db.redis_tools import redis


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
            return await event.message.answer("Не больше 1 запроса в 2 секунд")
        else:
            await redis.set(name=user, value=1, ex=5)
            return await handler(event, data)
