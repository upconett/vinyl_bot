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
    mask = Image.open('creation/res/mask3_al.png').convert("L")
    img_ratio = image.width / image.height
    mask_ratio = mask.width / mask.height

    if img_ratio > mask_ratio:
        scale = mask.height / image.height
        new_width = int(image.width * scale)
        new_height = mask.height
    else:
        scale = mask.width / image.width
        new_width = mask.width
        new_height = int(image.height * scale)

    resized_img = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    if resized_img.width > mask.width or resized_img.height > mask.height:
        x_left = (resized_img.width - mask.width) // 2
        y_top = (resized_img.height - mask.height) // 2
        resized_img = resized_img.crop((x_left, y_top, x_left + mask.width, y_top + mask.height))
    resized_mask = mask.resize((resized_img.width, resized_img.height), Image.Resampling.LANCZOS)
    resized_img.putalpha(resized_mask)
    # Применение маски
    resized_img.putalpha(mask)
    return resized_img


def overlay_mask_left(image):
    '''Применяем маску для левого фото'''
    mask = Image.open('creation/res/mask5.png').convert("L")
    img_ratio = image.width / image.height
    mask_ratio = mask.width / mask.height

    if img_ratio > mask_ratio:
        scale = mask.height / image.height
        new_width = int(image.width * scale)
        new_height = mask.height
    else:
        scale = mask.width / image.width
        new_width = mask.width
        new_height = int(image.height * scale)

    resized_img = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    if resized_img.width > mask.width or resized_img.height > mask.height:
        x_left = (resized_img.width - mask.width) // 2
        y_top = (resized_img.height - mask.height) // 2
        resized_img = resized_img.crop((x_left, y_top, x_left + mask.width, y_top + mask.height))
    resized_mask = mask.resize((resized_img.width, resized_img.height), Image.Resampling.LANCZOS)
    resized_img.putalpha(resized_mask)
    # Применение маски
    resized_img.putalpha(mask)
    return resized_img


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


def paste_shadow_soft(image):
    '''Вставляем одну день методом soft light'''
    background_image = image
    overlay_image = Image.open('creation/res/soft_light.png')
    width, height = overlay_image.size
    result = Image.new('RGBA', background_image.size)
    result.paste(background_image, (0, 0))

    for x in range(width):
        for y in range(height):

            bp = background_image.getpixel((x, y))
            op = overlay_image.getpixel((x, y))
            alpha_factor = op[3] / 255

            # Нормализуем значения RGB до 0-1
            br, bg, bb, ba = [v / 255 for v in bp]
            or_, og, ob, _ = [v / 255 for v in op]

            # Применяем формулу soft light
            new_r = (or_ * br + br ** 2 * (1 - 2 * or_)) if br < 0.5 else (
                        br ** 0.5 * (2 * or_ - 1) + 2 * br * (1 - or_))
            new_g = (og * bg + bg ** 2 * (1 - 2 * og)) if bg < 0.5 else (bg ** 0.5 * (2 * og - 1) + 2 * bg * (1 - og))
            new_b = (ob * bb + bb ** 2 * (1 - 2 * ob)) if bb < 0.5 else (bb ** 0.5 * (2 * ob - 1) + 2 * bb * (1 - ob))

            # Возвращаем значения в диапазон 0-255
            new_r = int(new_r * 255 * alpha_factor + br * 255 * (1 - alpha_factor))
            new_g = int(new_g * 255 * alpha_factor + bg * 255 * (1 - alpha_factor))
            new_b = int(new_b * 255 * alpha_factor + bb * 255 * (1 - alpha_factor))

            result.putpixel((x, y), (new_r, new_g, new_b, int(ba * 255)))
    return result.convert('RGB')


def paste_shadow3(image):
    '''Вставляем третью тень'''
    background = image
    overlay = Image.open('creation/res/first_shadow.png')
    background_width, background_height = background.size
    overlay_width, overlay_height = overlay.size
    position = ((background_width - overlay_width) // 2, (background_height - overlay_height) // 2)
    background.paste(overlay, position, overlay)
    return background