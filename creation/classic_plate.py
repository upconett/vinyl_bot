from creation import first_plate, second_plate

''''Модуль для классических пластинок (с фотками)

video - туда сохраняются готовые видосы
frames - там кадры
audio - там все аудио
img - там фотки
'''

def make_first_plate_vinil(user_id, photo_path, audio_path, start_time_audio, speed, noise):
    '''Запускаем эту функцию для создания видео первой пластинки
    user_id: id пользователя(создаем подпапки с этим id, чтобы ориентироваться какой файл какому юзеру принадлежат),
    photo_path: путь к фото которое засовываем в саму пластинку
    audio_path: путь к видео
    start_time_audio: начало аудио в формате 00:00:10  часы:минуты:секунды
    speed: Вид скорости, только 2 значения 1 и 2 type:int (1 - 8RMP, 2 - 1 оборот за 1 минуту)
    noise: bool Делать ли шум винила на пластинке'''
    circl_name = first_plate.circle_image(photo_path, user_id)  # Вырезаем кружок из фото юзера
    big_circle_name = first_plate.paste_circle_in_vinil(circl_name, user_id)  # Вставляем на черный круг
    shadow_name = first_plate.paste_shadow_mask_for_the_small(big_circle_name, user_id)
    first_plate.rotate_image(shadow_name, speed, user_id) #Нарезаем кадры для видео
    video_name = first_plate.make_video(audio_path, user_id, start_time_audio, noise) #Собираем видео
    return video_name


def make_second_plate_vinil(user_id, photo_path, audio_path, start_time_audio, speed, noise):
    '''Запускаем эту функцию для создания видео второй пластинки
        user_id: id пользователя(создаем подпапки с этим id, чтобы ориентироваться какой файл какому юзеру принадлежат),
        photo_path: путь к фото которое засовываем в саму пластинку
        audio_path: путь к видео
start_time_audio: начало аудио в формате 00:00:10  часы:минуты:секунды
        speed: Вид скорости, только 2 значения 1 и 2 type:int (1 - 8RMP, 2 - 1 оборот за 1 минуту)
        noise: bool Делать ли шум винила на пластинке'''
    circl_name = second_plate.circle_image(photo_path, user_id)  # Вырезаем кружок из фото юзера
    big_circle_name = second_plate.paste_circle_in_vinil(circl_name, user_id)  # Вставляем на черный круг
    second_plate.rotate_image(big_circle_name, speed, user_id) #
    video_name = second_plate.make_video(audio_path, user_id, start_time_audio, noise)
    return video_name

# print(make_first_plate_vinil(1, 'img/photo.jpeg', 'audio/kizaru.mp3', '00:00:00', 2, True))
#Закончил 0:00:45.749653 - короткий
#Закончил 0:01:22.233967 - длинное

#print(make_second_plate_vinil(1, 'img/photo.png', 'audio/kizaru.mp3', '00:10', 2, False))
#Закончил 0:00:47.753006 - короткий
#Закончил 0:01:29.891078 - длинное