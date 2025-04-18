from aiogram.dispatcher.router import Router
from aiogram import F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import *

from create_bot import logger, bot
from messages import core as messages
from create_bot import logger, bot
from messages import core as messages
from keyboards import core as keyboards

from logic.core import *


router = Router(name='core')


@router.message(CommandStart())
async def message_start(message: Message, state: FSMContext):
    user = message.from_user
    await update_user(user)
    lang = await get_language(user)

    data = await state.get_data()
    await update_user(user)
    lang = await get_language(user)

    data = await state.get_data()

    await message.answer(
        text=messages.start(lang, user),
        reply_markup=keyboards.start(lang)
    )

    for key in data.keys():
        try: 
            if 'id' in key: 
                try: await bot.delete_message(user.id, data[key])
                except: await bot.delete_messages(user.id, data[key])
        except: pass
    await state.set_data({})
    await state.clear()
 
        text=messages.start(lang, user),
        reply_markup=keyboards.start(lang)
    )

    for key in data.keys():
        try: 
            if 'id' in key: 
                try: await bot.delete_message(user.id, data[key])
                except: await bot.delete_messages(user.id, data[key])
        except: pass
    await state.set_data({})
    await state.clear()
 
    logger.info(f'@{user.username} started bot')


@router.callback_query(F.data == 'start')
async def query_start(query: CallbackQuery, state: FSMContext):
async def query_start(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    await update_user(user)
    lang = await get_language(user)
    data = await state.get_data()

    await query.message.answer(
        text=messages.start(lang, user),
        reply_markup=keyboards.start(lang)
    )

    for key in data.keys():
        try:
            if 'id' in key:
                try: await bot.delete_message(user.id, data[key])
                except: await bot.delete_messages(user.id, data[key])
        except: pass

    try:
        await query.message.delete()
    except:
        pass

    await state.set_data({})
    await state.clear()

    logger.info(f'@{user.username} called start')


@router.callback_query(F.data == 'profile')
async def query_profile(query: CallbackQuery):
    user = query.from_user
    await update_user(user)
    lang = await get_language(user)
    await update_user(user)
    lang = await get_language(user)

    pd = await get_profile_data(user)
    pd = await get_profile_data(user)
    await query.message.edit_text(
        text=messages.profile(lang, pd),
        reply_markup=keyboards.profile(lang)
    )
    await query.answer()
    logger.info(f'@{user.username} called profile')


@router.callback_query(F.data == 'profile_new')
async def query_profile(query: CallbackQuery):
    user = query.from_user
    await update_user(user)
    lang = await get_language(user)

    pd = await get_profile_data(user)

    await query.message.edit_reply_markup(
        reply_markup=None
    )

    await query.message.answer(
        text=messages.profile(lang, pd),
        reply_markup=keyboards.profile(lang)
        text=messages.profile(lang, pd),
        reply_markup=keyboards.profile(lang)
    )
    await query.answer()
    logger.info(f'@{user.username} called profile')


@router.callback_query(F.data == 'profile_new')
async def query_profile(query: CallbackQuery):
    user = query.from_user
    await update_user(user)
    lang = await get_language(user)

    pd = await get_profile_data(user)

    await query.message.edit_reply_markup(
        reply_markup=None
    )

    await query.message.answer(
        text=messages.profile(lang, pd),
        reply_markup=keyboards.profile(lang)
    )
    await query.answer()
    logger.info(f'@{user.username} called profile')
    
    

@router.callback_query(F.data == 'language')
async def query_language(query: CallbackQuery):
    user = query.from_user
    await update_user(user)
    lang = await get_language(user)
    await update_user(user)
    lang = await get_language(user)

    await query.message.edit_text(
        text=messages.language(lang),
        text=messages.language(lang),
        reply_markup=keyboards.language()
    )
    await query.answer()
    logger.info(f'@{user.username} called language')


@router.callback_query(F.data.startswith('language_'))
async def query_language_set(query: CallbackQuery):
    user = query.from_user
    await update_user(user)

    lang = await set_language(user, query.data.replace('language_', ''))
    await update_user(user)

    lang = await set_language(user, query.data.replace('language_', ''))
    if lang == LangTypes.RU: answer_text = "Язык установлен 🇷🇺"
    else: answer_text = "Language set 🇺🇸"

    pd = await get_profile_data(user)
    pd = await get_profile_data(user)
    await query.message.edit_text(
        text=messages.profile(lang, pd),
        reply_markup=keyboards.profile(lang)
        text=messages.profile(lang, pd),
        reply_markup=keyboards.profile(lang)
    )

    await query.answer(answer_text)
    logger.info(f'@{user.username} set language to "{lang.value.upper()}"')

