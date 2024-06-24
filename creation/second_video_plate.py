import os
import subprocess
'''Скрипт для создание пластинки №2 НО С ВИДЕО В ЦЕНТРЕ'''


def get_video_duration(video_path):
    result = subprocess.run(
        ['ffprobe', '-i', video_path, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return float(result.stdout)

def get_audio_duration(audio_path):
    result = subprocess.run(
        ['ffprobe', '-i', audio_path, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0'],
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



def crop_video_and_rotate(user_id, video_path, speed):
    '''Делаем видео 1 мин и Вырезаем квадрат из видео и аудио накладываем'''
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

    if speed == 1:
        speed = 8
    elif speed == 2:
        speed = 60
    command = [
        'ffmpeg',
        '-y',
        '-i', video_path,
        '-frames:v', '1',
        f'creation/img/{user_id}_first_cadr.png'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    command = [
        'ffmpeg',
        '-y',
        '-i', video_path,
        '-vf', "crop='min(iw,ih):min(iw,ih)',scale=1500:1500,format=yuv420p",
        '-c:v', 'libx264',
        '-crf', '23',
        '-preset', 'ultrafast',
        f'creation/video/{user_id}_crop_video.mp4'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(video_path)
    if duration < 60:
        command = [
            'ffmpeg',
            '-y',
            '-stream_loop', '-1',
            '-i', f'creation/video/{user_id}_crop_video.mp4',
            '-t', '60',
            '-c:v', 'libx264',
            '-b:v', '0',
            '-threads', 'auto',
            f'creation/video/{user_id}_looped.mp4'
        ]
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.remove(f'creation/video/{user_id}_crop_video.mp4')
        os.rename(f'creation/video/{user_id}_looped.mp4', f'creation/video/{user_id}_crop_video.mp4')
    command = [
        'ffmpeg',
        '-y',
        '-i', f'creation/video/{user_id}_crop_video.mp4',
        '-vf', f"rotate=2*PI*t/{speed}",
        '-pix_fmt', 'yuv420p',
        '-vcodec', 'libx264',
        f'creation/video/{user_id}_rotate_vinil.mp4'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(f'creation/video/{user_id}_crop_video.mp4')
    command = [
        'ffmpeg',
        '-y',
        '-i', 'creation/res/black.png',
        '-i', f'creation/video/{user_id}_rotate_vinil.mp4',
        '-i', 'creation/res/mask.png',
        '-filter_complex',
        "[1:v][2:v]alphamerge[masked]; [0:v][masked]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2:format=auto,format=yuv420p[v]",
        '-map', '[v]',
        '-c:v', 'libx264',
        '-shortest',
        f'creation/video/{user_id}_round_video.mp4'
    ]

    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(f'creation/video/{user_id}_rotate_vinil.mp4')
    return f'creation/video/{user_id}_round_video.mp4'


def make_video(user_id, video_path, audio_path, noise):
    '''Вставляем тень и иголку и аудио'''
    command = [
        'ffmpeg',
        '-y',
        '-i', video_path,
        '-i', audio_path,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-shortest',
        f'creation/video/{user_id}_video_audio.mp4'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(video_path)
    os.remove(audio_path)
    if noise:
        command = [
            'ffmpeg',
            '-y',
            '-i', f'creation/video/{user_id}_video_audio.mp4',
            '-i', 'creation/res/vinil_audio.mp3',
            '-filter_complex', '[1:a]volume=0.15[a1]; [0:a][a1]amix=inputs=2:duration=first',
            '-c:v', 'copy',
            f'creation/video/{user_id}_output_video_noise.mp4'
        ]
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.remove(f'creation/video/{user_id}_video_audio.mp4')
        os.rename(f'creation/video/{user_id}_output_video_noise.mp4', f'creation/video/{user_id}_video_audio.mp4')

    command = [
        'ffmpeg',
        '-y',
        '-i', f'creation/video/{user_id}_video_audio.mp4',
        '-i', 'creation/res/needle-min.png',
        '-i', 'creation/res/light-min.png',
        '-filter_complex',
        "[0][1]overlay=W-w-0:H-h-0[tmp1];[tmp1][2]overlay=W-w-0:H-h-0[v]",
        '-map', '[v]',
        '-map', '0:a',
        '-c:v', 'libx264',
        '-c:a', 'copy',
        f'creation/video/{user_id}_output_video.mp4'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(f'creation/video/{user_id}_video_audio.mp4')
    command = [
        'ffmpeg',
        '-y',
        '-i', f'creation/video/{user_id}_output_video.mp4',
        '-vf', 'scale=640:640',
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-preset', 'slow',
        '-crf', '28',
        f'creation/video/{user_id}_output_video_1m_round.mp4'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return (f'creation/video/{user_id}_output_video.mp4', f'creation/video/{user_id}_output_video_1m_round.mp4')
