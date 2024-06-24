import subprocess
import os

'''Скрипт для создания пластинки №2 (которая на весь виниловый диск)'''


def get_audio_duration(video_path):
    result = subprocess.run(
        ['ffprobe', '-i', video_path, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    duration = float(result.stdout)
    return int(duration) if duration<60 else 60

def cut_audio(user_id, audio_path, start_time):
    '''Обрезаем аудио до 1 минуты'''
    duration = get_audio_duration(audio_path)
    command = [
        'ffmpeg',
        '-y',
        '-i', audio_path,
        '-map', '0:a:0',
        '-ss', start_time,
        '-t', '00:01:00',
        '-acodec', 'libmp3lame',
        f'creation/audio/{user_id}_audio1m_temp.mp3'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(audio_path)
    command = [
        'ffmpeg',
        '-y',
        '-i', f'creation/audio/{user_id}_audio1m_temp.mp3',
        '-af', f"afade=t=in:st=0:d=5,afade=t=out:st={duration-1.5}:d=1.5",
        '-acodec', 'libmp3lame',
        f'creation/audio/{user_id}_audio1m.mp3'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(f'creation/audio/{user_id}_audio1m_temp.mp3')
    return f'creation/audio/{user_id}_audio1m.mp3'



def rotate_photo(user_id, audio_path, photo_path, speed):
    '''Создаем видео длинной 1 минуту где крутится фотка юзера'''
    if speed == 1:
        speed = 8
    elif speed == 2:
        speed = 60
    command = [
        'ffmpeg',
        '-y',
        '-i', photo_path,
        '-vf', "scale='max(1500,iw*1500/ih)':'max(1500,ih*1500/iw)'",
        f'creation/img/{user_id}_scale.png'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Изменяем размер
    os.rename(photo_path, f'creation/img/{user_id}_first_cadr.png')
    command = [
        'ffmpeg',
        '-y',
        '-i', f'creation/img/{user_id}_scale.png',
        '-filter_complex',
        "[0:v]crop=1500:1500:(in_w-1500)/2:(in_h-1500)/2[cropped]",
        '-map', '[cropped]',
        '-c:v', 'png',
        f'creation/img/{user_id}_square.png'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Вырезаем по квадрат
    os.remove(f'creation/img/{user_id}_scale.png')
    command = [
        'ffmpeg',
        '-y',
        '-loop', '1',
        '-i', f'creation/img/{user_id}_square.png',
        '-i', audio_path,
        '-i', 'creation/res/needle-min.png',
        '-t', '60',
        '-filter_complex',
        f"[0:v]rotate=2*PI*t/{speed}[rotated];[rotated][2:v]overlay=0:0:format=auto[v]",
        '-map', '[v]',
        '-map', '1:a',
        '-pix_fmt', 'yuv420p',
        '-vcodec', 'libx264',
        '-acodec', 'aac',
        '-preset', 'fast',
        '-shortest',
        f'creation/video/{user_id}_rotate.mp4'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(f'creation/img/{user_id}_square.png')
    os.remove(audio_path)
    return f'creation/video/{user_id}_rotate.mp4'


def make_video(user_id, video_vinil, noise):
    '''Собираем все в видео'''

    command = [
        'ffmpeg',
        '-y',
        '-i', 'creation/res/black.png',
        '-i', video_vinil,
        '-i', 'creation/res/mask.png',
        '-i', 'creation/res/light-min.png',
        '-i', 'creation/res/1shadow-min.png',
        '-filter_complex',
        "[1:v][2:v]alphamerge[masked_video];"
        "[0:v][masked_video]overlay=(W-w)/2:(H-h)/2[bg_with_rotating];"
        "[bg_with_rotating][3:v]overlay=(W-w)/2:(H-h)/2[bg_with_light];"
        "[bg_with_light][4:v]overlay=(W-w)/2:(H-h)/2",  # Наложение нового изображения
        '-codec:a', 'copy',
        f'creation/video/{user_id}_output_video.mp4'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Вставляем по маске
    os.remove(video_vinil)
    if noise:  # Накладываем шум если надо
        command = [
            'ffmpeg',
            '-y',
            '-i', f'creation/video/{user_id}_output_video.mp4',
            '-i', 'creation/res/vinil_audio.mp3',
            '-filter_complex', '[1:a]volume=0.15[a1]; [0:a][a1]amix=inputs=2:duration=first',
            '-c:v', 'copy',
            f'creation/video/{user_id}_output_video_noise.mp4'
        ]
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.remove(f'creation/video/{user_id}_output_video.mp4')
        os.rename(f'creation/video/{user_id}_output_video_noise.mp4', f'creation/video/{user_id}_output_video.mp4')
    command = [
        'ffmpeg',
        '-y',
        '-i', f'creation/video/{user_id}_output_video.mp4',
        '-vf', 'scale=640:640',
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-crf', '27',
        f'creation/video/{user_id}_output_video_1m_round.mp4'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Тут делаем видео для кружка
    return (f'creation/video/{user_id}_output_video.mp4', f'creation/video/{user_id}_output_video_1m_round.mp4')