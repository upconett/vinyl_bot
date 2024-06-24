import os

from aiogram.dispatcher.router import Router
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.types import *
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import json

from create_bot import logger, bot, cm
from creation.CreationManager import Album
from messages import album as messages
from messages import core as messages_core
from keyboards import album as keyboards
from keyboards import core as keyboards_core
from utility.template_images import get_image

from logic.core import *
from logic.album import *
from creation.asyncio import get_unique_id


router = Router(name='album')


class CreationStates(StatesGroup):
    wait_for_template = State()
    wait_for_single_photo = State()
    wait_for_first_photo = State()
    wait_for_second_photo = State()
    wait_for_approve = State()


@router.callback_query(F.data == 'create_album')
async def query_create_album(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    await update_user(user)
    lang = await get_language(user)
    data = await state.get_data()
    if not await check_sub_or_free_albums(user):
        await query.answer(messages.no_free_albums(lang), show_alert=True)
        return

    if cm.in_album_queue(user.id):
        await query.answer(messages.album_query_block(lang), show_alert=True)
        return

    images = get_image('templates_album')
    if images:
        photo_messages = await query.message.answer_media_group(media=[InputMediaPhoto(media=x) for x in images])
    else:
        photo_messages = [await query.message.answer(messages_core.template_image_warning(lang))]
    data['photo_ids'] = [x.message_id for x in photo_messages]

    await query.message.delete()
    await query.message.answer(
        text=messages.create_album_template(lang),
        reply_markup=keyboards.create_album_template(lang)
    )

    await query.answer()

    await state.set_data(data)

    await state.set_state(CreationStates.wait_for_template)
    logger.info(f'@{user.username} decided to create album')


@router.callback_query(StateFilter(CreationStates.wait_for_template), F.data.startswith('create_album_template_'))
async def query_wait_for_template(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    await update_user(user)
    lang = await get_language(user)
    data = await state.get_data()
    tmp = int(query.data.replace('create_album_template_', ''))

    data['template'] = tmp

    if tmp == 1:
        text = messages.wait_single_photo(lang)
        st = CreationStates.wait_for_single_photo
    else:
        text = messages.wait_first_photo(lang)
        st = CreationStates.wait_for_first_photo
    
    last_message = await query.message.edit_text(
        text=text,
        reply_markup=keyboards_core.go_back(lang)
    )

    data['last_message_id'] = last_message.message_id

    await state.set_data(data)

    await bot.delete_messages(user.id, data['photo_ids'])
    await state.set_state(st)
    logger.info(f'@{user.username} chose album template {tmp}')


@router.message(StateFilter(CreationStates.wait_for_first_photo), F.document)
async def message_wait_for_first_photo(message: Message, state: FSMContext):
    user = message.from_user
    await update_user(user)
    lang = await get_language(user)
    data = await state.get_data()

    if not (message.document and 'image' in message.document.mime_type) or message.document.file_size>=10000000:
        await message.answer(
            text=messages.wrong_photo_format(lang)
        )       
        return

    file_id = message.document.file_id
    data['photos'] = [file_id]

    last_message = await message.answer(
        text=messages.wait_second_photo(lang),
        reply_markup=keyboards_core.go_back(lang)
    )
    
    await bot.delete_message(user.id, data['last_message_id'])

    data['last_message_id'] = last_message.message_id

    await state.set_data(data)
    await state.set_state(CreationStates.wait_for_second_photo)
    logger.info(f'@{user.username} sent first photo, id = {file_id}')


@router.message(StateFilter(CreationStates.wait_for_single_photo, CreationStates.wait_for_second_photo), F.document)
async def message_wait_for_singe_or_second_photo(message: Message, state: FSMContext):
    user = message.from_user
    await update_user(user)
    lang = await get_language(user)
    data = await state.get_data()

    if not (message.document and 'image' in message.document.mime_type) or message.document.file_size>=10000000:
        await message.answer(
            text=messages.wrong_photo_format(lang)
        )       
        return

    file_id = message.document.file_id
    if 'photos' in data.keys():
        data['photos'].append(file_id)
    else:
        data['photos'] = [file_id]

    last_message = await message.answer(
        text=messages.create_album_approve(lang, data),
        reply_markup=keyboards.create_album_approve(lang)
    )

    await bot.delete_message(user.id, data['last_message_id'])

    data['last_message_id'] = last_message.message_id

    await state.set_data(data)
    await state.set_state(CreationStates.wait_for_approve)
    logger.info(f'@{user.username} sent second or single photo, id = {file_id}')


@router.message(StateFilter(CreationStates.wait_for_single_photo, CreationStates.wait_for_first_photo, CreationStates.wait_for_second_photo))
async def message_wrong_photo_format(message: Message, state: FSMContext):
    user = message.from_user
    await update_user(user)
    lang = await get_language(user)

    await message.answer(
        text=messages.wrong_photo_format(lang)
    )
    await message.delete()
    logger.info(f'@{user.username} sent wrong format creating album')


@router.callback_query(StateFilter(CreationStates.wait_for_approve), F.data == 'create_album_approve')
async def query_wait_for_approve(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    await update_user(user)
    lang = await get_language(user)
    data = await state.get_data()

    if not await check_sub(user):
        if await check_free_albums(user):
            await use_free_albums(user)
        else:
            await query.answer(messages.no_free_albums(lang), show_alert=True)
            return

    if cm.in_album_queue(user.id):
        await query.answer(messages.album_query_block(lang), show_alert=True)
        return

    await query.message.edit_text(
        text=messages.creation_end(lang, 20, 0),
        reply_markup=keyboards_core.go_back(lang)
    )

    photos = data['photos']

    files = [f'creation/img/{user.id}_{x}.jpeg' for x in photos]

    print('Album creation started')

    await bot.download(photos[0], files[0])

    if len(photos) > 1:
        await bot.download(photos[1], files[1])
    
    if len(files) == 1: files.append(None) 
    try:
        await use_free_albums(user)
        unique_id = get_unique_id()
        alb_file = await cm.createAlbum(Album(user.id, unique_id, data['template'], files[0], files[1]))
        print(alb_file)
        # await query.message.answer_photo(
        #     photo=BufferedInputFile(file=open(alb_file, 'rb').read(), filename='album for you'),
        #     caption=messages.album_ready(lang), reply_markup=keyboards_core.go_back(lang)
        # )
        await query.message.answer_document(BufferedInputFile(file=open(alb_file, 'rb').read(), filename='album for you.png'),
                                            reply_markup=keyboards_core.go_back(lang), disable_content_type_detection=True)
        print(alb_file)
        os.remove((alb_file))
    except Exception as e:
        print(e)
        await add_free_albums(user)
        if 'VOICE_MESSAGES_FORBIDDEN' in e.__str__():
            await query.message.answer(messages_core.voice_forbidden(lang))
        else:
            await query.message.answer(messages_core.error(lang))

    logger.info(f'@{user.username} started album creation')
