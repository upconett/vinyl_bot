from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from aiogram.types import User as AIOgramUser

from database.base import async_engine
from database.models import User
from database.models.User import LangTypes

from database.dataclasses import ProfileData


async def get_stats_data() -> dict:
    async with AsyncSession(async_engine) as s:
        users = (await s.execute(select(User))).all()
    users_total = 0
    users_today = 0
    users_active = 0
    users_blocked = 0
    for u in users:
        if u[0].created_at.date() == datetime.now().date():
            users_today += 1
        if u[0].active: users_active += 1
        else: users_blocked += 1
        users_total += 1
    return {
        'users_total': users_total,
        'users_today': users_today,
        'users_active': users_active,
        'users_blocked': users_blocked
    }
        

async def get_all_users() -> list:
    async with AsyncSession(async_engine) as s:
        return (await s.execute(select(User).where(User.active))).all()


async def set_blocked(user: User) -> None:
    async with AsyncSession(async_engine) as s:
        u = await s.get(User, {'id': user.id})
        if u.active: u.active = False
        await s.commit()
