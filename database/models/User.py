import enum
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from aiogram.types import User as AIOgramUser

from .BaseModel import BaseModel 
from .Subscription import Subscription


class LangTypes(enum.Enum):
    RU = 'ru'
    EN = 'en'


class User(BaseModel):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(unique=True, primary_key=True)

    username: Mapped[str | None]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]

    language: Mapped[LangTypes]

    free_vinyl: Mapped[int] = mapped_column(default=5)
    free_albums: Mapped[int] = mapped_column(default=1)

    subscription: Mapped[Subscription] = relationship(
        cascade='all, delete-orphan', lazy='selectin'
    )

    def __init__(self, user: AIOgramUser):
        super().__init__()
        self.id = user.id
        self.username = user.username
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.language = LangTypes.RU if user.language_code == 'ru' else LangTypes.EN


    async def update(self, user: AIOgramUser) -> None:
        """Обновление данных о пользователе"""
        self.username = user.username
        self.first_name = user.first_name
        self.last_name = user.last_name

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"
    