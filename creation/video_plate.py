from creation import first_video_plate
from creation import second_video_plate
from creation import third_video_plate

'''Модуль для создания пластинок с видео
video - туда сохраняются готовые видосы
frames - там кадры
audio - там все аудио
users_video - там видосы юзеров'''




def make_first_plate_video(user_id,  video_path, audio_path, start_time, speed, noise):
    '''Запускаем эту функцию для создания видео первой пластинки (НО В ЦЕНТРЕ ВИДЕО)
        user_id: id пользователя(создаем подпапки с этим id, чтобы ориентироваться какой файл какому юзеру принадлежат),
        video_path: путь к видео которое засовываем в саму пластинку
        audio_path: путь к видео
        start_time_audio: начало аудио в формате 00:00:10  часы:минуты:секунды
        speed: Вид скорости, только 2 значения 1 и 2 type:int (1 - 8RMP, 2 - 1 оборот за 1 минуту)
        noise: bool Делать ли шум винила на пластинке'''

    audio = first_video_plate.cut_audio(user_id, audio_path, start_time)
    rotate_vinil = first_video_plate.make_video_with_vinil(user_id, audio, speed)
    rotated_video = first_video_plate.crop_video_and_rotate(user_id, video_path, speed)
    final_video = first_video_plate.process_video(user_id, rotated_video, rotate_vinil, noise)
    return final_video


def make_second_plate_video(user_id,  video_path, audio_path, start_time, speed, noise):
    '''Запускаем эту функцию для создания видео первой пластинки (НО В ЦЕНТРЕ ВИДЕО)
        user_id: id пользователя(создаем подпапки с этим id, чтобы ориентироваться какой файл какому юзеру принадлежат),
        video_path: путь к видео которое засовываем в саму пластинку
        audio_path: путь к видео
        start_time_audio: начало аудио в формате 00:00:10  часы:минуты:секунды
        speed: Вид скорости, только 2 значения 1 и 2 type:int (1 - 8RMP, 2 - 1 оборот за 1 минуту)
        noise: bool Делать ли шум винила на пластинке'''

    audio = second_video_plate.cut_audio(user_id, audio_path, start_time)
    crop = second_video_plate.crop_video_and_rotate(user_id, video_path, speed)
    video = second_video_plate.make_video(user_id, crop,audio, noise)
    return video

def make_third_plate_video(user_id,  video_path, audio_path, start_time, speed, noise):
    '''Запускаем эту функцию для создания видео третей пластинки (НО В ЦЕНТРЕ ВИДЕО)
        user_id: id пользователя(создаем подпапки с этим id, чтобы ориентироваться какой файл какому юзеру принадлежат),
        video_path: путь к видео которое засовываем в саму пластинку
        audio_path: путь к видео
        start_time_audio: начало аудио в формате 00:00:10  часы:минуты:секунды
        speed: Вид скорости, только 2 значения 1 и 2 type:int (1 - 8RMP, 2 - 1 оборот за 1 минуту)
        noise: bool Делать ли шум винила на пластинке'''

    audio = third_video_plate.cut_audio(user_id, audio_path, start_time)
    crop = third_video_plate.crop_video(user_id, video_path)
    rotated_video = third_video_plate.rotate_vinil(user_id, crop, speed)
    video = third_video_plate.make_video(user_id, rotated_video, audio, noise)
    return video

#make_first_plate_video(1, 'users_video/user_video.mp4', 'creation/audio/kizaru.mp3', '00:00:00', 2, True)
# Закончил <function make_first_plate_video at 0x0000023ACACB3600> за 0:01:41.284915

# make_second_plate_video(1, 'users_video/user_video.mp4', 'creation/audio/kizaru.mp3','00:00:00', 2, True)
# Закончил <function make_second_plate_video at 0x0000018BFC54E840> за 0:03:55.710234

# make_third_plate_video(1, 'users_video/user_video.mp4', 'creation/audio/kizaru.mp3', '00:00:00', 1, True)
#Закончил <function make_third_plate_video at 0x000001FAAEC62AC0> за 0:05:40.207023