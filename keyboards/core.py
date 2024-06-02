from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def start() -> InlineKeyboardMarkup:
    btn_create_album = InlineKeyboardButton(text='Создать альбом', callback_data='create_album')
    btn_create_vinyl = InlineKeyboardButton(text='Создать пластинку', callback_data='create_vinyl')
    btn_profile = InlineKeyboardButton(text='Профиль', callback_data='profile')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [btn_create_album],
            [btn_create_vinyl],
            [btn_profile]
        ]
    )


def profile() -> InlineKeyboardMarkup:
    btn_language = InlineKeyboardButton(text='Язык', callback_data='language')
    btn_subscription = InlineKeyboardButton(text='Оформить подписку', callback_data='subscription')
    btn_back = InlineKeyboardButton(text='Назад', callback_data='start')
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


