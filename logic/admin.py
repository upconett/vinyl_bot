from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from aiogram.types import User as AIOgramUser

from database.base import async_engine
from database.models import User
from database.models import Subscription, SubType
from database.models.User import LangTypes

from database.dataclasses import ProfileData


async def get_stats_data() -> dict:
    async with AsyncSession(async_engine) as s:
        users = (await s.execute(select(User))).all()
        subs = (await s.execute(select(Subscription))).all()
    users_total = 0
    users_today = 0
    users_active = 0
    users_blocked = 0

    sub_today_month = 0
    sub_today_6month = 0
    sub_today_12month = 0

    sub_month = 0
    sub_6month = 0
    sub_12month = 0
    for u in users:
        if u[0].created_at.date() == datetime.now().date():
            users_today += 1
        if u[0].active: users_active += 1
        else: users_blocked += 1
        users_total += 1
    for s in subs:
        if s[0].created_at.date() == datetime.now().date():
            match s[0].type:
                case SubType.MONTH_1: sub_today_month+=1
                case SubType.MONTH_6: sub_today_6month+=1
                case SubType.MONTH_12: sub_today_12month+=1
        match s[0].type:
            case SubType.MONTH_1:
                sub_month += 1
            case SubType.MONTH_6:
                sub_6month += 1
            case SubType.MONTH_12:
                sub_12month += 1
    return {
        'users_total': users_total,
        'users_today': users_today,
        'users_active': users_active,
        'users_blocked': users_blocked,
        'sub_today_month': sub_today_month,
        'sub_today_6month': sub_today_6month,
        'sub_today_12month': sub_today_12month,
        'sub_month': sub_month,
        'sub_6month': sub_6month,
        'sub_12month': sub_12month
    }
        

async def get_all_users() -> list:
    async with AsyncSession(async_engine) as s:
        return (await s.execute(select(User).where(User.active))).all()


async def set_blocked(user: User) -> None:
    async with AsyncSession(async_engine) as s:
        u = await s.get(User, {'id': user.id})
        if u.active: u.active = False
        await s.commit()
