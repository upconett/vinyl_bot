from aiogram.dispatcher.router import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import F
from aiogram.types import *

import messages.subscription
from create_bot import logger, bot
from messages import subscription as messages
from keyboards import subscription as keyboards
from keyboards import core as keyboards_core

from logic.subscription import add_subscription
from logic.core import *
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
        await query.answer(messages.subscription_already(lang), show_alert=True)
        logger.info(f'@{user.username} is already subscribed')
        return

    message_to_edit = await query.message.edit_text(
        text=messages.subscription_rate(lang),
        reply_markup=await keyboards.subscription_rate(lang)
    )
    await state.set_data({'message_to_edit': message_to_edit.message_id})
    logger.info(f'@{user.username} called subscription')
    await state.set_state(SubscriptionStates.buying)


@router.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery):

    # {
    # "id": "790986186977243107",
    # "from_user": {...},
    # "currency": "XTR",
    # "total_amount": 1,
    # "invoice_payload": "subscription_for_1_months",
    # "shipping_option_id": null,
    # "order_info": null
    # }

    user = pre_checkout_query.from_user
    rate = int(pre_checkout_query.invoice_payload.split('_')[2])

    try:
        await add_subscription(user, rate)
        await pre_checkout_query.answer(ok=True)
    except Exception as e:
        await pre_checkout_query.answer(ok=False, error_message=e)


@router.message(F.successful_payment)
async def successful_payment(message: Message, state: FSMContext):
    user = message.from_user
    await update_user(user)
    lang = await get_language(user)
    
    try:
        data = await state.get_data()
        message_to_edit = data['message_to_edit']
        await bot.edit_message_text(
            chat_id=user.id, 
            message_id=message_to_edit, 
            text=messages.successful_payment(lang),
            reply_markup=keyboards_core.go_back_profile(lang)
        )
    except:
        await message.answer(
            text=messages.successful_payment(lang),
            reply_markup=keyboards_core.go_back_profile(lang)
        )
