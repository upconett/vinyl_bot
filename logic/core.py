from sqlalchemy.orm import Session
from aiogram.types import User as AIOgramUser

from database.base import engine
from database.models import User, Subscription
from database.models.Subscription import SubType
from database.models.User import LangTypes

from database.dataclasses import ProfileData


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


def get_profile_data(user: AIOgramUser) -> ProfileData:
    with Session(engine) as s:
        db_user = s.get(User, {'id': user.id})
        return ProfileData(
            subscription=db_user.subscription,
            free_vinyl=db_user.free_vinyl,                           # TODO -----------------------
            free_albums=db_user.free_albums
        )
        

def set_language(user: AIOgramUser, lang: str) -> LangTypes:
    with Session(engine) as s:
        db_user = s.get(User, {'id': user.id})
        if lang == 'ru':
            db_user.language = LangTypes.RU
        elif lang == 'en':
            db_user.language = LangTypes.EN
        s.commit()
        return db_user.language


async def get_language(user: AIOgramUser) -> LangTypes:
    with Session(engine) as s:
        return s.get(User, {'id': user.id}).language
        