from PIL import Image, ImageChops
import numpy as np



def open_image(image_path):
    return Image.open(image_path)

def bend_photo(img, coeff_depth, coeff_curvature):
    '''Делаем изгибы'''

    width, height = img.size

    print(width, height)
    # Создание массива для искривленного изображения
    data = np.array(img)

    #Параметры для искривления
    depth = -(int(height/coeff_depth))  # Глубина изгиба
    middle_x = (width // 2) + (width//400)
    middle_y = height // 2
    curvature = int(width/coeff_curvature)  # Ширина изгиба

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

def overlay_mask(image):
    '''Применяем маску'''
    image = image.resize((1506, 985))
    mask = Image.open('creation/res/mask1.png').convert("L")
    # Применение маски
    image.putalpha(mask)
    return image


def paste_photo(image):
    '''Вставляем на поверхность альбома'''
    background = Image.open('creation/res/main.png').convert('RGBA')
    vertical_offset = 951  # Смещение вниз
    horizontal_offset = 64  # Смещение вправо
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
    background_image = image
    overlay_image = Image.open('creation/res/soft_light.png')
    result_image = ImageChops.difference(background_image, overlay_image)
    return result_image.convert('RGB')

def paste_shadow2(image):
    '''Вставляем вторую тень'''
    background = image
    overlay = Image.open('creation/res/first_shadow.png')
    background_width, background_height = background.size
    overlay_width, overlay_height = overlay.size
    position = ((background_width - overlay_width) // 2, (background_height - overlay_height) // 2)
    background.paste(overlay, position, overlay)
    return background.convert('RGB')