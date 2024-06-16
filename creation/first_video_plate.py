import os
import subprocess
import datetime
def get_video_duration(video_path):
    result = subprocess.run(
        ['ffprobe', '-i', video_path, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return float(result.stdout)


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


def make_video_with_vinil(user_id, audio_path, speed):
    '''Создаем видео длинной 1 минуту где крутится заготовка под пластинку'''
    if speed == 1:
        speed = 8
    elif speed == 2:
        speed = 60

    command = [
        'ffmpeg',
        '-y',
        '-loop', '1',
        '-i', 'creation/res/3.movement.png',
        '-i', audio_path,
        '-i', 'creation/res/2-min.png',
        '-t', '60',
        '-filter_complex',
        f"[0:v]rotate=2*PI*t/{speed}:c=black@0:ow=ih:oh=ih[rotated];"
        "[rotated][2:v]overlay=0:0:format=auto[v]",
        '-map', '[v]',
        '-map', '1:a',
        '-pix_fmt', 'yuv420p',
        '-vcodec', 'libx264',
        '-acodec', 'aac',
        '-preset', 'fast',
        '-shortest',
        f'creation/video/{user_id}_rotate_vinil.mp4'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(audio_path)
    return f'creation/video/{user_id}_rotate_vinil.mp4'


def crop_video_and_rotate(user_id, video_path, speed):
    if speed == 1:
        speed = 8
    elif speed == 2:
        speed = 60
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

        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.remove(video_path)
        video_path = f'creation/video/{user_id}_1min.mp4'

    command = [
        'ffmpeg',
        '-y',
        '-i', video_path,
        '-frames:v', '1',
        f'creation/img/{user_id}_first_cadr.png'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Изменяем размер
    command = [
        'ffmpeg',
        '-y',
        '-i', video_path,
        '-vf', "scale='max(650,iw*650/ih)':'max(650,ih*650/iw)',crop=650:650:(in_w-650)/2:(in_h-650)/2",
        f'creation/video/{user_id}_processed_video.mp4'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(video_path)
    if duration < 60:
        command = [
            'ffmpeg',
            '-y',
            '-stream_loop', '-1',
            '-i', f'creation/video/{user_id}_processed_video.mp4',
            '-t', '59',
            '-c:v', 'libx264',
            '-b:v', '0',
            '-threads', 'auto',
            f'creation/video/{user_id}_looped.mp4'
        ]
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.remove(f'creation/video/{user_id}_processed_video.mp4')
        os.rename(f'creation/video/{user_id}_looped.mp4', f'creation/video/{user_id}_processed_video.mp4')
    # Заставляем крутится
    command = [
        'ffmpeg',
        '-y',
        '-i', f'creation/video/{user_id}_processed_video.mp4',
        '-vf', f"rotate=2*PI*t/{speed}",
        '-t', '59',
        f'creation/video/{user_id}_rotate_video.mp4'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(f'creation/video/{user_id}_processed_video.mp4')
    return f'creation/video/{user_id}_rotate_video.mp4'


def process_video(user_id, video_path, video_vinil, noise):
    '''Собираем все в видео.'''
    # Накладываем все че надо
    command = [
        'ffmpeg',
        '-y',
        '-i', video_vinil,
        '-i', video_path,
        '-i', 'creation/res/mask3.png',
        '-i', 'creation/res/1top-min.png',
        '-filter_complex',
        "[1][2]alphamerge[rotating_masked];[0][rotating_masked]overlay=(W-w)/2:(H-h)/2[bg_with_rotating];[bg_with_rotating][3]overlay=(W-w)/2:(H-h)/2",
        '-codec:a', 'copy',
        '-shortest',
        f'creation/video/{user_id}_output_video.mp4'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(f'creation/video/{user_id}_rotate_video.mp4')
    os.remove(video_vinil)
    # Шум винила
    if noise:
        command = [
            'ffmpeg',
            '-y',
            '-i', f'creation/video/{user_id}_output_video.mp4',
            '-i', 'creation/res/vinil_audio.mp3',
            '-filter_complex', '[1:a]volume=0.15[a1]; [0:a][a1]amix=inputs=2:duration=first',
            '-c:v', 'copy',
            f'creation/video/{user_id}_final_output_with_noise.mp4'
        ]
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.remove(f'creation/video/{user_id}_output_video.mp4')
        os.rename(f'creation/video/{user_id}_final_output_with_noise.mp4', f'creation/video/{user_id}_output_video.mp4')

    command = [
        'ffmpeg',
        '-y',
        '-i', f'creation/video/{user_id}_output_video.mp4',
        '-vf', 'scale=640:640',
        '-c:v', 'libx264',
        '-c:a', 'aac',
        f'creation/video/{user_id}_output_video_1m_round.mp4'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Тут делаем видео для кружка
    return (f'creation/video/{user_id}_output_video.mp4', f'creation/video/{user_id}_output_video_1m_round.mp4')
