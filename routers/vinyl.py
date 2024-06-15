from aiogram.dispatcher.router import Router
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.types import *
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import json, os

from create_bot import logger, bot
from messages import vinyl as messages
from messages import core as messages_core
from keyboards import vinyl as keyboards
from keyboards import core as keyboards_core
from utility.template_images import get_image

from creation.asyncio import make_classic_vinyl, make_video_vinyl, make_player_vinyl

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



@router.callback_query(F.data == 'create_vinyl')
async def query_create_vinyl(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    await update_user(user)
    lang = await get_language(user)

    if not await check_sub_or_free_vinyl(user):
        await query.answer(messages.no_free_vinyl(lang), show_alert=True)
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

    image_id = get_image('templates_vinyl')
    if image_id:
        photo_message = await message.answer_photo(photo=image_id)
    else:
        photo_message = await message.answer(messages_core.template_image_warning(lang))
    data['photo_id'] = photo_message.message_id

    await message.answer(
        text=messages.create_vinyl_template(lang),
        reply_markup=keyboards.create_vinyl_template(lang)
    )

    await bot.delete_message(user.id, data['query_message_id'])
     
    await state.set_data(data)

    await state.set_state(CreationStates.wait_for_template)
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

    await bot.delete_message(user.id, data['photo_id'])

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
        await message.answer(await messages.wrong_format(lang))
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
        if await check_free_vinyl(user):
            await use_free_vinyl(user)
        else:
            await query.answer(messages.no_free_vinyl(lang), show_alert=True)
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
        if data['cover_type'] == 1:
            video, circle = await make_classic_vinyl(user.id, cover_file, audio_file, data['template'], data['offset'], data['speed'], data['noise'])
        else:
            video, circle = await make_video_vinyl(user.id, cover_file, audio_file, data['template'], data['offset'], data['speed'], data['noise'])

        await state.set_data(data)

        await query.message.answer_video_note(
            video_note=BufferedInputFile(open(circle, 'rb').read(), filename='video_for_test')
        )
        await query.message.answer(
            text=messages.get_player(lang),
            reply_markup=keyboards.get_player(lang, video)
        )
    except:
        await query.message.answer(messages_core.error(lang))
        await state.clear()


@router.callback_query(F.data.startswith('get_player_'))
async def query_get_player(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    await update_user(user)
    lang = await get_language(user)
    data = await state.get_data()

    unique_id = query.data.replace('get_player_', '')
    video_path = fr'creation/video/{user.id}_{unique_id}_output_video.mp4'

    if not os.path.exists(video_path):
        await query.answer(messages.record_missing(lang), show_alert=True)
        await query.message.delete()
        return

    data['unique_id'] = unique_id

    await query.message.edit_text(
        text=messages.player_types,
        reply_markup=keyboards.player_types
    )
    await query.answer()

    await state.set_data(data)
    state.set_state(CreationStates.wait_for_player)


@router.callback_query(StateFilter(CreationStates.wait_for_player), F.data.startswith('player_template_'))
async def query_get_player_template(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    await update_user(user)
    lang = await get_language(user)
    data = await state.get_data()

    template = int(query.data.replace('player_template_', ''))
    unique_id = data['unique_id']

    try:
        video = await make_player_vinyl(user.id, unique_id, template)

        await query.message.answer_video(
            video=video,
            caption=messages.player_done(lang),
            reply_markup=keyboards_core.go_back(lang)
        )
        await state.clear()

    except Exception as e:
        print(e)
        await query.message.answer(messages_core.error(lang))
        return
