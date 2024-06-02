from aiogram.dispatcher.router import Router
from aiogram import F
from aiogram.filters import CommandStart
from aiogram.types import *

from create_bot import logger
from keyboards import private as keyboards

from logic.private import *


router = Router(name='private')


@router.message(CommandStart())
async def message_start(message: Message):
    user = message.from_user
    update_user(user)

    await message.answer(
        text=(f'Привет, {user.first_name}\n'
        'В этом боте ты можешь создать '
        'визуализацию музыки в виде кружка с '
        'пластинкой или вставить свое изображение в альбом!'
        ),
        reply_markup=keyboards.start()
    )
    logger.info(f'@{user.username} started bot')


@router.callback_query(F.data == 'start')
async def query_start(query: CallbackQuery):
    user = query.from_user
    update_user(user)
    await query.message.edit_text(
        text=(f'Привет, {user.first_name}\n'
        'В этом боте ты можешь создать '
        'визуализацию музыки в виде кружка с '
        'пластинкой или вставить свое изображение в альбом!'
        ),
        reply_markup=keyboards.start()
    )
    logger.info(f'@{user.username} called start')


@router.callback_query(F.data == 'profile')
async def query_subscription_rate(query: CallbackQuery):
    user = query.from_user
    update_user(user)
    await query.message.edit_text(
        text='Ваш профиль',
        reply_markup=keyboards.profile()
    )
    await query.answer()
    logger.info(f'@{user.username} called profile')


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
