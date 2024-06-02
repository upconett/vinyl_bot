from multipledispatch import dispatch
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BIGINT
from aiogram.types import User as AIOgramUser

from .BaseModel import BaseModel 
from .Subscription import Subscription


class User(BaseModel):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(unique=True, primary_key=True)

    username: Mapped[str | None]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]

    subscription: Mapped[Subscription] = relationship(cascade='all, delete-orphan')


    def __init__(self, user: AIOgramUser):
        self.id = user.id
        self.username = user.username
        self.first_name = user.first_name
        self.last_name = user.last_name


    def update(self, user: AIOgramUser) -> None:
        """Обновление данных о пользователе"""
        self.username = user.username
        self.first_name = user.first_name
        self.last_name = user.last_name



    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"
    