from aiogram.dispatcher.router import Router
from aiogram.filters import CommandStart
from aiogram.types import *

from create_bot import logger

router = Router(name='private')


@router.message(CommandStart())
async def message_start(message: Message):
    user = message.from_user
    await message.answer(f'Привет {user.full_name}!\nБудем делать пластинки 📀')
    logger.info(f'@{user.username} started bot')
