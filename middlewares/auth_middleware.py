from pprint import pprint
from typing import Any, Awaitable, Callable, Coroutine, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message

from config import settings


class AuthMiddleware(BaseMiddleware):

    def __init__(self) -> None:
        self.access_id = settings.admin_id
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Coroutine[Any, Any, Any]:

        id = data["event_chat"].id
        if id != int(self.access_id):
            await event.message.answer(
                "Access Denied",
                # show_alert=True,
            )
            return
        return await handler(event, data)
