from aiogram.dispatcher.router import Router
from aiogram import F
from aiogram.types import *

from create_bot import logger
from utility.filters import AllowedUsers
from utility.template_images import change_image

from logic.core import *

 
router = Router(name='admin')
router.message(AllowedUsers())


@router.message(F.caption == '/add_image_vinyl', F.photo, AllowedUsers())
async def message_add_image_templates_vinyl(message: Message):
    user = message.from_user
    file_id = message.photo[-1].file_id

    change_image('templates_vinyl', file_id)

    await message.answer(
        text='Изменена картинка шаблонов пластинок ✅'
    )

    logger.info(f'@{user.username} admin_id [{user.id}] changed vinyl template image')


@router.message(F.caption == '/add_image_album', F.photo, AllowedUsers())
async def message_add_image_templates_album(message: Message):
    user = message.from_user
    file_id = message.photo[-1].file_id

    change_image('templates_album', file_id)

    await message.answer(
        text='Изменена картинка шаблонов альбомов ✅'
    )

    logger.info(f'@{user.username} admin_id [{user.id}] changed albums template image')
