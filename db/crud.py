from sqlalchemy.orm import Session
from sqlalchemy import select

from db.schemas import QuoteSchema
from db.models import Quote
from db.database import get_session


def add_quote(quote_in: QuoteSchema):
    session = get_session()
    quote = Quote(**quote_in.model_dump())
    session.add(quote)
    session.commit()


def delete_quote(quote: QuoteSchema):
    session = get_session()
    quote = session.get
    session.delete(quote)
    session.commit()
