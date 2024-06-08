import asyncio

from aiogram.dispatcher.router import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.types import *

import messages.subscription
from create_bot import logger
from messages import subscription as messages
from messages import core as messages_core
from keyboards import subscription as keyboards
from keyboards import core as keyboards_core

from logic.core import *
from logic.subscription import get_payment_link_yoomoney, check_payment, add_subscription
from logic.vinyl import *


router = Router(name='subscription')


class SubscriptionStates(StatesGroup):
    buying = State()


@router.callback_query(F.data == 'subscription')
async def query_subscription_rate(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    await update_user(user)
    lang = await get_language(user)

    if await check_sub(user):
        await query.answer(messages.subscription_already(lang))
        logger.info(f'@{user.username} is already subscribed')
        return


    await query.message.edit_text(
        text=messages.subscription_rate(lang),
        reply_markup=keyboards.subscription_rate(lang)
    )
    await query.answer()
    await state.set_state(SubscriptionStates.buying)
    logger.info(f'@{user.username} called subscription')


@router.callback_query(StateFilter(SubscriptionStates.buying), F.data.startswith('subscription_rate_'))
async def query_subscription_payment_method(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    await update_user(user)
    lang = await get_language(user)
    data = await state.get_data()
    rate = int(query.data.replace('subscription_rate_', ''))
    data['rate'] = rate

    await query.message.edit_text(
        text=messages.subscription_payment_method(lang),
        reply_markup=keyboards.subscription_payment_method(lang)
    )
    await state.set_data(data)
    await query.answer()
    logger.info(f'@{user.username} called subscription_rate_*')


@router.callback_query(StateFilter(SubscriptionStates.buying), F.data.startswith('subscription_payment_method'))
async def query_subscription_payment(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    await update_user(user)
    lang = await get_language(user)
    data = await state.get_data()
    rate = data['rate']
    method = query.data.replace('subscription_payment_method_', '')

    payment_link = ''
    if method == 'yoomoney':
        payment_link = await get_payment_link_yoomoney(user, rate)
        await query.message.edit_text(
            text=messages.subscription_payment(lang),
            reply_markup=keyboards.subscription_payment(lang, payment_link)
        )
        await query.answer()
    else:
        await query.answer('No PayPal payment for now...', show_alert=True)

    logger.info(f'@{user.username} called subscription_payment_method_*')


@router.callback_query(StateFilter(SubscriptionStates.buying), F.data == 'subscription_check')
async def query_subscription_check(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    await update_user(user)
    lang = await get_language(user)
    data = await state.get_data()

    rate = data['rate']

    pd = await get_profile_data(user)

    if await check_payment(user):
        await add_subscription(user, rate)
        await asyncio.sleep(.2)
        await query.message.edit_text(
            text=messages_core.profile(lang, pd),
            reply_markup=keyboards_core.profile(lang)
        )
        await query.answer(messages.payment_success(lang))
        logger.info(f'@{user.username} paid for subscription for {rate} months')
    else:
        await query.answer(messages.payment_fault(lang))
        logger.info(f'@{user.username} didn\'t pay yet')
