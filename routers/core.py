from aiogram.dispatcher.router import Router
from aiogram import F
from aiogram.filters import CommandStart
from aiogram.types import *

from create_bot import logger
from keyboards import core as keyboards

from logic.core import *


router = Router(name='core')


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
async def query_profile(query: CallbackQuery):
    user = query.from_user
    update_user(user)

    pd = get_profile_data(user)
    await query.message.edit_text(
        text=(
            'Профиль\n' +
            f'Подписка {"✅" if pd.subscribed else "❌"}\n' +
            (f"Истекает: {pd.expires_at}\n" if pd.subscribed else "") + 
            '\n' +
            f'Бесплатных пластинок: {pd.free_vinyl}\n' +
            f'Бесплатных альбомов: {pd.free_albums}\n'
        ),
        reply_markup=keyboards.profile()
    )
    await query.answer()
    logger.info(f'@{user.username} called profile')


@router.callback_query(F.data == 'language')
async def query_language(query: CallbackQuery):
    user = query.from_user
    update_user(user)

    await query.message.edit_text(
        text='Выберите язык',
        reply_markup=keyboards.language()
    )
    await query.answer()
    logger.info(f'@{user.username} called language')


@router.callback_query(F.data.startswith('language_'))
async def query_language_set(query: CallbackQuery):
    user = query.from_user
    update_user(user)

    
    lang = set_language(user, query.data.replace('language_', ''))

    pd = get_profile_data(user)
    await query.message.edit_text(
        text=(
            'Профиль\n' +
            f'Подписка {"✅" if pd.subscribed else "❌"}\n' +
            (f"Истекает: {pd.expires_at}\n" if pd.subscribed else "") + 
            '\n' +
            f'Бесплатных пластинок: {pd.free_vinyl}\n' +
            f'Бесплатных альбомов: {pd.free_albums}\n'
        ),
        reply_markup=keyboards.profile()
    )

    await query.answer()
    logger.info(f'@{user.username} set language to "{lang.value.upper()}"')
    