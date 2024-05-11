from sqlalchemy.orm import Session
from sqlalchemy import delete, func, select

from db.schemas import QuoteSchema
from db.models import Quote
from db.database import get_session


class CRUDQuotes:

    def __init__(self, session: Session) -> None:
        """Intialisation of class CRUDQuotes

        Args:
            session (Session): session
        """
        self.session: Session = session

    def user_quote_owner(self, quote_id: int, user_id: int) -> bool:
        """Check if user is owner of quote

        Args:
            quote_id (int): quote id
            user_id (int): user id

        Returns:
            bool:
        """
        stmt = select(Quote).where((Quote.user_id == user_id) & (Quote.id == quote_id))
        quote: Quote | None = self.session.scalar(stmt)
        if quote:
            return True
        return False

    def add_quote(self, quote_in: QuoteSchema) -> None:
        """Adds quote in database

        Args:
            quote_in (QuoteSchema): a quote to be added to the database
        """
        quote = Quote(**quote_in.model_dump())
        self.session.add(quote)
        self.session.commit()

    def delete_quote(self, quote_id: int) -> None:
        """Delete quote from database

        Args:
            quote_id (int): id of quote to be deleted from database
        """
        self.session = get_session()
        stmt = delete(Quote).where(Quote.id == quote_id)
        self.session.execute(stmt)
        self.session.commit()

    def get_all_quotes(self, user_id: int) -> list[Quote]:
        """Returns all quotes of specific user

        Args:
            user_id (int): user id

        Returns:
            list[Quote]: all quotes from user
        """
        stmt = select(Quote).where(Quote.user_id == user_id)

        return self.session.scalars(stmt)

    def get_random_quote(self, user_id: int) -> Quote:
        """Returns a random quote from specific user

        Args:
            user_id (int): user id

        Returns:
            Quote: random quote of specific user
        """
        self.session = get_session()
        stmt = select(Quote).where(Quote.user_id == user_id).order_by(func.random())

        return self.session.scalar(stmt)


crud = CRUDQuotes(session=get_session())
