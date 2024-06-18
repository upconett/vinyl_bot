from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


from database.models.User import LangTypes


def start(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU:
            texts = [ 'Создать альбом', 'Создать пластинку', 'Профиль', 'Статистика']
        case LangTypes.EN:
            texts = ['Create album', 'Create vinyl', 'Profile', 'Статистика']
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=texts[0], callback_data='create_album')
    keyboard.button(text=texts[1], callback_data='create_vinyl')
    keyboard.button(text=texts[2], callback_data='profile') 
    keyboard.button(text=texts[3], callback_data='stats')
    keyboard.adjust(1, repeat=True)
    return keyboard.as_markup()


def announcement(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU: texts = ['Отправить', 'Отмена']
        case LangTypes.EN: texts = ['Send', 'Cancel']
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=texts[0], callback_data='announce')
    keyboard.button(text=texts[1], callback_data='start')
    keyboard.adjust(1, repeat=True)
    return keyboard.as_markup()


def go_back(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU: text = 'Назад'
        case LangTypes.EN: text = 'Back'
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=text, callback_data='start')
    return keyboard.as_markup()
