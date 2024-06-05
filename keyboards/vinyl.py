from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.models.User import LangTypes

async def create_vinyl(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU:
            text = 'Назад'
        case LangTypes.EN:
            text = 'Back'
    btn_back = InlineKeyboardButton(text=text, callback_data='start')
    return InlineKeyboardMarkup(
        inline_keyboard=[ [btn_back] ]
    )


async def create_vinyl_template(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU:
            text = 'Назад'
        case LangTypes.EN:
            text = 'Back'
    buttons_choice = [
        InlineKeyboardButton(
            text=f'{x}', 
            callback_data=f'create_vinyl_template_{x}'
        ) for x in range(1, 5)
    ]
    btn_back = InlineKeyboardButton(text=text, callback_data='start')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            buttons_choice,
            [btn_back]
        ]
    )


async def create_vinyl_noise(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU:
            texts = ['Да', 'Нет', 'Назад']
        case LangTypes.EN:
            texts = ['Yes', 'No', 'Back']
    btn_yes = InlineKeyboardButton(text=texts[0], callback_data='create_vinyl_noise_1')
    btn_no = InlineKeyboardButton(text=texts[1], callback_data='create_vinyl_noise_0')
    btn_back = InlineKeyboardButton(text=texts[2], callback_data='start')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [btn_yes, btn_no],
            [btn_back]
        ]
    )


async def create_vinyl_speed(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU:
            texts = ['Полный оборот', 'Назад']
        case LangTypes.EN:
            texts = ['Full turn', 'Back']
    btn_8rpm = InlineKeyboardButton(text='8RMP', callback_data='create_vinyl_speed_8RPM')
    btn_full = InlineKeyboardButton(text=texts[0], callback_data='create_vinyl_speed_full')
    btn_back = InlineKeyboardButton(text=texts[1], callback_data='start')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [btn_8rpm],
            [btn_full],
            [btn_back]
        ]
    )


async def create_vinyl_offset(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU:
            texts = ['С начала', 'Назад']
        case LangTypes.EN:
            texts = ['From the beginning', 'Back']
    btn_start = InlineKeyboardButton(text=texts[0], callback_data='create_vinyl_offset_start')
    btn_back = InlineKeyboardButton(text=texts[1], callback_data='start')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [btn_start],
            [btn_back]
        ]
    )


async def create_vinyl_approve(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU:
            texts = ['Создать', 'Отмена']
        case LangTypes.EN:
            texts = ['Create', 'Cancel']
    btn_yes = InlineKeyboardButton(text=texts[0], callback_data='create_vinyl_approve')
    btn_no = InlineKeyboardButton(text=texts[1], callback_data='start')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [btn_yes],
            [btn_no]
        ]
    )