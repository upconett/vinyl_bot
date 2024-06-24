from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


from database.models.User import LangTypes


def start(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU: texts = ['Создать альбом', 'Создать пластинку', 'Профиль']
        case LangTypes.EN: texts = ['Create album', 'Create vinyl', 'Profile']
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=texts[0], callback_data='create_album')
    keyboard.button(text=texts[1], callback_data='create_vinyl')
    keyboard.button(text=texts[2], callback_data='profile')
    keyboard.adjust(1, repeat=True)
    return keyboard.as_markup()


def profile(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU: texts = ['Язык', 'Оформить подписку', 'Назад']
        case LangTypes.EN: texts = ['Language', 'Subscribe', 'Back']
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=texts[0], callback_data='language')
    keyboard.button(text=texts[1], callback_data='subscription')
    keyboard.button(text=texts[2], callback_data='start')
    keyboard.adjust(1, repeat=True)
    return keyboard.as_markup()


def language() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Русский 🇷🇺', callback_data='language_ru')
    keyboard.button(text='English 🇺🇸', callback_data='language_en')
    keyboard.adjust(1, repeat=True)
    return keyboard.as_markup()


def go_back(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU:
            text = 'Вернуться'
        case LangTypes.EN:
            text = 'Go back'
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=text, callback_data='start')
    return keyboard.as_markup()


def go_back_profile(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU:
            text = 'Вернуться'
        case LangTypes.EN:
            text = 'Go back'
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=text, callback_data='profile_new')
    return keyboard.as_markup()
