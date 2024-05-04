from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter, state
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from db.crud import add_quote
from db.schemas import QuoteSchema

quote_router = Router()


class States(StatesGroup):
    input_author = State()
    input_quote = State()


@quote_router.message(Command("add_quote"))
async def start_of_the_adding_quote(message: Message, state: FSMContext):
    await state.set_state(States.input_author)
    await message.answer("Введите автора цитаты")


@quote_router.message(F.text, States.input_author)
async def cmd_input_author(message: Message, state: FSMContext):
    await state.update_data(author=message.text)
    await state.set_state(States.input_quote)
    await message.answer("Введите текст цитаты")


@quote_router.message(F.text, States.input_quote)
async def cmd_input_quote(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.update_data(user_id=message.from_user.id)
    quote_dict = await state.get_data()
    print(f"словарь из хэндлера {quote_dict}")
    quote = QuoteSchema(**quote_dict)
    add_quote(quote)
    await message.answer("Цитата добавлена")
    await state.set_state(None)
