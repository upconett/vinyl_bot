from database.models.User import LangTypes


async def create_vinyl(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return 'Пришли мне аудио'
        case LangTypes.EN:
            return 'Send me audio'


async def no_free_vinyl(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return '🌠 Подпишитесь, чтобы создать новые пластинки'
        case LangTypes.EN:
            return '🌠 Subscribe to create new records'


async def audio_fail(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return 'Аудио должно длится минимум 3 секунды!'
        case LangTypes.EN:
            return 'Audio must be at least 3 seconds long!'


async def template_image_warning(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return 'Картинка шаблонов не выставлена!'
        case LangTypes.EN:
            return 'Templates image not set!'


async def create_vinyl_template(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return 'Супер! Теперь выбери шаблон пластинки'
        case LangTypes.EN:
            return 'Nice! Now choose vinyl template'


async def create_vinyl_cover(lang: LangTypes, template: int) -> str:
    match lang:
        case LangTypes.RU:
            return f'Выбран шаблон №{template}\nПришли мне картинку или видео на обложку'
        case LangTypes.EN:
            return f'Template №{template} chosen\nNow send me image or video for cover'


async def cover_failure(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return 'Пожалуйста пришлите фото со сжатием или видео'
        case LangTypes.EN:
            return 'Please, send compressed photo or video'


async def create_vinyl_noise(lang: LangTypes, cover_type: int) -> str:
    match lang:
        case LangTypes.RU:
            cover_type = 'фото' if cover_type == 1 else 'видео'
            return f'Получил {cover_type}-обложку\nДобавить шум винила на фон?'
        case LangTypes.EN:
            cover_type = 'photo' if cover_type == 1 else 'video'
            return f'Got {cover_type} cover\nDo we add vinyl noise?'


async def create_vinyl_speed(lang: LangTypes, noise: bool) -> str:
    match lang:
        case LangTypes.RU:
            return f'Добавляем шум: {"Да" if noise else "Нет"}\nВыбери скорость вращения диска'
        case LangTypes.EN:
            return f'Adding noise: {"Yes" if noise else "No"}\nChoose rotation speed'


async def create_vinyl_offset(lang: LangTypes, speed: str) -> str:
    match lang:
        case LangTypes.RU:
            return (
                f'Скорость вращения: {speed}\n'
                'Введи время начала трека в формате:\n'
                '02:30 (две минуты 30 секунд)'
            )
        case LangTypes.EN:
            return (
                f'Rotation Speed: {speed}\n'
                'Enter offset time in format:\n'
                '02:30 (2 minutes 30 seconds)'
            )


async def create_vinyl_approve(lang: LangTypes, data: dict) -> str:
    match lang:
        case LangTypes.RU:
            return (
                f'Выбран шаблон: {data["template"]}\n'
                f'Шум винила: {"✅" if data["noise"] else "❌"}\n'
                f'Скорость: {"Полный оборот" if data["speed"] else "8RPM"}\n'
                f'Начало трека: {data["offset"]}\n\n'
                'Создать пластинку с этими настройками?'
            )
        case LangTypes.EN:
            return (
                f'Template number: {data["template"]}\n'
                f'Vinyl noise: {"✅" if data["noise"] else "❌"}\n'
                f'Speed: {"Full turn" if data["speed"] else "8RPM"}\n'
                f'Offset: {data["offset"]}\n\n'
                'Create vinyl record with the settings?'
            )


async def wrong_format(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return 'Неверный формат!'
        case LangTypes.EN:
            return 'Invalid format!'