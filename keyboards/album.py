from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def create_album_template() -> InlineKeyboardMarkup:
    buttons_choice = [
        InlineKeyboardButton(
            text=f'{x}',
            callback_data=f'create_album_template_{x}'
        ) for x in range(1, 5)
    ]
    btn_back = InlineKeyboardButton(text='Назад', callback_data='start')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            buttons_choice,
            [btn_back]
        ]
    )