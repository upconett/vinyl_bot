from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.models.User import LangTypes


async def create_album_template(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU: text = 'Назад'
        case LangTypes.EN: text = 'Back'
    buttons_choice = [
        InlineKeyboardButton(
            text=f'{x}',
            callback_data=f'create_album_template_{x}'
        ) for x in range(1, 5)
    ]
    btn_back = InlineKeyboardButton(text=text, callback_data='start')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            buttons_choice,
            [btn_back]
        ]
    )


async def create_album_approve(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU:
            texts = ['Создать', 'Отмена']
        case LangTypes.EN:
            texts = ['Create', 'Cancel']
    btn_yes = InlineKeyboardButton(text=texts[0], callback_data='create_album_approve')
    btn_no = InlineKeyboardButton(text=texts[1], callback_data='start')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [btn_yes],
            [btn_no]
        ]
    )
