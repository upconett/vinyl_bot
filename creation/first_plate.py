from PIL import Image, ImageDraw
import subprocess
import os
import datetime
from concurrent.futures import ThreadPoolExecutor
import cv2
import glob

'''Скрипт для создания пластинки №1(которая классическая с изображением посередине)'''


def del_files(user_id):
    files_to_delete = glob.glob(f'creation/frames/{user_id}_*.png')
    print(files_to_delete)
    for file_path in files_to_delete:
        os.remove(file_path)

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
def circle_image(photo_path, user_id):
    '''Создание круга из фото'''
    image = Image.open(photo_path)

    # Размеры круга
    x, y, r = image.width // 2, image.height // 2, min(image.size) // 2  # x, y - координаты центра круга, r - радиус

    # Создаем маску для круга
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((x - r, y - r, x + r, y + r), fill=255)

    # Применяем маску к изображению
    transparent_area = Image.new("RGBA", image.size, (0, 0, 0, 0))  # Создаем прозрачное изображение для фона
    result = Image.composite(image, transparent_area, mask)

    # Обрезаем результат до размера круга
    cropped_result = result.crop((x - r, y - r, x + r, y + r))

    # Сохранение вырезанного круга
    cropped_result.save(f'creation/img/{user_id}_2photo.png')
    os.remove(photo_path)
    return f'creation/img/{user_id}_2photo.png'


@time_count
def paste_circle_in_vinil(photo_name, user_id):
    '''Обычное наложение фото на фото
    Кружка обложки на черный круг пластинки'''
    # Загрузка шаблона виниловой пластинки
    vinyl = Image.open('creation/res/3.movement.png').convert('RGBA')  # Преобразование в RGBA для поддержки прозрачности

    # Размер центра (можете изменить на нужный размер)
    center_size = (674, 674)

    # Загрузка изображения для центра и изменение его размера
    center_image = Image.open(photo_name).convert('RGBA')  # Убедитесь, что изображение в RGBA
    center_image = center_image.resize(center_size, Image.Resampling.LANCZOS)

    # Создание маски для круга
    mask = Image.new('L', center_size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, center_size[0], center_size[1]), fill=255)

    # Определение центра виниловой пластинки
    vinyl_size = vinyl.size
    center_position = ((vinyl_size[0] - center_size[0]) // 2, (vinyl_size[1] - center_size[1]) // 2)

    # Наложение центра изображения на шаблон виниловой пластинки с использованием маски
    vinyl.paste(center_image, center_position, mask)

    # Сохранение итогового изображения
    vinyl.save(f'creation/img/{user_id}_3photo.png')
    os.remove(photo_name)
    return f'creation/img/{user_id}_3photo.png'


@time_count
def paste_shadow_mask_for_the_small(photo_name, user_id):
    '''Наложение тени между пластинкой и абложкой для плавного перехода'''
    shadow = Image.open('creation/res/shadow.png')
    vinyl_image = Image.open(photo_name)
    vinyl_image.paste(shadow, (0, 2), shadow)
    vinyl_image.save(f'creation/img/{user_id}_3photo.png')
    return f'creation/img/{user_id}_3photo.png'

def rotate_and_save(img, speed, i, user_id):
    rows, cols, channels = img.shape
    white = cv2.imread('creation/res/black.png', cv2.IMREAD_UNCHANGED)
    M = cv2.getRotationMatrix2D((cols/2, rows/2), -speed * i, 1)
    rotated = cv2.warpAffine(img, M, (cols, rows), borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0))

    cv2.imwrite(f'creation/frames/{user_id}_{i}.png', rotated)
@time_count
def rotate_image(photo_path, speed, user_id):
    speed_map = {1: 1.4, 2: 0.2}
    speed = speed_map.get(speed, speed)
    step = int(360 / speed)

    img = cv2.imread(photo_path, cv2.IMREAD_UNCHANGED)

    with ThreadPoolExecutor(max_workers=10) as executor:
            for i in range(step):
                executor.submit(rotate_and_save, img, speed, i, user_id)
    os.remove(photo_path)
