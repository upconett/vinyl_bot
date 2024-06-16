import os
import subprocess
import datetime
def time_count(func):
    def wrapper(*args, **kwargs):
        time_start = datetime.datetime.now()
        print(f'Запускаю {func}')
        result = func(*args, **kwargs)
        print(f'Закончил {datetime.datetime.now() - time_start}')
        print('________________________\n')
        return result

    return wrapper
@time_count
def make_background_video(user_id, video_path):
    command = [
        "ffmpeg",
        "-y",
        "-loop", "1",
        "-i", "creation/res/player_black.png",
        "-i", video_path,
        "-i", "creation/res/mask.png",
        "-filter_complex",
        "[1:v]scale=720:720,setsar=1[vid_resized]; [2:v]scale=720:720[mask_resized]; [vid_resized][mask_resized]alphamerge[masked]; [0:v][masked]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2:format=auto,format=yuv420p[v]",
        "-map", "[v]",
        "-map", "1:a",
        "-c:v", "libx264",
        "-c:a", "copy",
        "-shortest",
        f"creation/video/{user_id}_player_back.mp4"
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return f"creation/video/{user_id}_player_back.mp4"
@time_count
def paste_needle(user_id, video_path):
    # 04fc44
    command = [
        'ffmpeg',
        '-y',
        '-i', video_path,  # Исходное видео
        '-i', 'creation/res/needle.mov',  # Видео для наложения
        '-filter_complex', "[1:v]format=rgba,colorchannelmixer=aa=0.9[ovr]; [0:v][ovr]overlay",  # Фильтры для наложения
        '-c:v', 'libx264',  # Кодек для выходного видео
        '-crf', '23',  # Качество видео
        '-preset', 'fast',  # Пресет кодирования
        '-shortest',
        f'creation/video/{user_id}_player2.mp4'  # Выходной файл
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(video_path)
    return f'creation/video/{user_id}_player2.mp4'