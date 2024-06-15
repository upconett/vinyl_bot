import os
import subprocess
import datetime


def make_background(user_id, photo_path):
    '''Создаем фон'''
    command = [
        'ffmpeg',
        '-y',
        '-i', photo_path,
        '-vf', "scale='max(2276,iw*1518/ih)':'max(1518,ih*2276/iw)'",
        f'creation/img/{user_id}_scale.png'
    ]
    subprocess.run(command)
    os.remove(photo_path)

    command = [
        'ffmpeg',
        '-y',
        '-i', f'creation/img/{user_id}_scale.png',
        '-vf',
        "crop=2276:1518:(iw-2276)/2:(ih-1518)/2, scale=2276:1518:force_original_aspect_ratio=decrease, pad=2276:1518:(ow-iw)/2:(oh-ih)/2, gblur=sigma=100",
        f'creation/img/{user_id}_background.png'
    ]
    subprocess.run(command)
    os.remove(f'creation/img/{user_id}_scale.png')
    return f'creation/img/{user_id}_background.png'


def paste_soft_light(user_id, photo_path):
    '''Накладываем слой методом soft_light'''
    command = [
        'ffmpeg',
        '-y',
        '-i', photo_path,
        '-i', 'creation/res/player3_soft_light.png',
        '-filter_complex', "[0:v][1:v]blend=shortest=1:all_mode=softlight",
        f'creation/img/{user_id}_soft_light.png']
    subprocess.run(command)
    os.remove(photo_path)
    return f'creation/img/{user_id}_soft_light.png'


def paste_multiply(user_id, photo_path):
    '''Накладываем слой методом multiply'''
    command = [
        'ffmpeg',
        '-y',
        '-i', photo_path,
        '-i', 'creation/res/player3_multiply.png',
        '-filter_complex', "[0:v][1:v]blend=shortest=1:all_mode=multiply",
        f'creation/img/{user_id}_multiply.png']
    subprocess.run(command)
    os.remove(photo_path)
    return f'creation/img/{user_id}_multiply.png'


def paste_screen(user_id, photo_path):
    '''Накладываем слой методом multiply'''
    command = [
        'ffmpeg',
        '-y',
        '-i', photo_path,
        '-i', 'creation/res/player3_screen.png',
        '-filter_complex', "[0:v][1:v]blend=shortest=1:all_mode=screen",
        f'creation/img/{user_id}_screen.png']
    subprocess.run(command)
    os.remove(photo_path)
    return f'creation/img/{user_id}_screen.png'


def paste_normal(user_id, photo_path):
    '''Накладываем простой слой'''
    command = [
        'ffmpeg',
        '-y',
        '-i', photo_path,
        '-i', 'creation/res/player3_normal.png',
        '-filter_complex', "overlay",
        f'creation/img/{user_id}_normal.png']
    subprocess.run(command)
    os.remove(photo_path)
    return f'creation/img/{user_id}_normal.png'

def paste_video(user_id, video_path, background):
    '''Вставляем видео пластинки'''
    command = [
        'ffmpeg',
        '-y',
        '-loop', '1',
        '-i', background,
        '-i', video_path,
        '-i', 'creation/res/mask.png',
        '-filter_complex',
        "[1:v]scale=942:942,setsar=1[vid_resized];"
        "[2:v]scale=942:942[mask_resized];"
        "[vid_resized][mask_resized]alphamerge[masked];"
        "[0:v][masked]overlay=902:94:format=auto,format=yuv420p[v]",
        '-map', '[v]',
        '-map', '1:a',
        '-c:v', 'libx264',
        '-c:a', 'copy',
        '-shortest',
        f'creation/video/{user_id}_vinil.mp4'
    ]
    subprocess.run(command)
    os.remove(background)
    return f'creation/video/{user_id}_vinil.mp4'

def paste_needle(user_id, video_path):
    '''Накладываем иголку'''
    command = [
        'ffmpeg',
        '-y',
        '-i', video_path,
        '-i', 'creation/res/player3_needle.png',
        '-filter_complex', "overlay",
        f'creation/video/{user_id}_player3.mp4']
    subprocess.run(command)
    os.remove(video_path)
    return f'creation/img/{user_id}_player3.png'