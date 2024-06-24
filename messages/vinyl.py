from database.models.User import LangTypes
import time

def create_vinyl(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return 'Пришли мне аудио'
        case LangTypes.EN:
            return 'Send me audio'


def no_free_vinyl(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return '🌠 Подпишитесь, чтобы создать новые пластинки'
        case LangTypes.EN:
            return '🌠 Subscribe to create new records'


def audio_fail(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return 'Аудио должно длится минимум 3 секунды!'
        case LangTypes.EN:
            return 'Audio must be at least 3 seconds long!'


def create_vinyl_template(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return 'Супер! Теперь выбери шаблон пластинки'
        case LangTypes.EN:
            return 'Nice! Now choose vinyl template'


def create_vinyl_cover(lang: LangTypes, template: int) -> str:
    match lang:
        case LangTypes.RU:
            return f'Выбран шаблон №{template}\nПришли мне картинку или видео на обложку'
        case LangTypes.EN:
            return f'Template №{template} chosen\nNow send me image or video for cover'


def cover_failure(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return 'Пожалуйста пришлите фото со сжатием или видео'
        case LangTypes.EN:
            return 'Please, send compressed photo or video'


def create_vinyl_noise(lang: LangTypes, cover_type: int) -> str:
    match lang:
        case LangTypes.RU:
            cover_type = 'фото' if cover_type == 1 else 'видео'
            return f'Получил {cover_type}-обложку\nДобавить шум винила на фон?'
        case LangTypes.EN:
            cover_type = 'photo' if cover_type == 1 else 'video'
            return f'Got {cover_type} cover\nDo we add vinyl noise?'


def create_vinyl_speed(lang: LangTypes, noise: bool) -> str:
    match lang:
        case LangTypes.RU:
            return f'Добавляем шум: {"Да" if noise else "Нет"}\nВыбери скорость вращения диска'
        case LangTypes.EN:
            return f'Adding noise: {"Yes" if noise else "No"}\nChoose rotation speed'


def create_vinyl_offset(lang: LangTypes, speed: str) -> str:
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


def create_vinyl_approve(lang: LangTypes, data: dict) -> str:
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


def wrong_format(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return 'Неверный формат!'
        case LangTypes.EN:
            return 'Invalid format!'


def creation_end(lang: LangTypes, wait: int, queue: int):
    match lang:
        case LangTypes.RU:
            if wait <= 60: wait = f'{wait} секунд'
            else: wait = time.strftime('%M минут %S секунд', time.gmtime(wait))
            return (
                f'Супер, подожди {wait} и пластинка будет готова\n'
                f'Перед тобой в очереди {queue} человек'
            )
        case LangTypes.EN:
            if wait <= 60: wait = f'{wait} seconds'
            else: wait = time.strftime('%M minutes %S seconds', time.gmtime(wait))
            return (
                f'Super, wait {wait} for your record to be ready\n'
                f'It\'s {queue} people in queue before you'
            )


def record_missing(lang: LangTypes):
    match lang:
        case LangTypes.RU:
            return 'Ваша пластинка уже удалена'
        case LangTypes.EN:
            return 'Your record is already deleted'


def get_player(lang: LangTypes):
    match lang:
        case LangTypes.RU:
            return (
                'Вы можете скачать пластинку в хорошем качестве\n\n'
                'Мы храним ваши пластинки 24 часа\n'
                'После этого скачать её не получится'
            )
        case LangTypes.EN:
            return (
                'You can download the record in better quality\n\n'
                'We store your records for 24 hours\n'
                'You won\'t be able to donwload the record after that'
            )

        
def player_types(lang: LangTypes):
    match lang:
        case LangTypes.RU:
            return 'Выберите шаблон проигрывателя для вашей пластинки'
        case LangTypes.EN:
            return 'Choose record player template to download'

        
def player_get_ready(lang: LangTypes, wait: int, queue: int):
    match lang:
        case LangTypes.RU:
            if wait <= 60: wait = f'{wait} секунд'
            else: wait = time.strftime('%M минут %S секунд', time.gmtime(wait))

            return (
                f'Подождите {wait}, ваш проигрыватель скоро будет готов ⌛'
                f'\nПеред вами в очереди {queue} человек'
            )
        case LangTypes.EN:
            if wait <= 60: wait = f'{wait} seconds'
            else: wait = time.strftime('%M minutes %S seconds', time.gmtime(wait))
            return (
                f'Please, wait {wait}, your record player will be ready soon ⌛'
                f'\nThere are {queue} people in queue'
            )


def player_done(lang: LangTypes):
    match lang:
        case LangTypes.RU:
            return 'Ваш проигрыватель готов ✅'
        case LangTypes.EN:
            return 'Your record player ready ✅'


def vinyl_query_block(lang: LangTypes):
    match lang:
        case LangTypes.RU:
            return 'Подождите пока завершится создание другой вашей пластинки ⌛' 
        case LangTypes.EN:
            return 'Wait for your other record to be ready ⌛'


def player_query_block(lang: LangTypes):
    match lang:
        case LangTypes.RU:
            return 'Подождите пока завершится создание другого вашего проигрывателя ⌛' 
        case LangTypes.EN:
            return 'Wait for your other record player to be ready ⌛'


def too_big_video(lang: LangTypes):
    match lang:
        case LangTypes.RU:
            return 'Размер видео не должен привышать 10Мб\nПришлите, пожалуйста, другое видео или фото'
        case LangTypes.EN:
            return 'Video size can\'t be more than 10Mb\nPlease, send another video or photo'
