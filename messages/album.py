from database.models.User import LangTypes


def create_album_template(lang: LangTypes):
    match lang:
        case LangTypes.RU: return 'Выбери тип шаблона'
        case LangTypes.EN: return 'Choose template'


def wait_single_photo(lang: LangTypes):
    match lang:
        case LangTypes.RU:
            return 'Пришли мне фото которое будет на альбоме(В виде файла)\nУчти, что фото желательно горизонтальное фото, иначе может получиться некрасиво'
        case LangTypes.EN:
            return 'Send me a photo for album cover(File)\nKeep in mind that the photo is preferably a horizontal photo, otherwise it may turn out ugly'
    

def wait_first_photo(lang: LangTypes):
    match lang:
        case LangTypes.RU:
            return 'Пришли мне фото для левой страницы(В виде файла)\nУчти, что фото желательно вертикальное фото, иначе может получиться некрасиво'
        case LangTypes.EN:
            return 'Send me a photo for the left page of the album(File)\nKeep in mind that the photo is preferably a vertical photo, otherwise it may turn out ugly'


def wait_second_photo(lang: LangTypes):
    match lang:
        case LangTypes.RU:
            return (
                'Теперь пришли мне фото для правой страницы(В виде файла)\nУчти, что фото желательно вертикальное фото, иначе может получиться некрасиво'
            )
        case LangTypes.EN:
            return (
                'Now send me photo for right page of the album(File)\n'
                'Keep in mind that the photo is preferably a vertical photo, otherwise it may turn out ugly'
            )


def create_album_approve(lang: LangTypes, settings: dict):
    match lang:
        case LangTypes.RU:
            return (
                f'Выбран шаблон: {settings["template"]}\n\n'
                'Создать альбом с этими настройками?'
            )
        case LangTypes.EN:
            return (
                f'Template chose: {settings["template"]}\n\n'
                'Create album with the settings?'
            )


def wrong_photo_format(lang: LangTypes):
    match lang:
        case LangTypes.RU:
            return (
                'Пожалуйста, пришлите фото без сжатия весом менее 20 мбайт\n'
                'Или введите /start, чтобы отменить создание альбома'
            )
        case LangTypes.EN:
            return (
                'Please, send uncompressed photo less than 20 MB\n'
                'Or use /start to cancel album creation'
            )
        

def creation_end(lang: LangTypes, time: int, queue: int):
    match lang:
        case LangTypes.RU:
            return (
                f'Супер, подожди {time} сек и твой альбом будет готов\n'
                f'Перед тобой в очереди {queue} человек'
            )
        case LangTypes.EN:
            return (
                f'Excellent, wait {time} seconds and your album will be ready\n'
                f'It\'s {queue} people in queue before you'
            )


def no_free_albums(lang: LangTypes):
    match lang:
        case LangTypes.RU:
            return '🌠 Оформите подписку, чтобы создать новые альбомы'
        case LangTypes.EN:
            return '🌠 Subscribe to create new albums'


def album_ready(lang: LangTypes):
    match lang:
        case LangTypes.RU:
            return 'Ваш альбом готов ✅'
        case LangTypes.EN:
            return 'Your album is ready ✅'


def album_query_block(lang: LangTypes):
    match lang:
        case LangTypes.RU:
            return 'Подождите пока завершится создание другого вашего альбома ⌛' 
        case LangTypes.EN:
            return 'Wait for your other album to be ready ⌛'