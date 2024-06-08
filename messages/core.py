from aiogram.types import User as AIOgramUser

from database.models.User import LangTypes
from database.dataclasses import ProfileData


def start(lang: LangTypes, user: AIOgramUser) -> str:
    match lang:
        case LangTypes.RU:
            return (
                f'Привет, {user.first_name}\n'
                'В этом боте ты можешь создать '
                'визуализацию музыки в виде кружка с '
                'пластинкой или вставить свое изображение в альбом!'
            )
        case LangTypes.EN:
            return (
                f'Hello, {user.first_name}\n'
                'With this bot you can create '
                'a video message of vinyl record '
                'or an album with your image!'
            )


def profile(lang: LangTypes, profile_data: ProfileData) -> str:
    pd = profile_data
    match lang:
        case LangTypes.RU:
            return (
                'Профиль\n' +
                f'Подписка: {"✅" if pd.subscribed else "❌"}\n' +
                (f"Истекает: {pd.expires_at}\n" if pd.subscribed else "") +
                '\n' +
                f'Бесплатных пластинок: {pd.free_vinyl}\n' +
                f'Бесплатных альбомов: {pd.free_albums}\n'
            )
        case LangTypes.EN:
            return (
                'Profile\n' +
                f'Subscription: {"✅" if pd.subscribed else "❌"}\n' +
                (f"Expires At: {pd.expires_at}\n" if pd.subscribed else "") +
                '\n' +
                f'Free Vinyl: {pd.free_vinyl}\n' +
                f'Free Albums: {pd.free_albums}\n'
            )


def language(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return 'Выбери язык'
        case LangTypes.EN:
            return 'Choose language'


def template_image_warning(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return 'Картинка шаблонов не выставлена!'
        case LangTypes.EN:
            return 'Templates image not set!'
