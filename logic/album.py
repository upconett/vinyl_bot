from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import User as AIOgramUser

from database.base import async_engine
from database.models import User


async def use_free_albums(user: AIOgramUser) -> None:
    async with AsyncSession(async_engine) as s:
        u = await s.get(User, {'id': user.id})
        u.free_albums -= 1
        await s.commit()


async def check_sub_or_free_albums(user: AIOgramUser) -> bool:
    """Проверка есть ли у пользователя подписка или бесплатные альбомы"""
    async with AsyncSession(async_engine) as s:
        u = await s.get(User, {'id': user.id})
        return (u.subscription is not None or u.free_albums != 0)


async def check_sub(user: AIOgramUser) -> bool:
    async with AsyncSession(async_engine) as s:
        u = await s.get(User, {'id': user.id})
        return u.subscription is not None


async def check_free_albums(user: AIOgramUser) -> bool:
    async with AsyncSession(async_engine) as s:
        u = await s.get(User, {'id': user.id})
        return u.free_albums != 0