from creation import album1
from creation import album2
from creation import album3
from creation import album4
import os


def make_first_album(unique_id, photo_path):
    image = album1.open_image(photo_path)
    temp_bended_photo = album1.bend_photo(image, 231, 99)
    bended_photo = album1.bend_photo(temp_bended_photo, 249, 330)
    mask_photo = album1.overlay_mask(bended_photo)
    photo_on_album = album1.paste_photo(mask_photo)
    photo_with_shadow = album1.paste_shadow(photo_on_album)
    photo_with_soft = album1.paste_shadow_soft(photo_with_shadow)
    photo_with_soft.save(f'creation/img/{unique_id}_result.png')
    os.remove(photo_path)
    return f'creation/img/{unique_id}_result.png'


def make_second_album(unique_id, left_photo_path, right_photo_path):
    image_left = album2.open_image(left_photo_path)
    image_right = album2.open_image(right_photo_path)
    main_image = album2.open_image('creation/res/main.png')
    temp_bended_image_left = album2.bend_photo(image_left, 231, 99)
    bended_image_left = album2.bend_photo(temp_bended_image_left, 249, 330)
    maks_image_left = album2.overlay_mask_left(bended_image_left)
    mask_image_right = album2.overlay_mask_right(image_right)
    paste_image_left = album2.paste_photo(maks_image_left, main_image, 952, 98)
    paste_image_right = album2.paste_photo(mask_image_right, paste_image_left, 1040, 895)

    photo_shadow = album2.paste_shadow3(paste_image_right)
    result_photo = album2.paste_shadow_soft(photo_shadow)
    result_photo.save(f'creation/img/{unique_id}_result.png')
    os.remove(left_photo_path)
    os.remove(right_photo_path)
    return f'creation/img/{unique_id}_result.png'

def make_third_album(unique_id, left_photo_path, right_photo_path):
    image_left = album3.open_image(left_photo_path)
    image_right = album3.open_image(right_photo_path)
    main_image = album3.open_image('creation/res/main.png')

    temp_bended_image_right = album3.bend_photo(image_right, 231, 99)
    bended_image_right = album3.bend_photo(temp_bended_image_right, 249, 330)

    maks_image_left = album3.overlay_mask_left(image_left)
    mask_image_right = album3.overlay_mask_right(bended_image_right)

    paste_image_left = album3.paste_photo(maks_image_left, main_image, 1040, 200)
    paste_image_right = album3.paste_photo(mask_image_right, paste_image_left, 952, 817)

    photo_shadow = album3.paste_shadow3(paste_image_right)
    result_photo = album3.paste_shadow_soft(photo_shadow)
    result_photo.save(f'creation/img/{unique_id}_result.png')
    os.remove(left_photo_path)
    os.remove(right_photo_path)
    return f'creation/img/{unique_id}_result.png'


def make_forth_album(unique_id, left_photo_path, right_photo_path):
    image_left = album4.open_image(left_photo_path)
    image_right = album4.open_image(right_photo_path)
    main_image = album4.open_image('creation/res/main.png')

    temp_bended_image_right = album4.bend_photo(image_right, 231, 99)
    bended_image_right = album4.bend_photo(temp_bended_image_right, 249, 330)

    maks_image_left = album4.overlay_mask(image_left)
    mask_image_right = album4.overlay_mask(bended_image_right)

    paste_image_left = album4.paste_photo(maks_image_left, main_image, 1040, 190)
    paste_image_right = album4.paste_photo(mask_image_right, paste_image_left, 1040, 905)

    photo_shadow = album4.paste_shadow3(paste_image_right)
    result_photo = album4.paste_shadow_soft(photo_shadow)
    result_photo.save('result.png')
    result_photo.save(f'creation/img/{unique_id}_result.png')
    os.remove(left_photo_path)
    os.remove(right_photo_path)
    return f'creation/img/{unique_id}_result.png'
