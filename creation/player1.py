import os
import subprocess


def make_background(user_id, photo_path):
    '''Создаем фон'''
    command = [
        'ffmpeg',
        '-y',
        '-i', photo_path,
        '-vf', "scale='max(1080,iw*1920/ih)':'max(1920,ih*1080/iw)'",
        f'creation/img/{user_id}_scale.png'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    command = [
        'ffmpeg',
        '-y',
        '-i', f'creation/img/{user_id}_scale.png',
        '-vf',
        "crop=1080:1920:(iw-1080)/2:(ih-1920)/2, scale=1080:1920:force_original_aspect_ratio=decrease, pad=1080:1920:(ow-iw)/2:(oh-ih)/2, gblur=sigma=100",
        f'creation/img/{user_id}_background.png'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(f'creation/img/{user_id}_scale.png')
    return f'creation/img/{user_id}_background.png'

def paste_video_and_player(user_id, background_path, video_path):
    command = [
        'ffmpeg',
        '-y',
        '-i', background_path,
        '-i', 'creation/res/player1.png',
        '-filter_complex', "overlay=0:0",
        f'creation/img/{user_id}_player.png'
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(background_path)
    command = [
        'ffmpeg',
        '-y',
        '-loop', '1',
        '-i', f'creation/img/{user_id}_player.png',
        '-i', video_path,
        '-i', 'creation/res/mask.png',
        '-filter_complex',
        "[1:v]scale=720:720,setsar=1[vid_resized];"
        "[2:v]scale=720:720[mask_resized];"
        "[vid_resized][mask_resized]alphamerge[masked];"
        "[0:v][masked]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2:format=auto,format=yuv420p[v]",
        '-map', '[v]',
        '-map', '1:a',
        '-c:v', 'libx264',
        '-c:a', 'copy',
        '-shortest',
        f'creation/video/{user_id}_player1.mp4'
    ]

    # Выполнение команды
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(f'creation/img/{user_id}_player.png')
    return f'creation/video/{user_id}_player1.mp4'
