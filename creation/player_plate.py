from creation import player1
from creation import player2
from creation import player3



def make_first_player(user_id, first_cadr_path, video_path):
    background = player1.make_background(user_id, first_cadr_path)
    player = player1.paste_video_and_player(user_id, background, video_path)
    return player

def make_second_player(user_id, video_path):
    background = player2.make_background_video(user_id, video_path)
    player = player2.paste_needle(user_id, background)
    return player

def make_third_player(user_id, first_cadr_path, video_path):
    background = player3.make_background(user_id, first_cadr_path)
    soft_light = player3.paste_soft_light(user_id, background)
    multiply = player3.paste_multiply(user_id, soft_light)
    screen = player3.paste_screen(user_id, multiply)
    normal = player3.paste_normal(user_id, screen)
    video = player3.paste_video(user_id, video_path, normal)
    player = player3.paste_needle(user_id, video)
    return player