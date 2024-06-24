from aiogram.dispatcher.router import Router
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.types import *
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import json, os

from create_bot import logger, bot, cm
from messages import vinyl as messages
from messages import core as messages_core
from keyboards import vinyl as keyboards
from keyboards import core as keyboards_core
from utility.template_images import get_image
from creation.CreationManager import Vinyl, Player, VinylTypes

from creation.asyncio import get_unique_id, make_classic_vinyl, make_video_vinyl, make_player_vinyl

from logic.core import *
from logic.vinyl import *


router = Router(name='vinyl')

class CreationStates(StatesGroup):
    wait_for_audio = State()
    wait_for_template = State()
    wait_for_cover = State()
    wait_for_noise = State()
    wait_for_speed = State()
    wait_for_offset = State()
    wait_for_approve = State()
    wait_for_player = State()

    album = State()


@router.callback_query(F.data == 'create_vinyl')
async def query_create_vinyl(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    await update_user(user)
    lang = await get_language(user)

    if not await check_sub_or_free_vinyl(user):
        await query.answer(messages.no_free_vinyl(lang), show_alert=True)
        return
        
    if cm.in_vinyl_queue(user.id):
        await query.answer(messages.vinyl_query_block(lang), show_alert=True)
        return

    await state.set_state(CreationStates.wait_for_audio)

    query_message = await query.message.edit_text(
        text=messages.create_vinyl(lang),
        reply_markup=keyboards.create_vinyl(lang)
    )

    data = await state.get_data()
    data['query_message_id'] = query_message.message_id
    await state.set_data(data)

    await query.answer()
    logger.info(f'@{user.username} called create_vinyl')


@router.message(StateFilter(CreationStates.wait_for_audio))
async def message_wait_for_audio(message: Message, state: FSMContext):
    try:
        if not any([message.audio, message.voice]):
            return
        user = message.from_user
        await update_user(user)
        lang = await get_language(user)
        data = await state.get_data()

        file = None
        if message.audio: file = message.audio
        elif message.voice: file = message.voice
        if file.duration < 3:
            await message.answer(messages.audio_fail(lang))
            return

        data['audio_file_id'] = file.file_id
        data['duration'] = file.duration
        images = get_image('templates_vinyl')
        if images:
            photo_messages = await message.answer_media_group(media=[
                InputMediaPhoto(media=x) for x in images
            ])
        else:
            photo_messages = [await message.answer(messages_core.template_image_warning(lang))]
        data['photo_ids'] = [x.message_id for x in photo_messages]

        await message.answer(
            text=messages.create_vinyl_template(lang),
            reply_markup=keyboards.create_vinyl_template(lang)
        )

        await bot.delete_message(user.id, data['query_message_id'])
        
        await state.set_data(data)

        await state.set_state(CreationStates.wait_for_template)
    except Exception as e:
        print(e)
    logger.info(f'@{user.username} sent audio for vinyl, saved {file.file_id}.mp3')


@router.callback_query(StateFilter(CreationStates.wait_for_template), F.data.startswith('create_vinyl_template_'))
async def query_wait_for_template(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    await update_user(user)
    lang = await get_language(user)
    data = await state.get_data()

    # Получаем номер шаблона из callback_query.data
    tmp = int(query.data.replace('create_vinyl_template_', ''))
    data['template'] = tmp

    query_message = await query.message.edit_text(
        text=messages.create_vinyl_cover(lang, tmp),
        reply_markup=keyboards.create_vinyl(lang)
    )
    data['query_message_id'] = query_message.message_id
    await query.answer()

    await bot.delete_messages(user.id, data['photo_ids'])

    await state.set_data(data)

    await state.set_state(CreationStates.wait_for_cover)
    logger.info(f'@{user.username} choose template №{tmp} for vinyl')
       

@router.message(StateFilter(CreationStates.wait_for_cover))
async def message_wait_for_cover(message: Message, state: FSMContext):
    if not any([message.photo, message.video, message.document]): return
    user = message.from_user
    await update_user(user)
    lang = await get_language(user)
    data = await state.get_data()

    if message.document: 
        await message.answer(messages.cover_failure(lang))
        logger.info(f'@{user.username} sent document and got rejected')
        return

    cover_type = ''

    if message.photo: 
        file_id = message.photo[-1].file_id
        cover_type = 1
    elif message.video:
        if message.video.file_size > 1_048_576 * 10: # 10MB
            print(message.video.file_size)
            await message.answer(messages.too_big_video(lang))
            return
        file_id = message.video.file_id
        cover_type = 2

    data['cover_file_id'] = file_id
    data['cover_type'] = cover_type

    await message.answer(
        text=messages.create_vinyl_noise(lang, cover_type),
        reply_markup=keyboards.create_vinyl_noise(lang)
    )

    await bot.delete_message(user.id, data['query_message_id'])

    cover_type = 'photo' if cover_type == 1 else 'video'

    await state.set_data(data)

    await state.set_state(CreationStates.wait_for_noise)
    logger.info(f'@{user.username} sent {cover_type} cover for vinyl, saved {file_id}{".jpeg" if cover_type == "photo" else ".mp4"}')


@router.callback_query(StateFilter(CreationStates.wait_for_noise), F.data.startswith('create_vinyl_noise_'))
async def query_wait_for_noise(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    await update_user(user)
    lang = await get_language(user)
    data = await state.get_data()

    # Получаем bool значение шума из callback_query.data
    noise = bool(int(query.data.replace('create_vinyl_noise_', '')))

    data['noise'] = noise

    await query.message.edit_text(
        text=messages.create_vinyl_speed(lang, noise),
        reply_markup=keyboards.create_vinyl_speed(lang)
    )

    await query.answer()

    await state.set_data(data)
    await state.set_state(CreationStates.wait_for_speed)
    logger.info(f'@{user.username} choose {"not " if not noise else ""}to add noise')


@router.callback_query(StateFilter(CreationStates.wait_for_speed), F.data.startswith('create_vinyl_speed_'))
async def query_wait_for_speed(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    await update_user(user)
    lang = await get_language(user)
    data = await state.get_data()

    speed = int(query.data.replace('create_vinyl_speed_', ''))

    data['speed'] = speed

    query_message = await query.message.edit_text(
        text=messages.create_vinyl_offset(lang, speed),
        reply_markup=keyboards.create_vinyl_offset(lang)
    )
    data['query_message_id'] = query_message.message_id

    await query.answer()

    await state.set_data(data)
    await state.set_state(CreationStates.wait_for_offset)
    logger.info(f'@{user.username} choose speed: {speed}')


@router.callback_query(StateFilter(CreationStates.wait_for_offset), F.data.startswith('create_vinyl_offset_'))
async def query_wait_for_approve(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    await update_user(user)
    lang = await get_language(user)
    data = await state.get_data()

    data['offset'] = '00:00'

    await query.message.edit_text(
        text=messages.create_vinyl_approve(lang, data),
        reply_markup=keyboards.create_vinyl_approve(lang)
    )

    await state.set_data(data)
    await state.set_state(CreationStates.wait_for_approve)
    logger.info(f'@{user.username} chose offset 00:00')


@router.message(StateFilter(CreationStates.wait_for_offset), F.text)
async def message_wait_for_approve(message: Message, state: FSMContext):
    user = message.from_user
    await update_user(user)
    lang = await get_language(user)
    data = await state.get_data()

    if len(message.text) == 5 and message.text[2] == ':' and \
            message.text.count(':') == 1 and all(x.isdigit() for x in message.text.replace(':', '')):
        offset = message.text
    else:
        await message.answer(messages.wrong_format(lang))
        return

    minutes, seconds = map(int, offset.split(':'))
    duration = minutes * 60 + seconds
    if not duration<=data['duration']:
        await message.answer(messages.error_start_time(lang))
        return
    data['offset'] = offset

    await message.answer(
        text=messages.create_vinyl_approve(lang, data),
        reply_markup=keyboards.create_vinyl_approve(lang)
    )

    await bot.delete_message(user.id, data['query_message_id'])

    await state.set_data(data)
    await state.set_state(CreationStates.wait_for_approve)
    logger.info(f'@{user.username} chose offset {offset}')


@router.callback_query(StateFilter(CreationStates.wait_for_approve), F.data == 'create_vinyl_approve')
async def query_end(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    await update_user(user)
    lang = await get_language(user)
    data = await state.get_data()

    if not await check_sub(user):
        if not await check_free_vinyl(user):
            await query.answer(messages.no_free_vinyl(lang), show_alert=True)
            return

    if cm.in_vinyl_queue(user.id):
        await query.answer(messages.vinyl_query_block(lang), show_alert=True)
        return

    await query.message.edit_text(
        text=messages.creation_end(lang, 20, 0),
        reply_markup=keyboards_core.go_back(lang)
        # TODO ------------- ADD seconds counter, queue counter
    )

    await state.clear()
    logger.info(f'@{user.username} started vinyl creation')

    audio_id = data['audio_file_id']
    cover_id = data['cover_file_id']

    audio_file = f'creation/audio/{user.id}_{audio_id}.mp3'
    if data['cover_type'] == 1: cover_file = f'creation/img/{user.id}_{cover_id}.jpeg'
    else: cover_file = f'creation/users_video/{user.id}_{cover_id}.mp4'

    await bot.download(audio_id, f'{audio_file}')
    await bot.download(cover_id, f'{cover_file}')

    print('Started creation')

    try:
        await use_free_vinyl(user)
        unique_id = get_unique_id()
        type = VinylTypes.PHOTO if data['cover_type'] == 1 else VinylTypes.VIDEO
        video, circle = await cm.createVinyl(Vinyl(user.id, unique_id, data['template'], type, audio_file, cover_file, data['offset'], data['speed'], data['noise']))

        await query.message.answer_video_note(
            video_note=BufferedInputFile(open(circle, 'rb').read(), filename='vinyl for you')
        )
        os.remove(circle)
        await query.message.answer(
            text=messages.get_player(lang),
            reply_markup=keyboards.get_player(lang, unique_id)
        )
    except Exception as e:
        print(e)
        await add_free_vinyl(user)
        if 'VOICE_MESSAGES_FORBIDDEN' in e:
            await query.message.answer(messages_core.voice_forbidden(lang))
        else:
            await query.message.answer(messages_core.error(lang))
        await state.clear()


@router.callback_query(F.data.startswith('get_player_'))
async def query_get_player(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    await update_user(user)
    lang = await get_language(user)

    unique_id = query.data.replace('get_player_', '')
    video_path = fr'creation/video/{unique_id}_output_video.mp4'

    if not os.path.exists(video_path):
        await query.answer(messages.record_missing(lang), show_alert=True)
        await query.message.delete()
        return

    if cm.in_player_queue(user.id):
        await query.answer(messages.player_query_block(lang), show_alert=True)
        return

    await query.message.delete()

    try:
        photo_ids = await query.message.answer_media_group(
            media=[InputMediaPhoto(media=x) for x in get_image('templates_player')],
        )
        await query.message.answer(
            text=messages.player_types(lang),
            reply_markup=keyboards.player_types(unique_id)
        )
    except:
        await query.message.answer(
            text=messages.player_types(lang),
            reply_markup=keyboards.player_types(unique_id)
        )
    await query.answer()

    await state.set_data({'photo_ids': [x.message_id for x in photo_ids]})
    await state.set_state(CreationStates.album)


@router.callback_query(F.data.startswith('player_template_'))
async def query_get_player_template(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    await update_user(user)
    lang = await get_language(user)

    if state:
        data = await state.get_data()

    unique_id, template = map(int, query.data.replace('player_template_', '').split('_'))
    if cm.in_player_queue(user.id):
        await query.answer(messages.player_query_block(lang), show_alert=True)
        return

    try:
        await query.message.edit_caption(
            caption=messages.player_get_ready(lang),
            reply_markup=keyboards_core.go_back(lang)
        )
    except:
        await query.message.edit_text(
            text=messages.player_get_ready(lang),
            reply_markup=keyboards_core.go_back(lang)
        )

    await bot.delete_messages(user.id, data['photo_ids'])

    await state.clear()
    # match template:
    #     case 1:
    #         width = 1080
    #         height = 1920
    #     case 2:
    #         width = 1080
    #         height = 1920
    #     case 3:
    #         width = 2276
    #         height = 1518
    try:
        video_path = await cm.createPlayer(Player(user.id, unique_id, template))

        # await query.message.answer_video(
        #     video=BufferedInputFile(open(video_path, 'rb').read(), filename='player for you'),
        #     caption=messages.player_done(lang), reply_markup=keyboards_core.go_back(lang),
        #     width=width, height=height, supports_streaming=True
        # )
        await query.message.answer_document(document=BufferedInputFile(open(video_path, 'rb').read(), filename='player for you.mp4'), filename='player for you.mp4', disable_content_type_detection=True)
        await query.message.answer(messages.back_or_player(lang), reply_markup=keyboards.go_back_or_make(lang, unique_id))
    except Exception as e:
        print(e)
        if 'VOICE_MESSAGES_FORBIDDEN' in e:
            await query.message.answer(messages_core.voice_forbidden(lang))
        else:
            await query.message.answer(messages_core.error(lang))
