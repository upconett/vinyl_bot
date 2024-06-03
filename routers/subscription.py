from aiogram.dispatcher.router import Router
from aiogram import F
from aiogram.types import *

import messages.subscription
from create_bot import logger
from messages import subscription as messages
from keyboards import subscription as keyboards

from logic.core import *


router = Router(name='subscription')


@router.callback_query(F.data == 'subscription')
async def query_subscription_rate(query: CallbackQuery):
    user = query.from_user
    update_user(user)
    lang = await get_language(user)
    await query.message.edit_text(
        text=await messages.subscription_rate(lang),
        reply_markup=await keyboards.subscription_rate(lang)
    )
    await query.answer()
    logger.info(f'@{user.username} called subscription')


@router.callback_query(F.data.startswith('subscription_rate'))
async def query_subscription_payment_method(query: CallbackQuery):
    user = query.from_user
    update_user(user)
    lang = await get_language(user)
    await query.message.edit_text(
        text=await messages.subscription_payment_method(lang),
        reply_markup=await keyboards.subscription_payment_method(lang)
    )
    await query.answer()
    logger.info(f'@{user.username} called subscription_rate_*')


@router.callback_query(F.data.startswith('subscription_payment_method'))
async def query_subscription_payment(query: CallbackQuery):
    user = query.from_user
    update_user(user)
    lang = await get_language(user)
    await query.message.edit_text(
        text=await messages.subscription_payment(lang),
        reply_markup=await keyboards.subscription_payment(lang, user)
    )
    await query.answer()
    logger.info(f'@{user.username} called subscription_payment_method_*')