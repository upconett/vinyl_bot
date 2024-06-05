from sqlalchemy.orm import Session
from aiogram.types import User as AIOgramUser

from database.base import engine
from database.models import User


async def use_free_vinyl(user: AIOgramUser) -> None:
    with Session(engine) as s:
        u = s.get(User, {'id': user.id})
        u.free_vinyl -= 1
        s.commit()


async def check_sub_or_free_vinyl(user: AIOgramUser) -> bool:
    """Проверка есть ли у пользователя подписка или бесплатные пластинки"""
    with Session(engine) as s:
        u = s.get(User, {'id': user.id})
        return (u.subscription is not None or u.free_vinyl != 0)
