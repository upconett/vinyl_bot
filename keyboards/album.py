from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.models.User import LangTypes


def create_album_template(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU: text = 'Назад'
        case LangTypes.EN: text = 'Back'
    keyboard = InlineKeyboardBuilder()
    for x in range(1, 5):
        keyboard.button(
            text=f'{x}',
            callback_data=f'create_album_template_{x}'
        )
    keyboard.button(text=text, callback_data='start')
    keyboard.adjust(4, 1)
    return keyboard.as_markup()


def create_album_approve(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU: texts = ['Создать', 'Отмена']
        case LangTypes.EN: texts = ['Create', 'Cancel']
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=texts[0], callback_data='create_album_approve')
    keyboard.button(text=texts[1], callback_data='start')
    keyboard.adjust(1, repeat=True)
    return keyboard.as_markup()
