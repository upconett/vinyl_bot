from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BIGINT

from .BaseModel import BaseModel 
from .Subscription import Subscription


class User(BaseModel):
    __tablename__ = 'users'

    telegram_id: Mapped[BIGINT] = mapped_column(BIGINT, nullable=False, unique=True)

    username: Mapped[str | None]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]

    subscription: Mapped[Subscription] = relationship(cascade='all, delete-orphan')

    def __init__(self, telegram_id: int, username: str = None, first_name: str = None, last_name: str = None):
        self.telegram_id = telegram_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, telegram_id={self.telegram_id!r}, username={self.username!r})"
    