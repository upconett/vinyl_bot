from aiogram.dispatcher.router import Router
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.types import *
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import json

from create_bot import logger, bot
from messages import album as messages
from messages import core as messages_core
from keyboards import album as keyboards
from keyboards import core as keyboards_core
from utility.template_images import get_image

from logic.core import *


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

    image_id = get_image('templates_album')
    if image_id:
        photo_message = await query.message.answer_photo(photo=image_id)
    else:
        photo_message = await query.message.answer(messages_core)
    data['photo_id'] = photo_message.message_id

    await query.message.delete()
    await query.message.answer(
        text='Выбери тип шаблона',
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
    data = await state.get_data()

    tmp = int(query.data.replace('create_album_template_', ''))

    data['template'] = tmp

    if tmp == 1:
        text = 'Пришли мне фото которое будет на альбоме\n'
        st = CreationStates.wait_for_single_photo
    else:
        text = 'Пришли мне фото для левой страницы\n'
        st = CreationStates.wait_for_first_photo
    
    last_message = await query.message.edit_text(
        text=text+'Учти, что фото желательно скидывать разрешения X на Y иначе может получиться некрасиво',
        reply_markup=None
    )

    data['last_message_id'] = last_message.message_id

    await state.set_data(data)

    await bot.delete_message(user.id, data['photo_id'])
    await state.set_state(st)
    logger.info(f'@{user.username} chose album template {tmp}')


@router.message(StateFilter(CreationStates.wait_for_first_photo), F.photo)
async def message_wait_for_first_photo(message: Message, state: FSMContext):
    user = message.from_user
    await update_user(user)
    lang = await get_language(user)
    data = await state.get_data()

    file_id = message.photo[-1].file_id
    data['photos'] = [file_id]

    last_message = await message.answer(
        text='Теперь пришли мне фото для правой страницы\nУчти, что фото желательно скидывать разрешения X на Y иначе может получиться некрасиво'
    )
    
    await bot.delete_message(user.id, data['last_message_id'])

    data['last_message_id'] = last_message.message_id

    await state.set_data(data)
    await state.set_state(CreationStates.wait_for_second_photo)
    logger.info(f'@{user.username} sent first photo, id = {file_id}')


@router.message(StateFilter(CreationStates.wait_for_single_photo, CreationStates.wait_for_second_photo), F.photo)
async def message_wait_for_singe_or_second_photo(message: Message, state: FSMContext):
    user = message.from_user
    await update_user(user)
    lang = await get_language(user)
    data = await state.get_data()

    file_id = message.photo[-1].file_id
    if data['photos']:
        data['photos'].append(file_id)
    else:
        data['photos'] = [file_id]

    tmp = data['template']

    last_message = await message.answer(
        # photo=tmp_photo...                                                      <--------------------------------------- TODO
        text=f'Выбран шаблон: {tmp}\n\nСоздать альбом с этими настройками?',
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
        text='Пожалуйста, пришлите сжатое фото\nИли введите /start, чтобы отменить создание альбома'
    )
    await message.delete()
    logger.info(f'@{user.username} sent wrong format creating album')


@router.callback_query(StateFilter(CreationStates.wait_for_approve), F.data == 'create_album_approve')
async def query_wait_for_approve(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    await update_user(user)
    lang = await get_language(user)
    data = await state.get_data()

    await query.message.edit_text(
        text='Супер, подожди N сек и твой альбом будет готов\nПеред вами в очереди X человек',
        reply_markup=None
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
    logger.info(f'@{user.username} started album creation')
