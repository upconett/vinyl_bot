from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


from database.models.User import LangTypes


def start(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU: texts = ['Создать альбом', 'Создать пластинку', 'Профиль']
        case LangTypes.EN: texts = ['Create album', 'Create vinyl', 'Profile']
    btn_create_album = InlineKeyboardButton(text=texts[0], callback_data='create_album')
    btn_create_vinyl = InlineKeyboardButton(text=texts[1], callback_data='create_vinyl')
    btn_profile = InlineKeyboardButton(text=texts[2], callback_data='profile')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [btn_create_album],
            [btn_create_vinyl],
            [btn_profile]
        ]
    )


def profile(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU: texts = ['Язык', 'Оформить подписку', 'Назад']
        case LangTypes.EN: texts = ['Language', 'Subscribe', 'Back']
    btn_language = InlineKeyboardButton(text=texts[0], callback_data='language')
    btn_subscription = InlineKeyboardButton(text=texts[1], callback_data='subscription')
    btn_back = InlineKeyboardButton(text=texts[2], callback_data='start')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [btn_language],
            [btn_subscription],
            [btn_back]
        ]
    )


def language() -> InlineKeyboardMarkup:
    btn_language_russian = InlineKeyboardButton(text='Русский 🇷🇺', callback_data='language_ru')
    btn_language_english = InlineKeyboardButton(text='English 🇺🇸', callback_data='language_en')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [btn_language_russian],
            [btn_language_english],
        ]
    )



def go_back(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU:
            text = 'Вернуться'
        case LangTypes.EN:
            text = 'Go back'
    btn_back = InlineKeyboardButton(text=text, callback_data='start')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [btn_back]
        ]
    )


def go_back_profile(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU:
            text = 'Вернуться'
        case LangTypes.EN:
            text = 'Go back'
    btn_back = InlineKeyboardButton(text=text, callback_data='profile_new')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [btn_back]
        ]
    )