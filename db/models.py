from sqlalchemy.orm import Mapped, mapped_column

from db.basemodel import Base


class Quote(Base):
    user_id: Mapped[int]
    author: Mapped[str]
    text: Mapped[str]
    folder: Mapped[str] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"user {self.user_id}, quote {self.id}, author {self.author}"
