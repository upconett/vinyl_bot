from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import User as AIOgramUser

from database.base import async_engine
from database.models import User, Subscription
from database.models.Subscription import SubType


async def add_subscription(user: AIOgramUser, rate: int):
    if rate == 1: rate = SubType.MONTH_1
    elif rate == 6: rate = SubType.MONTH_6
    elif rate == 12: rate = SubType.MONTH_12
    async with AsyncSession(async_engine) as s:
        u = await s.get(User, {'id': user.id})
        u.subscription = Subscription(type = rate)
        await s.commit()
