from aiogram.dispatcher.router import Router
from aiogram import F
from aiogram.types import *

from create_bot import logger
from keyboards import subscription as keyboards

from logic.core import *


router = Router(name='subscription')


@router.callback_query(F.data == 'subscription')
async def query_subscription_rate(query: CallbackQuery):
    user = query.from_user
    update_user(user)
    await query.message.edit_text(
        text='Выберите тариф',
        reply_markup=keyboards.subscription_rate()
    )
    await query.answer()
    logger.info(f'@{user.username} called subscription')


@router.callback_query(F.data.startswith('subscription_rate'))
async def query_subscription_rate(query: CallbackQuery):
    user = query.from_user
    update_user(user)
    await query.message.edit_text(
        text='Выберите метод оплаты',
        reply_markup=keyboards.subscription_payment_method()
    )
    await query.answer()
    logger.info(f'@{user.username} called subscription_rate_*')


@router.callback_query(F.data.startswith('subscription_payment_method'))
async def query_subscription_rate(query: CallbackQuery):
    user = query.from_user
    update_user(user)
    await query.message.edit_text(
        text='Перейдите по ссылке чтобы оплатить',
        reply_markup=keyboards.subscription_payment()
    )
    await query.answer()
    logger.info(f'@{user.username} called subscription_payment_method_*')