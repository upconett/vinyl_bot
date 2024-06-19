from PIL import Image, ImageChops
import numpy as np


def open_image(image_path):
    return Image.open(image_path)


def bend_photo(img, coeff_depth, coeff_curvature):
    '''Делаем изгибы'''
    width, height = img.size

    # Создание массива для искривленного изображения
    data = np.array(img)

    # Параметры для искривления
    depth = -(int(height / coeff_depth))  # Глубина изгиба
    middle_x = 0
    middle_y = height // 2
    curvature = int(width / coeff_curvature)  # Ширина изгиба

    # Расчёт смещения для каждого столбца изображения
    x = np.arange(width)
    # Вычисление изгиба в зависимости от расстояния до середины
    offsets = depth * np.exp(-((x - middle_x) ** 2) / (2 * curvature ** 2))

    # Создание матрицы координат Y с учётом смещений для верхней и нижней половины
    yy_upper = np.tile(np.arange(middle_y), (width, 1)).T
    yy_lower = np.tile(np.arange(middle_y, height), (width, 1)).T - middle_y
    xx_upper = np.tile(x, (middle_y, 1))
    xx_lower = np.tile(x, (height - middle_y, 1))

    # Применение смещений: вверх для нижней половины, вниз для верхней
    yy_upper = np.clip(yy_upper + offsets[xx_upper].astype(int), 0, middle_y - 1)
    yy_lower = np.clip(yy_lower - offsets[xx_lower].astype(int) + middle_y, middle_y, height - 1)

    # Объединение верхней и нижней половин с применёнными смещениями
    result_upper = data[yy_upper, xx_upper]
    result_lower = data[yy_lower, xx_lower]
    result = np.vstack((result_upper, result_lower))

    # Преобразование массива обратно в изображение
    result_img = Image.fromarray(result)
    return result_img


def overlay_mask_right(image):
    '''Применяем маску для левого фото'''
    image = image.resize((721, 980))
    mask = Image.open('creation/res/mask3_al.png').convert("L")
    image.putalpha(mask)
    return image


def overlay_mask_left(image):
    '''Применяем маску для левого фото'''
    image = image.resize((545, 710))
    mask = Image.open('creation/res/mask5.png').convert("L")
    # Применение маски
    image.putalpha(mask)
    return image


def paste_photo(image, background, vertical_offset, horizontal_offset):
    '''Вставляем на поверхность альбома'''
    width, height = image.size
    result = Image.new('RGBA', background.size)
    result.paste(background, (0, 0))

    for x in range(width):
        for y in range(height):
            new_x = x + horizontal_offset
            new_y = y + vertical_offset
            if new_y >= background.height or new_x >= background.width:
                continue

            bp = background.getpixel((new_x, new_y))
            op = image.getpixel((x, y))
            alpha_factor = op[3] / 255
            new_r = int((bp[0] * op[0] / 255) * alpha_factor + bp[0] * (1 - alpha_factor))
            new_g = int((bp[1] * op[1] / 255) * alpha_factor + bp[1] * (1 - alpha_factor))
            new_b = int((bp[2] * op[2] / 255) * alpha_factor + bp[2] * (1 - alpha_factor))
            new_a = bp[3]  # Альфа-канал фонового пикселя сохраняется

            result.putpixel((new_x, new_y), (new_r, new_g, new_b, new_a))
    return result


def paste_shadow(image):
    '''Вставляем одну день методом difference'''
    background_image = image.convert('RGBA')
    overlay_image = Image.open('creation/res/soft_light.png')

    arr1 = np.array(background_image)
    arr2 = np.array(overlay_image)
    difference = np.abs(arr1 - arr2)

    # Преобразование результата обратно в объект изображения PIL
    result_image = Image.fromarray(difference, 'RGBA')

    return result_image


def paste_shadow2(image):
    '''Вставляем вторую тень'''
    background = image.convert('RGB')
    overlay = Image.open('creation/res/shadow_twice.png')
    transparent_overlay = Image.new('RGBA', overlay.size)
    for x in range(overlay.width):
        for y in range(overlay.height):
            r, g, b, a = overlay.getpixel((x, y))
            transparent_overlay.putpixel((x, y), (r, g, b, int(a * 0.5)))

    background_width, background_height = background.size
    overlay_width, overlay_height = transparent_overlay.size
    position = ((background_width - overlay_width) // 2, (background_height - overlay_height) // 2)
    temp_background = Image.new('RGBA', background.size)
    temp_background.paste(background, (0, 0))
    temp_background.paste(transparent_overlay, position, transparent_overlay)

    return temp_background.convert('RGB')


def paste_shadow3(image):
    '''Вставляем третьюс тень'''
    background = image
    overlay = Image.open('creation/res/first_shadow.png')
    background_width, background_height = background.size
    overlay_width, overlay_height = overlay.size
    position = ((background_width - overlay_width) // 2, (background_height - overlay_height) // 2)
    background.paste(overlay, position, overlay)
    return background.convert('RGB')