from datetime import datetime
from sqlalchemy.orm import Session
from aiogram.types import User as AIOgramUser
from yoomoney import Quickpay

from database.base import engine
from database.models import User, Subscription
from database.models.Subscription import SubType
from database.models.User import LangTypes

from database.dataclasses import ProfileData
from create_bot import yoomoney_info, yoomoney_client, bot_url


async def save_last_payment_label(user: AIOgramUser, label: str):
    with Session(engine) as s:
        u = s.get(User, {'id': user.id})
        u.last_payment_label = label
        s.commit()


async def get_payment_link_yoomoney(user: AIOgramUser, subscription_rate: int) -> str:
    """Генерирует ссылку для получения платежа в YooMoney"""
    text = 'Error'
    sum = 0

    match subscription_rate:
        case 1:
            text = '1 Month'
            sum = 2 # 399
        case 6:
            text = '6 Months'
            sum = 3 # 1915
        case 12:
            text = '12 Months'
            sum = 4 # 3830

    quickpay = Quickpay(
        receiver=yoomoney_info.account,
        quickpay_form='shop',
        targets=f'Vinyl Bot Subscription {text}',
        paymentType='SB',
        sum=sum,
        label=str(user.id),
        successURL=bot_url
    )

    return quickpay.redirected_url


async def get_payments_today(user: AIOgramUser):
    result = []
    history = yoomoney_client.operation_history(label=str(user.id))
    for op in history.operations:
        if (datetime.now() - op.datetime).days <= 1:
            result.append(op)
    return result


async def check_payment(user: AIOgramUser):
    for op in await get_payments_today(user):
        if op.status == 'success':
            return True
    return False


async def add_subscription(user: AIOgramUser, rate: int):
    if rate == 1: rate = SubType.MONTH_1
    if rate == 6: rate = SubType.MONTH_6
    if rate == 12: rate = SubType.MONTH_12
    with Session(engine) as s:
        u = s.get(User, {'id': user.id})
        u.subscription = Subscription(type=rate)
        s.commit()