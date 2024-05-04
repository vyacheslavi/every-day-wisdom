from pydantic import BaseModel


class UserShema(BaseModel):
    id: int


class QuoteSchema(BaseModel):
    user_id: int
    text: str
    author: str
    folder: str = None
