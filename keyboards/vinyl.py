from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models.User import LangTypes

def create_vinyl(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU: text = 'Назад'
        case LangTypes.EN: text = 'Back'
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=text, callback_data='start')
    return keyboard.as_markup()
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models.User import LangTypes

def create_vinyl(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU: text = 'Назад'
        case LangTypes.EN: text = 'Back'
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=text, callback_data='start')
    return keyboard.as_markup()


def create_vinyl_template(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU: text = 'Назад'
        case LangTypes.EN: text = 'Back'
    keyboard = InlineKeyboardBuilder()
    for x in range(1, 4):
        keyboard.button(
def create_vinyl_template(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU: text = 'Назад'
        case LangTypes.EN: text = 'Back'
    keyboard = InlineKeyboardBuilder()
    for x in range(1, 4):
        keyboard.button(
            text=f'{x}', 
            callback_data=f'create_vinyl_template_{x}'
        )
    keyboard.button(text=text, callback_data='start')
    keyboard.adjust(3,1)
    return keyboard.as_markup()


def create_vinyl_noise(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU: texts = ['Да', 'Нет', 'Назад']
        case LangTypes.EN: texts = ['Yes', 'No', 'Back']
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=texts[0], callback_data='create_vinyl_noise_1')
    keyboard.button(text=texts[1], callback_data='create_vinyl_noise_0')
    keyboard.button(text=texts[2], callback_data='start')
    keyboard.adjust(2, 1)
    return keyboard.as_markup()


def create_vinyl_speed(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU: texts = ['Полный оборот', 'Назад']
        case LangTypes.EN: texts = ['Full turn', 'Back']
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='8RMP', callback_data='create_vinyl_speed_1')
    keyboard.button(text=texts[0], callback_data='create_vinyl_speed_2')
    keyboard.button(text=texts[1], callback_data='start')
    keyboard.adjust(1, repeat=True)
    return keyboard.as_markup()


def create_vinyl_offset(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU: texts = ['С начала', 'Назад']
        case LangTypes.EN: texts = ['From the beginning', 'Back']
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=texts[0], callback_data='create_vinyl_offset_start')
    keyboard.button(text=texts[1], callback_data='start')
    keyboard.adjust(1, repeat=True)
    return keyboard.as_markup()


def create_vinyl_approve(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU: texts = ['Создать', 'Отмена']
        case LangTypes.EN: texts = ['Create', 'Cancel']
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=texts[0], callback_data='create_vinyl_approve')
    keyboard.button(text=texts[1], callback_data='start')
    keyboard.adjust(1, repeat=True)
    return keyboard.as_markup()


def get_player(lang: LangTypes, unique_id: int) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU:
            text1 = 'Скачать 💽'
            text2 = 'Вернуться'
        case LangTypes.EN:
            text1 = 'Download 💽'
            text2 = 'Go back'
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=text1, callback_data=fr'get_player_{unique_id}')
    keyboard.button(text=text2, callback_data='start')
    keyboard.adjust(1, repeat=True)
    return keyboard.as_markup()


def player_types(unique_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for x in range(1, 4):
        keyboard.button(
            text=f'{x}', 
            callback_data=f'player_template_{unique_id}_{x}'
        ) 
    return keyboard.as_markup()

def go_back_or_make(lang: LangTypes, unique_id: int) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU:
            text1 = 'Вернуться'
            text2 = 'Скачать еще💽'
        case LangTypes.EN:
            text1 = 'Go back'
            text2 = 'Download more💽'
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=text2, callback_data=fr'get_player_{unique_id}')
    keyboard.button(text=text1, callback_data='start')
    keyboard.adjust(1, repeat=True)
    return keyboard.as_markup()
