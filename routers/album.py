from aiogram.dispatcher.router import Router
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.types import *
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import json

from create_bot import logger, bot
from keyboards import album as keyboards
from keyboards import core as keyboards_core
from utility.template_images import get_image

from logic.core import *


router = Router(name='album')


class CreationStates(StatesGroup):
    wait_for_template = State()
    wait_for_photo = State()


@router.callback_query(F.data == 'create_album')
async def query_create_album(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    update_user(user)
    data = await state.get_data()

    image_id = get_image('templates_album')
    if image_id:
        photo_message = await query.message.answer_photo(photo=image_id)
    else:
        photo_message = await query.message.answer('Картинка шаблонов не выставлена!')
    data['photo_id'] = photo_message.message_id

    await query.message.delete()
    await query.message.answer(
        text='Выбери тип шаблона',
        reply_markup=keyboards.create_album_template()
    )

    await query.answer()

    await state.set_data(data)

    await state.set_state(CreationStates.wait_for_template)
    logger.info(f'@{user.username} decided to create album')


@router.callback_query(StateFilter(CreationStates.wait_for_template), F.data.startswith('create_album_template_'))
async def query_wait_for_template(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    update_user(user)
    data = await state.get_data()

    tmp = int(query.data.replace('create_album_template_', ''))

    data['template'] = tmp

    await query.message.edit_text(
        
    )



