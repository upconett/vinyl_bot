import os
import subprocess
import datetime

'''Скрипт для создание пластинки №3 НО С ВИДЕО В ЦЕНТРЕ'''


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
def cut_audio(user_id, audio_path, start_time):
    '''Обрезаем аудио до 1 минуты'''
    command = [
        'ffmpeg',
        '-y',
        '-i', audio_path,
        '-map', '0:a:0',
        '-ss', start_time,
        '-t', '00:00:59',
        '-acodec', 'libmp3lame',
        f'creation/audio/{user_id}_audio1m.mp3'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(audio_path)
    return f'creation/audio/{user_id}_audio1m.mp3'


@time_count
def crop_video(user_id, video_path):
    '''Делаем видео 1 мин и Вырезаем квадрат из видео'''
    duration = get_video_duration(video_path)
    if duration > 60:
        command = [
            'ffmpeg',
            '-y',
            '-t', '60',
            '-i', video_path,
            '-c:v', 'libx264',
            '-crf', '23',
            '-b:v', '0',
            '-threads', 'auto',
            f'creation/video/{user_id}_1min.mp4'
        ]

        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Обрезаем видео до 60сек если оно длиньше
        os.remove(video_path)
        video_path = f'creation/video/{user_id}_1min.mp4'
    command = [
        'ffmpeg',
        '-y',
        '-i', video_path,
        '-frames:v', '1',
        f'creation/img/{user_id}_first_cadr.png'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Делаем первый кадр для проигрывателя
    command = [
        'ffmpeg',
        '-y',
        '-i', video_path,
        '-loop', '1',
        '-i', 'creation/res/paper_overlay_small.png',
        '-i', 'creation/res/light2.png',
        '-filter_complex',
        """
        [0:v]crop='min(iw,ih):min(iw,ih)',scale=1500:1500,format=yuv420p[base];
        [1:v]setsar=1[overlay1];
        [base][overlay1]blend=all_mode='overlay':repeatlast=0[temp1];
        [temp1][2:v]overlay=W-w-0:H-h-0
        """,
        '-c:v', 'libx264',
        f'creation/video/{user_id}_crop_video.mp4'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Накладываем текстуру и свет
    os.remove(video_path)
    if duration < 60:
        command = [
            'ffmpeg',
            '-y',
            '-stream_loop', '-1',
            '-i', f'creation/video/{user_id}_crop_video.mp4',
            '-t', '59',
            '-c:v', 'libx264',
            '-b:v', '0',
            '-threads', 'auto',
            f'creation/video/{user_id}_looped.mp4'
        ]
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Если видео меньше минуты зацикливаем
        os.remove(f'creation/video/{user_id}_crop_video.mp4')
        os.rename(f'creation/video/{user_id}_looped.mp4', f'creation/video/{user_id}_crop_video.mp4')

    return f'creation/video/{user_id}_crop_video.mp4'


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
        '-pix_fmt', 'yuv420p',
        '-vcodec', 'libx264',
        f'creation/video/{user_id}_rotate_vinil.mp4'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(video_path)
    return f'creation/video/{user_id}_rotate_vinil.mp4'


@time_count
def make_video(user_id, video_path, audio_path, noise):
    '''Заворачиваем в видео'''
    command = [
        'ffmpeg',
        '-y',
        '-loop', '1',
        '-i', 'creation/res/black.png',
        '-i', video_path,
        '-i', 'creation/res/mask.png',
        '-i', audio_path,
        '-filter_complex',
        "[1:v][2:v]alphamerge[masked]; [0:v][masked]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2:format=auto,format=yuv420p[v]",
        '-map', '[v]',
        '-map', '3:a',
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-shortest',
        f'creation/video/{user_id}_round_video.mp4'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Накладываем на черный фон по маске и аудио
    os.remove(video_path)
    os.remove(audio_path)
    if noise:  # Накладываем шум если надо
        command = [
            'ffmpeg',
            '-y',
            '-i', f'creation/video/{user_id}_round_video.mp4',
            '-i', 'creation/res/vinil_audio.mp3',
            '-filter_complex', '[1:a]volume=0.15[a1]; [0:a][a1]amix=inputs=2:duration=first',
            '-c:v', 'copy',
            f'creation/video/{user_id}_output_video_noise.mp4'
        ]
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.remove(f'creation/video/{user_id}_round_video.mp4')
        os.rename(f'creation/video/{user_id}_output_video_noise.mp4', f'creation/video/{user_id}_round_video.mp4')

    command = [
        'ffmpeg',
        '-y',
        '-i', f'creation/video/{user_id}_round_video.mp4',
        '-i', 'creation/res/2light-min.png',
        '-filter_complex',
        """
        [0:v][1:v]overlay=x=0:y=0
        """,
        '-c:v', 'libx264',
        '-c:a', 'copy',
        f'creation/video/{user_id}_output_video_temp.mp4'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Накладываем свет
    os.remove(f'creation/video/{user_id}_round_video.mp4')
    command = [
        'ffmpeg',
        '-y',
        '-i', f'creation/video/{user_id}_output_video_temp.mp4',
        '-i', 'creation/res/put2.png',
        '-filter_complex',
        """
        [0:v][1:v]overlay=x=0:y=0,scale=640:640
        """,
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-crf', '32',
        '-preset', 'veryslow',
        f'creation/video/{user_id}_output_video_1m_round.mp4'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Накладываем гвоздик и приводим в формат кружка
    command = [
        'ffmpeg',
        '-y',
        '-i', f'creation/video/{user_id}_output_video_temp.mp4',
        '-i', 'creation/res/put.png',
        '-filter_complex',
        """
        [0:v][1:v]overlay=x=0:y=0
        """,
        '-c:v', 'libx264',
        '-c:a', 'copy',
        f'creation/video/{user_id}_output_video.mp4'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Накладываем другой гвоздик для проигрывателя
    os.remove(f'creation/video/{user_id}_output_video_temp.mp4')
    return (f'creation/video/{user_id}_output_video.mp4', f'creation/video/{user_id}_output_video_1m_round.mp4')