@time_count
def make_video(audio_path, user_id, start_time, noise:bool):
    '''Создаем само видео
    start time: Время  начала трека в формате 00:00:30 (hh:mm:ss) минуты:секунды'''
    # Определяем команду ffmpeg для создания видео из последовательности кадров
    command = [
        'ffmpeg',
        '-y',
        '-framerate', '30',
        '-i', f'creation/frames/{user_id}_%d.png',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuva420p',
        f'creation/video/{user_id}_temp_video.mp4'
    ]

    subprocess.run(command) #Тут мы создаем видео из всех кадров
    del_files(user_id)

    command = [
        'ffmpeg',
        '-y',
        '-i', f'creation/video/{user_id}_temp_video.mp4',
        '-i', 'creation/res/light.png',
        '-i', 'creation/res/put.png',
        '-filter_complex',
        "[0][1]overlay=W-w-0:H-h-0[tmp1];[tmp1][2]overlay=W-w-0:H-h-0",
        '-codec:a', 'copy',
        f'creation/video/{user_id}_temp_video2.mp4'

    ]
    subprocess.run(command) #Тут мы накладываем тень и иголку
    command = [
        'ffmpeg',
        '-y',
        '-i', audio_path,
        '-ss', start_time,
        '-t', '00:01:00',
        '-acodec', 'libmp3lame',
        f'creation/audio/{user_id}_audio1m.mp3'
    ]
    subprocess.run(command)  # Обрезаем аудио до 1 мин
    os.remove(audio_path)
    if noise:
        command = [
            'ffmpeg',
            '-y',
            '-stream_loop', '-1',
            '-i', f'creation/video/{user_id}_temp_video2.mp4',
            '-i', f'creation/audio/{user_id}_audio1m.mp3',
            '-shortest',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-t', '59',
            '-c:a', 'aac',
            '-strict', 'experimental',
            f'creation/video/{user_id}_output_video_temp.mp4'
        ]
        subprocess.run(command)#Накладываем аудио
        os.remove(f'creation/video/{user_id}_temp_video.mp4')
        os.remove(f'creation/video/{user_id}_temp_video2.mp4')
        os.remove(f'creation/audio/{user_id}_audio1m.mp3')
        command = [
            'ffmpeg',
            '-y',
            '-i', f'creation/video/{user_id}_output_video_temp.mp4',
            '-i', 'creation/res/vinil_audio.mp3',
            '-filter_complex',
            '[1:a]volume=0.15[a1]; [0:a][a1]amix=inputs=2:duration=first',
            '-c:v', 'copy',
            f'creation/video/{user_id}_output_video.mp4'
        ]
        subprocess.run(command)#Накладываем виниловый шум
        os.remove(f'creation/video/{user_id}_output_video_temp.mp4')
        command = [
            'ffmpeg',
            '-y',
            '-i', f'creation/video/{user_id}_output_video.mp4',
            '-vf', 'scale=640:640',
            '-c:v', 'libx264',
            '-c:a', 'aac',
            f'creation/video/{user_id}_output_video_1m_round.mp4'
        ]
        subprocess.run(command) #Тут делаем видео для кружка
        return (f'creation/video/{user_id}_output_video.mp4', f'creation/video/{user_id}_output_video_1m_round.mp4')
    command = [
        'ffmpeg',
        '-y',
        '-stream_loop', '-1',  # Повторение видео бесконечно
        '-i', f'creation/video/{user_id}_temp_video2.mp4',  # Исходное видео
        '-i', f'creation/audio/{user_id}_audio1m.mp3',  # Исходное аудио
        '-shortest',  # Прерывает выходной файл по самой короткой дорожке
        '-c:v', 'libx264',  # Кодек видео
        '-pix_fmt', 'yuv420p',  # Формат пикселей
        '-t', '59',  # Продолжительность выходного файла в секундах
        '-c:a', 'aac',  # Кодек аудио
        '-strict', 'experimental',  # Разрешает использование экспериментальных функций
        f'creation/video/{user_id}_output_video.mp4'  # Имя выходного файла
    ]
    subprocess.run(command)  # Накладываем аудио
    os.remove(f'creation/video/{user_id}_temp_video.mp4')
    os.remove(f'creation/video/{user_id}_temp_video2.mp4')
    os.remove(f'creation/audio/{user_id}_audio1m.mp3')
    command = [
        'ffmpeg',
        '-y',
        '-i', f'creation/video/{user_id}_output_video.mp4',
        '-vf', 'scale=640:640',
        '-c:v', 'libx264',
        '-c:a', 'aac',
        f'creation/video/{user_id}_output_video_1m_round.mp4'
    ]
    subprocess.run(command)  # Тут делаем видео для кружка
    return (f'creation/video/{user_id}_output_video.mp4', f'creation/video/{user_id}_output_video_1m_round.mp4')
