from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from aiogram.types import User as AIOgramUser

from database.base import async_engine
from database.models import User
from database.base import async_engine
from database.models import User
from database.models.User import LangTypes

from database.dataclasses import ProfileData


async def update_user(user: AIOgramUser) -> None:
async def update_user(user: AIOgramUser) -> None:
    """
    - Проверка есть ли пользователь в БД.
    - Добавление, если такого пользователя нет.
    - Обновление данных о пользователе.
    """
    async with AsyncSession(async_engine) as s:
        db_user = await s.get(User, {'id': user.id})
    async with AsyncSession(async_engine) as s:
        db_user = await s.get(User, {'id': user.id})
        
        if db_user is None: s.add(User(user))
        else:
            await db_user.update(user)
            if db_user.subscription:
                if db_user.subscription.expires_at < datetime.now():
                    await s.delete(db_user.subscription)

        await s.commit()
        if db_user is None: s.add(User(user))
        else:
            await db_user.update(user)
            if db_user.subscription:
                if db_user.subscription.expires_at < datetime.now():
                    await s.delete(db_user.subscription)

        await s.commit()


async def get_profile_data(user: AIOgramUser) -> ProfileData:
    async with AsyncSession(async_engine) as s:
        db_user = await s.get(User, {'id': user.id})
async def get_profile_data(user: AIOgramUser) -> ProfileData:
    async with AsyncSession(async_engine) as s:
        db_user = await s.get(User, {'id': user.id})
        return ProfileData(
            subscription=db_user.subscription,
            free_vinyl=db_user.free_vinyl,
            free_albums=db_user.free_albums
            free_vinyl=db_user.free_vinyl,
            free_albums=db_user.free_albums
        )
        

async def set_language(user: AIOgramUser, lang: str) -> LangTypes:
    async with AsyncSession(async_engine) as s:
        db_user = await s.get(User, {'id': user.id})
async def set_language(user: AIOgramUser, lang: str) -> LangTypes:
    async with AsyncSession(async_engine) as s:
        db_user = await s.get(User, {'id': user.id})
        if lang == 'ru':
            db_user.language = LangTypes.RU
            lang = LangTypes.RU
            lang = LangTypes.RU
        elif lang == 'en':
            db_user.language = LangTypes.EN
            lang = LangTypes.EN
        await s.commit()
        return lang
            lang = LangTypes.EN
        await s.commit()
        return lang


async def get_language(user: AIOgramUser) -> LangTypes:
    async with AsyncSession(async_engine) as s:
        return (await s.get(User, {'id': user.id})).language
async def get_language(user: AIOgramUser) -> LangTypes:
    async with AsyncSession(async_engine) as s:
        return (await s.get(User, {'id': user.id})).language
        