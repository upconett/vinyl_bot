import os
import subprocess
import datetime
'''Скрипт для создание пластинки №2 НО С ВИДЕО НА ВСЮ ПЛАСТИНКУ'''

def get_video_duration(video_path):
    result = subprocess.run(
        ['ffprobe', '-i', video_path, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return float(result.stdout)


def time_count(func):
    def wrapper(*args, **kwargs):
        time_start = datetime.datetime.now()
        print(f'Запускаю {func}')
        result = func(*args, **kwargs)
        print(f'Закончил {func} за {datetime.datetime.now() - time_start}')
        print('________________________\n')
        return result

    return wrapper


@time_count
def make_temp_video(user_id, audio_path, start_time):
    '''Обрезаем аудио до 1 минуты и сделаем видео где картинка шаблона пластинки под музыку'''
    trim_audio_command = [
        'ffmpeg',
        '-y',
        '-i', audio_path,
        '-ss', start_time,
        '-t', '00:01:00',
        '-acodec', 'libmp3lame',
        '-preset', 'ultrafast',
        f'creation/audio/{user_id}_audio1m.mp3'
    ]
    subprocess.run(trim_audio_command)
    create_video_command = [
        'ffmpeg',
        '-y',
        '-loop', '1',
        '-i', 'creation/res/3.movement.png',
        '-i', f'creation/audio/{user_id}_audio1m.mp3',
        '-c:v', 'libx264',
        '-tune', 'stillimage',
        '-c:a', 'copy',
        '-shortest',
        '-pix_fmt', 'yuv420p',
        '-preset', 'ultrafast',
        f'creation/video/{user_id}_image_video.mp4'
    ]
    subprocess.run(create_video_command)
    os.remove(audio_path)
    os.remove(f'creation/audio/{user_id}_audio1m.mp3')

    return (f'creation/video/{user_id}_image_video.mp4', f'creation/audio/{user_id}_audio1m.mp3')

@time_count
def crop_video(user_id, video_path):
    '''Вырезаем квадрат из видео'''
    command = [
        'ffmpeg',
        '-y',
        '-i', video_path,
        '-vf', "crop='min(iw,ih):min(iw,ih)',format=rgba",
        '-c:v', 'libx264',
        '-crf', '23',
        '-preset', 'ultrafast',
        f'creation/video/{user_id}_crop_video.mp4'
    ]

    subprocess.run(command)
    os.remove(video_path)
    return f'creation/video/{user_id}_crop_video.mp4'

@time_count
def process_video(user_id, video_path):
    '''Обрабатываем видео - зацикливаем либо обзераем, крч чтоб было 1 мин И делаем из него круг'''
    print(video_path)
    duration = get_video_duration(video_path)
    loop_or_trim1 = []
    loop_or_trim2 = []

    if duration < 60:
        loop_or_trim1 = ['-stream_loop', '-1']
        loop_or_trim2 = ['-t', '60']
    else:
        loop_or_trim1 = ['-t', '60']

    command = [
        'ffmpeg',
        '-y',
        *loop_or_trim1,
        '-i', video_path,
        '-loop', '1',
        '-i', 'creation/res/mask.png',
        *loop_or_trim2,
        '-filter_complex', "[0:v][1:v]scale2ref[video][mask];[video][mask]alphamerge,format=yuva420p",
        '-c:v', 'png',
        '-crf', '23',
        '-b:v', '0',
        '-threads', 'auto',
        f'creation/video/{user_id}_round.mp4'
    ]
    subprocess.run(command)
    os.remove(video_path)
    return f'creation/video/{user_id}_round.mp4'

@time_count
def paste_round_in_vinil(user_id, round_path, vinil_path):
    '''Накладываем видео юзера в пластинку не крутящуюся'''
    command = [
        'ffmpeg',
        '-y',
        '-i', vinil_path,
        '-i', round_path,
        '-filter_complex', "[0:v][1:v]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2:shortest=1[v]",
        '-map', '[v]',
        '-map', '0:a',
        '-c:v', 'libx264',
        '-crf', '23',
        '-preset', 'veryslow',
        f'creation/video/{user_id}_vinil_with_video.mp4'
    ]
    subprocess.run(command)

    os.remove(round_path)
    os.remove(vinil_path)
    return f'creation/video/{user_id}_vinil_with_video.mp4'

@time_count
def rotate_vinil(user_id, video_path, speed):
    '''Заставляем крутиться'''

    if speed == 1:
        speed = 8
    elif speed == 2:
        speed = 60
    command = [
        'ffmpeg',
        '-y',
        '-i', video_path,
        '-vf', f"rotate=2*PI*t/{speed}:c=black@0:ow=ih:oh=ih",
        '-t', '60',
        '-pix_fmt', 'yuv420p',
        '-vcodec', 'libx264',
        f'creation/video/{user_id}_rotate_vinil.mp4'
    ]
    subprocess.run(command)
    os.remove(video_path)
    return f'creation/video/{user_id}_rotate_vinil.mp4'


@time_count
def paste_light_put(user_id, video_path, noise):
    '''Вставляем тень и иголку'''
    if noise:
        command = [
            'ffmpeg',
            '-y',
            '-i', video_path,
            '-i', 'creation/res/vinil_audio.mp3',
            '-filter_complex', '[1:a]volume=0.1[a1]; [0:a][a1]amix=inputs=2:duration=first',
            '-c:v', 'copy',
            f'creation/video/{user_id}_output_video_noise.mp4'
        ]
        subprocess.run(command)
        os.remove(video_path)
        video_path = f'creation/video/{user_id}_output_video_noise.mp4'

    command = [
        'ffmpeg',
        '-y',
        '-i', video_path,
        '-i', 'creation/res/light.png',
        '-i', 'creation/res/put.png',
        '-filter_complex',
        "[0][1]overlay=W-w-0:H-h-0[tmp1];[tmp1][2]overlay=W-w-0:H-h-0",
        '-codec:a', 'copy',
        '-codec:v', 'libx264',
        f'creation/video/{user_id}_output_video.mp4'
    ]
    subprocess.run(command)
    os.remove(video_path)
    command = [
        'ffmpeg',
        '-y',
        '-i', f'creation/video/{user_id}_output_video.mp4',
        '-vf', 'scale=640:640',
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-preset', 'slow',
        f'creation/video/{user_id}_output_video_1m_round.mp4'
    ]
    subprocess.run(command)
    return (f'creation/video/{user_id}_output_video.mp4', f'creation/video/{user_id}_output_video_1m_round.mp4')

user_id = 1
@time_count
def make_second_plate_video(user_id, audio_path, video_path, start_time, speed, noise):
    '''Запускаем эту функцию для создания видео первой пластинки (НО В ЦЕНТРЕ ВИДЕО)
        user_id: id пользователя(создаем подпапки с этим id, чтобы ориентироваться какой файл какому юзеру принадлежат),
        video_path: путь к видео которое засовываем в саму пластинку
        audio_path: путь к видео
        start_time_audio: начало аудио в формате 00:00:10  часы:минуты:секунды
        speed: Вид скорости, только 2 значения 1 и 2 type:int (1 - 8RMP, 2 - 1 оборот за 1 минуту)
        noise: bool Делать ли шум винила на пластинке'''

    img_video = make_temp_video(user_id, audio_path, start_time)
    crop = crop_video(user_id, video_path)
    round_1m = process_video(user_id, crop)
    vinil_with_video = paste_round_in_vinil(user_id, round_1m, img_video[0])
    rotated_video = rotate_vinil(user_id, vinil_with_video, speed)
    light_video = paste_light_put(user_id, rotated_video, noise)
    return light_video