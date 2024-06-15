from creation import player1
from creation import player2
from creation import player3
import datetime


def time_count(func):
    def wrapper(*args, **kwargs):
        time_start = datetime.datetime.now()
        print(f'Запускаю {func}')
        result = func(*args, **kwargs)
        print(f'Закончил {func} за {datetime.datetime.now() - time_start}')
        print('________________________\n')
        return result

    return wrapper

@time_count
def make_first_player(user_id, first_cadr_path, video_path):
    background = player1.make_background(user_id, first_cadr_path)
    player = player1.paste_video_and_player(user_id, background, video_path)
    return player

@time_count
def make_second_player(user_id, video_path):
    background = player2.make_background_video(user_id, video_path)
    player = player2.paste_needle(user_id, background)
    return player

@time_count
def make_third_player(user_id, first_cadr_path, video_path):
    background = player3.make_background(user_id, first_cadr_path)
    soft_light = player3.paste_soft_light(user_id, background)
    multiply = player3.paste_multiply(user_id, soft_light)
    screen = player3.paste_screen(user_id, multiply)
    normal = player3.paste_normal(user_id, screen)
    video = player3.paste_video(user_id, video_path, normal)
    player = player3.paste_needle(user_id, video)
    return player

#make_first_player(1, 'creation/img/1_first_cadr.png', 'creation/video/1_output_video.mp4')
#20 сек в среднем
# make_second_player(1, 'creation/video/1_output_video.mp4')
#40 сек
#make_third_player(1, 'creation/img/1_first_cadr.png', 'creation/video/1_output_video.mp4')
#1 мин