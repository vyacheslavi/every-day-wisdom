import types
from typing import Any, Awaitable, Callable, Coroutine, Dict
from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import TelegramObject


class ThrottlingMiddleware(BaseMiddleware):

    def __init__(self) -> None:
        super().__init__()

    async def on_process_message(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        """TODO Реализовать с помощью Redis"""
