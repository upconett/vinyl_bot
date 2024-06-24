from aiogram.types import User as AIOgramUser

from database.models.User import LangTypes
from database.dataclasses import ProfileData


def start(lang: LangTypes, user: AIOgramUser) -> str:
    match lang:
        case LangTypes.RU:
            return (
                f'Привет, {user.first_name} 👑\n'
                'В этом боте ты можешь создать '
                'визуализацию музыки в виде кружка с '
                'пластинкой или вставить свое изображение в альбом!'
            )
        case LangTypes.EN:
            return (
                f'Hello, {user.first_name} 👑\n'
                'With this bot you can create '
                'a video message of vinyl record '
                'or an album with your image!'
            )


def stats(lang: LangTypes, data: dict) -> str:
    match lang:
        case LangTypes.RU:
            return (
                'Статистика работы бота\n\n'
                f'Всего пользователей: {data["users_total"]}\n'
                f'Активных: {data["users_active"]}\n'
                f'Заблокировали: {data["users_blocked"]}\n\n'
                f'Присоединилось сегодня: {data["users_today"]}\n'
                f'Оплатили подписку: {sum((data["sub_today_month"], data["sub_today_6month"], data["sub_today_12month"]))}\n'
                f'На 1 мес: {data["sub_today_month"]}\n'
                f'На 6 мес: {data["sub_today_6month"]}\n'
                f'На 12 мес: {data["sub_today_12month"]}\n\n'
                f'Всего Оплатили: {sum((data["sub_month"], data["sub_6month"], data["sub_12month"]))}\n'
                f'На 1 мес: {data["sub_month"]}\n'
                f'На 6 мес: {data["sub_6month"]}\n'
                f'На 12 мес: {data["sub_12month"]}\n\n'

                # 'Вы можете изменить картинку шаблонов:\n'
                # '/add_image_vinyl\n'
                # '/add_image_player\n'
                # '/add_image_album\n\n'
                'Вы можете отправить рассылку:\n'
                '/announce\n'
            )
        case LangTypes.EN:
            return (
                'Bot Activity Statistics\n\n'
                f'Total users: {data["users_total"]}\n'
                f'Active: {data["users_active"]}\n'
                f'Blocked: {data["users_blocked"]}\n\n'
                f'Joined today: {data["users_today"]}\n'
                f'Subscriptions paid today: {sum((data["sub_today_month"], data["sub_today_6month"], data["sub_today_12month"]))}\n'
                f'For 1 month: {data["sub_today_month"]}\n'
                f'For 6 months: {data["sub_today_6month"]}\n'
                f'For 12 months: {data["sub_today_12month"]}\n\n'
                f'Total Subscriptions Paid: {sum((data["sub_month"], data["sub_6month"], data["sub_12month"]))}\n'
                f'For 1 month: {data["sub_month"]}\n'
                f'For 6 months: {data["sub_6month"]}\n'
                f'For 12 months: {data["sub_12month"]}\n\n'
                # 'You can change image of templates:\n'
                # '/add_image_vinyl\n'
                # '/add_image_player\n'
                # '/add_image_album\n\n'
                'You can make announcement:\n'
                '/announce\n'
            )



def announcement_help(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return (
                'С помощью этой команды вы можете отправить рассылку **всем пользователям** бота\n\n'
                '**Использование\:**\n'
                '\/announce\n'
                'Ваше *соообщение* с ||любым форматированием|| здесь\.\.\.'
            )
        case LangTypes.EN:
            return (
                'Using this command you can send announcement to **each user** of the bot\n\n'
                '**Usage\:**\n'
                '\/announce\n'
                'Your *message* with ||any formatting|| here\.\.\.'
            )


def announcement_approve_1(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return 'Ваше сообщение будет выглядеть так:'
        case LangTypes.EN:
            return 'Your message will look like that:'


def announcement_approve_2(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return '*Запустить рассылку пользователям\?*'
        case LangTypes.EN:
            return '*Start Announcement\?*'


def vinyl_template(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return 'Картинка шаблонов пластинок изменена ✅'
        case LangTypes.EN:
            return 'Vinyl templates picture changed ✅'


def album_template(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return 'Картинка шаблонов альбомов изменена ✅'
        case LangTypes.EN:
            return 'Album templates picture changed ✅'

            
def player_template(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return 'Картинка шаблонов проигрывателей изменена ✅'
        case LangTypes.EN:
            return 'Players templates picture changed ✅'


def add_image_help(lang: LangTypes, command: str) -> str:
    match lang:
        case LangTypes.RU:
            return f'Пришлите картинку с подписью `{command}` чтобы сменить шаблон'
        case LangTypes.EN:
            return f'Send me image with `{command}` as caption to change template' 


def announce_start(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return f'📩 Начинаю рассылку сообщения для всех пользователей...'
        case LangTypes.EN:
            return f'📩 Start sending announcements to everyone...'


def announce_end(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return f'Рассылка успешно завершена ✅'
        case LangTypes.EN:
            return f'Announcement ended successfully ✅'
