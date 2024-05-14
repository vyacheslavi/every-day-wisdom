from aiogram import Router, types, F
from aiogram.filters import Command

from db.crud import crud

router = Router()


@router.message(Command("show_quotes"))
async def cmd_show_quotes(message: types.Message):
    user_id = message.from_user.id
    quotes = crud.get_all_quotes(user_id=user_id)
    list_of_quotes = []
    if quotes:
        for quote in quotes:
            text_of_quote = quote.text[:50] + "..."
            string = (
                f"<b>{quote.author}</b>: \n <i>{text_of_quote}</i> /del{quote.id}\n\n"
            )
            list_of_quotes.append(string)
    else:
        await message.answer("У вас нет цитат")
    text = " ".join(list_of_quotes)
    await message.answer(text)


@router.message(F.text.startswith("/del"))
async def cmd_delete_quote(message: types.Message):
    quote_id = int(message.text[4:])
    user_id = message.from_user.id
    if crud.user_quote_owner(
        quote_id=quote_id,
        user_id=user_id,
    ):
        crud.delete_quote(quote_id=quote_id)
        await message.answer("Удалено")
    else:
        await message.answer("Некорректная команда")
