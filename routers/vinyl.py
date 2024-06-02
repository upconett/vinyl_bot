from aiogram.dispatcher.router import Router
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.types import *
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from create_bot import logger, bot
from keyboards import vinyl as keyboards

from logic.core import *


router = Router(name='vinyl')

class CreationStates(StatesGroup):
    wait_for_audio = State()
    wait_for_template = State()



@router.callback_query(F.data == 'create_vinyl')
async def query_create_vinyl(query: CallbackQuery, state: FSMContext):
    user = query.from_user
    update_user(user)

    await state.set_state(CreationStates.wait_for_audio)

    query_message = await query.message.edit_text(
        text='Пришли мне аудио',
        reply_markup=keyboards.create_vinyl()
    )

    data = await state.get_data()
    data['query_message_id'] = query_message.message_id
    await state.set_data(data)

    await query.answer()
    logger.info(f'@{user.username} called create_vinyl')


@router.message(StateFilter(CreationStates.wait_for_audio))
async def message_wait_for_audio(message: Message, state: FSMContext):
    user = message.from_user
    update_user(user)
    data = await state.get_data()

    if message.audio: file_id = message.audio.file_id
    if message.voice: file_id = message.voice.file_id
    await bot.download(file=file_id, destination=f'./audio/{file_id}.mp3')
    data['audio_file'] = ('./audio/' + file_id + '.mp3')


    await bot.delete_message(user.id, data['query_message_id'])

    # photo_message = await message.answer_photo(
    #     photo=''
    # )
    # data['photo_id'] = photo_message.message_id

    await message.answer(
        text="Супер! Теперь выбери шаблон пластинки",
        reply_markup=keyboards.create_vinyl_template()
    )
     
    await state.set_data(data)

    state.set_state(CreationStates.wait_for_template)
    logger.info(f'@{user.username} sent auido for vinyl, saved "{file_id}.mp3"')
