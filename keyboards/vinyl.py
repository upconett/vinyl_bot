from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_vinyl() -> InlineKeyboardMarkup:
    btn_back = InlineKeyboardButton(text='Назад', callback_data='start')
    return InlineKeyboardMarkup(
        inline_keyboard=[ [btn_back] ]
    )


def create_vinyl_template() -> InlineKeyboardMarkup:
    buttons_choice = [
        InlineKeyboardButton(
            text=f'{x}', 
            callback_data=f'create_vinyl_template_{x}'
        ) for x in range(1, 5)
    ]
    btn_back = InlineKeyboardButton(text='Назад', callback_data='start')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            buttons_choice,
            [btn_back]
        ]
    )


def create_vinyl_noise() -> InlineKeyboardMarkup:
    btn_yes = InlineKeyboardButton(text='Да', callback_data='create_vinyl_noise_1')
    btn_no = InlineKeyboardButton(text='Нет', callback_data='create_vinyl_noise_0')
    btn_back = InlineKeyboardButton(text='Назад', callback_data='start')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [btn_yes, btn_no],
            [btn_back]
        ]
    )


def create_vinyl_speed() -> InlineKeyboardMarkup:
    btn_8rpm = InlineKeyboardButton(text='8RMP', callback_data='create_vinyl_speed_8RPM')
    btn_full = InlineKeyboardButton(text='1 Оборот', callback_data='create_vinyl_speed_full')
    btn_back = InlineKeyboardButton(text='Назад', callback_data='start')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [btn_8rpm],
            [btn_full],
            [btn_back]
        ]
    )


def create_vinyl_offset() -> InlineKeyboardMarkup:
    btn_start = InlineKeyboardButton(text='С самого начала', callback_data='create_vinyl_offset_start')
    btn_back = InlineKeyboardButton(text='Назад', callback_data='start')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [btn_start],
            [btn_back]
        ]
    )
