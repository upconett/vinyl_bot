from creation import first_plate
from creation import second_plate
from creation import third_plate

''''Модуль для классических пластинок (с фотками)
video - туда сохраняются готовые видосы
frames - там кадры
audio - там все аудио
img - там фотки
'''

def make_first_plate_vinil(user_id, photo_path, audio_path, start_time, speed, noise):
    '''Запускаем эту функцию для создания видео первой пластинки
    user_id: id пользователя(создаем подпапки с этим id, чтобы ориентироваться какой файл какому юзеру принадлежат),
    photo_path: путь к фото которое засовываем в саму пластинку
    audio_path: путь к видео
    start_time: начало аудио в формате 00:00:10  часы:минуты:секунды
    speed: Вид скорости, только 2 значения 1 и 2 type:int (1 - 8RMP, 2 - 1 оборот за 1 минуту)
    noise: bool Делать ли шум винила на пластинке'''
    audio = first_plate.cut_audio(user_id, audio_path, start_time)
    rotate_vinil = first_plate.make_video_with_vinil(user_id, audio, speed)
    video = first_plate.cut_image(user_id, photo_path, rotate_vinil, speed, noise)
    return video

def make_second_plate_vinil(user_id, photo_path, audio_path, start_time, speed, noise):
    '''Запускаем эту функцию для создания видео второй пластинки
        user_id: id пользователя(создаем подпапки с этим id, чтобы ориентироваться какой файл какому юзеру принадлежат),
        photo_path: путь к фото которое засовываем в саму пластинку
        audio_path: путь к видео
        start_time: начало аудио в формате 00:00:10  часы:минуты:секунды
        speed: Вид скорости, только 2 значения 1 и 2 type:int (1 - 8RMP, 2 - 1 оборот за 1 минуту)
        noise: bool Делать ли шум винила на пластинке'''
    audio = second_plate.cut_audio(user_id, audio_path, start_time)
    rotate_vinil = second_plate.rotate_photo(user_id, audio, photo_path, speed)
    video = second_plate.make_video(user_id, rotate_vinil, noise)
    return video

def make_third_plate_vinil(user_id, photo_path, audio_path, start_time, speed, noise):
    '''Запускаем эту функцию для создания видео третей пластинки пластинки
        user_id: id пользователя(создаем подпапки с этим id, чтобы ориентироваться какой файл какому юзеру принадлежат),
        photo_path: путь к фото которое засовываем в саму пластинку
        audio_path: путь к видео
        start_time: начало аудио в формате 00:00:10  часы:минуты:секунды
        speed: Вид скорости, только 2 значения 1 и 2 type:int (1 - 8RMP, 2 - 1 оборот за 1 минуту)
        noise: bool Делать ли шум винила на пластинке'''
    audio = third_plate.cut_audio(user_id, audio_path, start_time)
    cut = third_plate.cut_photo(user_id, photo_path)
    paper_photo = third_plate.overlay_photo(user_id, cut)
    rotated = third_plate.rotate_photo(user_id, paper_photo, audio, speed)
    video = third_plate.make_video(user_id, rotated, noise)
    return video

# print(make_first_plate_vinil(1, 'creation/img/photo.jpg', 'creation/audio/error.mp3', '00:01:00', 2, True))
# Среднее время - 1 мин

# print(make_second_plate_vinil(1, 'creation/img/photo.jpg', 'creation/audio/error.mp3', '00:30', 2, False))
# Среднее время - 1 мин

#print(make_third_plate_vinil(1, 'creation/img/photo3.jpg', 'creation/audio/audio2.mp3', '00:10', 1, True))
# Среднее время 2 мин