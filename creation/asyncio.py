import asyncio
from concurrent.futures import ThreadPoolExecutor


from creation.classic_plate import make_first_plate_vinil, make_second_plate_vinil, make_third_plate_vinil
from creation.video_plate import make_first_plate_video, make_second_plate_video, make_third_plate_video
from creation.player_plate import make_first_player, make_second_player, make_third_player


async def run(func, *args):
    """ Запускает асинхронное выполнение ресурсоёмких задач """
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, func, *args)
    return result


async def make_classic_vinyl(user_id: int, photo_path: str, audio_path: str, template: int, offset: str, speed: int, noise: bool) -> tuple[str, str]:
    match template:
        case 1: return await run(make_first_plate_vinil, user_id, photo_path, audio_path, offset, speed, noise)
        case 2: return await run(make_second_plate_vinil, user_id, photo_path, audio_path, offset, speed, noise)
        case 3: return await run(make_third_plate_vinil, user_id, photo_path, audio_path, offset, speed, noise)


async def make_video_vinyl(user_id: int, video_path: str, audio_path: str, template: int, offset: str, speed: int, noise: bool) -> tuple[str, str]:
    match template:
        case 1: return await run(make_first_plate_video, user_id, video_path, audio_path, offset, speed, noise)
        case 2: return await run(make_second_plate_video, user_id, video_path, audio_path, offset, speed, noise)
        case 3: return await run(make_third_plate_video, user_id, video_path, audio_path, offset, speed, noise)


async def make_player_vinyl(user_id: int, unique_id: str, type: int) -> str:
    video_path = fr'creation/video/{user_id}_{unique_id}_output_video.mp4'
    first_cadr_path = fr'creation/img/{user_id}_{unique_id}_first_cadr.png'
    match type:
        case 1: return await run(make_first_player(user_id, first_cadr_path, video_path))
        case 2: return await run(make_second_player(user_id, first_cadr_path, video_path))
        case 3: return await run(make_third_player(user_id, first_cadr_path, video_path))
