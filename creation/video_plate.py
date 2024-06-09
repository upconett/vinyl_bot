from creation import first_video_plate, second_video_plate

'''Модуль для создания пластинок с видео
video - туда сохраняются готовые видосы
frames - там кадры
audio - там все аудио
users_video - там видосы юзеров'''

def make_first_plate_video(user_id, audio_path, video_path, start_time, speed, noise):
    '''Запускаем эту функцию для создания видео первой пластинки (НО В ЦЕНТРЕ ВИДЕО)
        user_id: id пользователя(создаем подпапки с этим id, чтобы ориентироваться какой файл какому юзеру принадлежат),
        video_path: путь к видео которое засовываем в саму пластинку
        audio_path: путь к видео
        start_time_audio: начало аудио в формате 00:00:10  часы:минуты:секунды
        speed: Вид скорости, только 2 значения 1 и 2 type:int (1 - 8RMP, 2 - 1 оборот за 1 минуту)
        noise: bool Делать ли шум винила на пластинке'''

    img_video = first_video_plate.make_temp_video(user_id, audio_path, start_time)
    crop = first_video_plate.crop_video(user_id, video_path)
    round_1m = first_video_plate.process_video(user_id, crop)
    vinil_with_video = first_video_plate.paste_round_in_vinil(user_id, round_1m, img_video[0])
    rotated_video = first_video_plate.rotate_vinil(user_id, vinil_with_video, speed)
    light_video = first_video_plate.paste_light_put(user_id, rotated_video, noise)
    return light_video

def make_second_plate_video(user_id, audio_path, video_path, start_time, speed, noise):
    '''Запускаем эту функцию для создания видео первой пластинки (НО В ЦЕНТРЕ ВИДЕО)
        user_id: id пользователя(создаем подпапки с этим id, чтобы ориентироваться какой файл какому юзеру принадлежат),
        video_path: путь к видео которое засовываем в саму пластинку
        audio_path: путь к видео
        start_time_audio: начало аудио в формате 00:00:10  часы:минуты:секунды
        speed: Вид скорости, только 2 значения 1 и 2 type:int (1 - 8RMP, 2 - 1 оборот за 1 минуту)
        noise: bool Делать ли шум винила на пластинке'''

    img_video = second_video_plate.make_temp_video(user_id, audio_path, start_time)
    crop = second_video_plate.crop_video(user_id, video_path)
    round_1m = second_video_plate.process_video(user_id, crop)
    vinil_with_video = second_video_plate.paste_round_in_vinil(user_id, round_1m, img_video[0])
    rotated_video = second_video_plate.rotate_vinil(user_id, vinil_with_video, speed)
    light_video = second_video_plate.paste_light_put(user_id, rotated_video, noise)
    return light_video

#make_first_plate_video(user_id, 'audio/kizaru.mp3', 'users_video/user_video.mp4', '00:00:20', 1, True)
#Закончил <function make_first_plate_video at 0x00000202BF685A80> за 0:02:35.481831

#make_second_plate_video(1, 'audio/kizaru.mp3', 'users_video/user_video2.mp4', '00:00:20', 1, True)
#Закончил <function make_second_plate_video at 0x000001B0C5075A80> за 0:07:16.988971