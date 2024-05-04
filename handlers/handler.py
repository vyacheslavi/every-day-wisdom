from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from db.crud import add_quote, user_exist

router = Router()


@router.message(Command("start", "info"))
async def cmd_start(message: Message):
    await message.answer("Привет")


@router.message(Command("id"))
async def cmd_id(message: Message):
    id = message.from_user.id
    await message.answer(str(id))
