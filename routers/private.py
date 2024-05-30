from aiogram.dispatcher.router import Router
from aiogram.filters import CommandStart
from aiogram.types import *

from time import strftime

router = Router(name='private')


@router.message(CommandStart())
async def message_start(message: Message):
    user = message.from_user
    await message.answer(f'Привет {user.full_name}!\nБудем делать пластинки 📀')
    print(strftime('%H:%M:%S'), user.username, 'started bot')
