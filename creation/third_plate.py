import subprocess
import os

'''Скрипт для создания пластинки №3(которая c бумажной текстурой типо)'''



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


def cut_photo(user_id, photo_path):
    '''Обрезаем квадрат'''
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
    return f'creation/img/{user_id}_square.png'


def overlay_photo(user_id, photo_name):
    '''Обычное наложение фото на фото
    Текстуры на кружок'''

    command = [
        'ffmpeg',
        '-y',
        '-i', photo_name,  # Убедитесь, что photo_name содержит правильный путь к изображению
        '-i', 'creation/res/paper_overlay_small.png',
        '-i', 'creation/res/light2.png',
        '-filter_complex',
        "[0:v]format=yuv420p[base];[1:v]setsar=1[overlay1];[base][overlay1]blend=all_mode='overlay':repeatlast=0[temp1];[temp1][2:v]overlay=W-w-0:H-h-0",
        f'creation/img/{user_id}_paper.png'  # Путь для сохранения результата
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(photo_name)
    return f'creation/img/{user_id}_paper.png'


def rotate_photo(user_id, photo_name, audio_path, speed):
    '''Делаем видео где крутится фото юзера'''
    if speed == 1:
        speed = 8
    elif speed == 2:
        speed = 60

    command = [
        'ffmpeg',
        '-y',
        '-loop', '1',
        '-i', photo_name,
        '-i', audio_path,
        '-i', 'creation/res/2light-min.png',
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
    os.remove(photo_name)
    os.remove(audio_path)
    return f'creation/video/{user_id}_rotate.mp4'


def make_video(user_id, video_path, noise):
    '''Создаем видео'''
    if noise:
        command = [
            'ffmpeg',
            '-y',
            '-i', video_path,
            '-i', 'creation/res/vinil_audio.mp3',
            '-filter_complex',
            '[1:a]volume=0.15[a1]; [0:a][a1]amix=inputs=2:duration=first',
            '-c:v', 'copy',
            f'creation/video/{user_id}_output_noise.mp4'
        ]
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.remove(video_path)
        video_path = f'creation/video/{user_id}_output_noise.mp4'

    command = [
        'ffmpeg',
        '-y',
        '-i', 'creation/res/black.png',
        '-i', video_path,
        '-i', 'creation/res/mask.png',
        '-filter_complex',
        "[1:v][2:v]alphamerge[masked_video];"
        "[0:v][masked_video]overlay=0:0",
        '-codec:a', 'copy',
        f'creation/video/{user_id}_background.mp4']
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(video_path)
    command = [
        'ffmpeg',
        '-y',
        '-i', f'creation/video/{user_id}_background.mp4',
        '-i', 'creation/res/needle-min.png',
        '-filter_complex', '[0:v][1:v]overlay=0:0',
        '-c:v', 'libx264',
        '-c:a', 'aac',
        f'creation/video/{user_id}_output_video.mp4'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(f'creation/video/{user_id}_background.mp4')
    command = [
        'ffmpeg',
        '-y',
        '-i', f'creation/video/{user_id}_output_video.mp4',
        '-i', 'creation/res/put2.png',
        '-filter_complex', '[0:v][1:v]overlay=0:0,scale=640:640,fps=25',
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-crf', '28',
        f'creation/video/{user_id}_output_video_1m_round.mp4'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return (f'creation/video/{user_id}_output_video.mp4', f'creation/video/{user_id}_output_video_1m_round.mp4')