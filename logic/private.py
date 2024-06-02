from sqlalchemy.orm import Session
from aiogram.types import User as AIOgramUser

from database.base import engine
from database.models import User, Subscription


def update_user(user: AIOgramUser) -> None:
    """
    - Проверка есть ли пользователь в БД.
    - Добавление, если такого пользователя нет.
    - Обновление данных о пользователе.
    """
    with Session(engine) as s:
        db_user = s.get(User, {'id': user.id})
        
        if db_user == None: s.add(User(user))
        else: db_user.update(user)

        s.commit()
