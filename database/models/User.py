import enum
from datetime import datetime
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
    active: Mapped[bool] = mapped_column(default=True)
    active: Mapped[bool] = mapped_column(default=True)

    free_vinyl: Mapped[int] = mapped_column(default=1)
    free_albums: Mapped[int] = mapped_column(default=1)

    subscription: Mapped[Subscription] = relationship(
        cascade='all, delete-orphan', lazy='selectin'
    )
    subscription: Mapped[Subscription] = relationship(
        cascade='all, delete-orphan', lazy='selectin'
    )

    def __init__(self, user: AIOgramUser):
        super().__init__()
        super().__init__()
        self.id = user.id
        self.username = user.username
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.language = LangTypes.RU if user.language_code in ['ru', 'uk', 'be'] else LangTypes.EN
        self.language = LangTypes.RU if user.language_code in ['ru', 'uk', 'be'] else LangTypes.EN

    async def update(self, user: AIOgramUser) -> None:
    async def update(self, user: AIOgramUser) -> None:
        """Обновление данных о пользователе"""
        self.username = user.username
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.active = True
        self.active = True

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"
    