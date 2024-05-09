from aiogram import Router, F
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from db.crud import crud
from db.schemas import QuoteSchema

router = Router()


class States(StatesGroup):
    input_author = State()
    input_quote = State()


@router.message(Command("start", "info"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Я могу добавлять цитаты в ваш список и присылать одну случайную из них каждый день"
    )


@router.message(Command("add_quote"))
async def start_of_the_adding_quote(message: types.Message, state: FSMContext):
    await state.set_state(States.input_author)
    await message.answer("Введите автора цитаты")


@router.message(F.text, States.input_author)
async def cmd_input_author(message: types.Message, state: FSMContext):
    await state.update_data(author=message.text)
    await state.set_state(States.input_quote)
    await message.answer("Введите текст цитаты, для отмены действия нажмите /cancel")


@router.message(Command("cancel"), States.input_quote)
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.set_state(None)
    await message.answer("Отмена действия")


@router.message(F.text, States.input_quote)
async def cmd_input_quote(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.update_data(user_id=message.from_user.id)
    quote_dict = await state.get_data()
    print(f"словарь из хэндлера {quote_dict}")
    quote = QuoteSchema(**quote_dict)
    crud.add_quote(quote)
    await message.answer("Цитата добавлена")
    await state.set_state(None)
