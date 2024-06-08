from aiogram.dispatcher.router import Router
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.types import *
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import json

from create_bot import logger, bot
from messages import vinyl as messages
from messages import core as messages_core
from keyboards import vinyl as keyboards
from keyboards import core as keyboards_core
from utility.template_images import get_image

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



@router.callback_query(F.data == 'create_vinyl')
async def query_create_vinyl(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    await update_user(user)
    lang = await get_language(user)

    if not await check_sub_or_free_vinyl(user):
        await query.answer(messages.no_free_vinyl(lang))
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
    file_id = file.file_id
    await bot.download(file=file_id, destination=f'./audio/{file_id}.mp3')
    data['audio_file'] = ('./audio/' + file_id + '.mp3')

    await bot.delete_message(user.id, data['query_message_id'])

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
     
    await state.set_data(data)

    await state.set_state(CreationStates.wait_for_template)
    logger.info(f'@{user.username} sent audio for vinyl, saved {file_id}.mp3')


@router.callback_query(StateFilter(CreationStates.wait_for_template), F.data.startswith('create_vinyl_template_'))
async def query_wait_for_template(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    await update_user(user)
    lang = await get_language(user)
    data = await state.get_data()

    await bot.delete_message(user.id, data['photo_id'])

    # Получаем номер шаблона из callback_query.data
    tmp = int(query.data.replace('create_vinyl_template_', ''))
    data['template'] = tmp

    query_message = await query.message.edit_text(
        text=messages.create_vinyl_cover(lang, tmp),
        reply_markup=keyboards.create_vinyl(lang)
    )
    data['query_message_id'] = query_message.message_id
    await query.answer()

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
        await bot.download(file=file_id, destination=f'./cover/{file_id}.jpeg')
        data['cover_file'] = ('./cover/' + file_id + '.jpeg')
        cover_type = 1
    elif message.video:
        file_id = message.video.file_id
        await bot.download(file=file_id, destination=f'./cover/{file_id}.mp4')
        data['cover_file'] = ('./cover/' + file_id + '.mp4')
        cover_type = 2

    await bot.delete_message(user.id, data['query_message_id'])

    await message.answer(
        text=messages.create_vinyl_noise(lang, cover_type),
        reply_markup=keyboards.create_vinyl_noise(lang)
    )

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

    speed = query.data.replace('create_vinyl_speed_', '')

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
        await message.answer(await message.wrong_format(lang))
        return

    data['offset'] = offset

    await bot.delete_message(user.id, data['query_message_id'])

    await message.answer(
        text=messages.create_vinyl_approve(lang, data),
        reply_markup=keyboards.create_vinyl_approve(lang)
    )

    await state.set_state(CreationStates.wait_for_approve)
    logger.info(f'@{user.username} chose offset {offset}')


@router.callback_query(StateFilter(CreationStates.wait_for_approve))
async def query_end(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    await update_user(user)
    lang = await get_language(user)
    data = await state.get_data()

    if not await check_sub(user):
        if await check_free_vinyl(user):
            await use_free_vinyl(user)
        else:
            await query.answer(messages.no_free_vinyl(lang))
            return

    await query.message.edit_text(
        text=f'Пластинка будет готова через {20} сек\nПеред вами в очереди {0} человек'
        # TODO ------------- ADD seconds counter, queue counter
    )
    await query.message.answer(
        text=(
            f'```json\n{json.dumps(data, indent=4, ensure_ascii=False)}\n```'
        ),
        parse_mode='MarkdownV2'
    )
    await query.message.answer(
        text=messages_core.start(lang, user),
        reply_markup=keyboards_core.start(lang)
    )

    await state.clear()
    logger.info(f'@{user.username} started vinyl creation')