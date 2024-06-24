from database.models.User import LangTypes
import time

def create_album_template(lang: LangTypes):
    match lang:
        case LangTypes.RU: return 'Выбери тип шаблона'
        case LangTypes.EN: return 'Choose template'
        

def wait_for_photo(lang: LangTypes):
    match lang:
        case LangTypes.RU:
            return 'Пришли фото без сжатия!\nУчти, что фото желательно скидывать разрешения X на Y иначе может получиться некрасиво'
        case LangTypes.EN:
            return 'Send uncompressed photo!\nKeep in mind that it is advisable to change photo resolutions X to Y, otherwise it may turn out ugly'


def wait_single_photo(lang: LangTypes):
    match lang:
        case LangTypes.RU:
            return 'Пришли мне фото которое будет на альбоме\n'
        case LangTypes.EN:
            return 'Send me a photo for album cover\n'
    

def wait_first_photo(lang: LangTypes):
    match lang:
        case LangTypes.RU:
            return 'Пришли мне фото для левой страницы\n'
        case LangTypes.EN:
            return 'Send me a photo for the left page of the album\n'


def wait_second_photo(lang: LangTypes):
    match lang:
        case LangTypes.RU:
            return (
                'Теперь пришли мне фото для правой страницы\n'
                'Учти, что фото желательно скидывать разрешения X на Y иначе может получиться некрасиво'
            )
        case LangTypes.EN:
            return (
                'Now send me photo for right page of the album\n'
                'Keep in mind that it is advisable to change photo resolutions X to Y, otherwise it may turn out ugly'
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
                'Пожалуйста, пришлите фото без сжатия\n'
                'Или введите /start, чтобы отменить создание альбома'
            )
        case LangTypes.EN:
            return (
                'Please, send uncompressed photo\n'
                'Or use /start to cancel album creation'
            )
        

def creation_end(lang: LangTypes, wait: int, queue: int):
    match lang:
        case LangTypes.RU:
            if wait <= 60: wait = f'{wait} секунд'
            else: wait = time.strftime('%M минут %S секунд', time.gmtime(wait))
            return (
                f'Супер, подожди {wait} и твой альбом будет готов\n'
                f'Перед тобой в очереди {queue} человек'
            )
        case LangTypes.EN:
            if wait <= 60: wait = f'{wait} seconds'
            else: wait = time.strftime('%M minutes %S seconds', time.gmtime(wait))
            return (
                f'Excellent, wait {wait} and your album will be ready\n'
                f'It\'s {queue} people in queue before you'
            )


def no_free_albums(lang: LangTypes):
    match lang:
        case LangTypes.RU:
            return '🌠 Подпишитесь, чтобы создать новые альбомы'
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
