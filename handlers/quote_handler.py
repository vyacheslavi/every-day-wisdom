from aiogram import Router
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from db.crud import crud
from db.models import Quote


class States(StatesGroup):
    state_executing = State()


router = Router()


async def send_quote(message: types.Message):
    user_id = message.from_user.id
    quote: Quote = crud.get_random_quote(user_id=user_id)
    text = f"Автор цитаты  - <b>{quote.author}</b>,\n\n <i>{quote.text}</i>"

    await message.answer(text)


@router.message(Command("day"), State(None))
async def cmd_get_quote(
    message: types.Message,
    apscheduler: AsyncIOScheduler,
    state: FSMContext,
):
    apscheduler.add_job(
        func=send_quote,
        trigger="cron",
        hour=5,
        kwargs={"message": message},
    )
    apscheduler.start()
    await state.set_state(States.state_executing)
    await message.answer("Теперь каждый день вы будете получать случайную цитату")


@router.message(Command("stop"), States.state_executing)
async def cmd_stop(
    message: types.Message,
    apscheduler: AsyncIOScheduler,
    state: FSMContext,
):
    apscheduler.shutdown()
    await message.answer("Вы приостановили рассылку цитат")
    await state.set_state(None)


@router.message(Command("send_quote"))
async def cmd_send_quote(message: types.Message):
    await send_quote(message=message)
