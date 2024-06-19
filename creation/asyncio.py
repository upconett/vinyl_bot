import asyncio, time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


from creation.classic_plate import make_first_plate_vinil, make_second_plate_vinil, make_third_plate_vinil
from creation.video_plate import make_first_plate_video, make_second_plate_video, make_third_plate_video
from creation.player_plate import make_first_player, make_second_player, make_third_player
from creation.album import make_first_album, make_second_album, make_third_album, make_forth_album


def get_unique_id():
    return int(time.time() * 1000000)


async def run(func, *args):
    """ Запускает асинхронное выполнение ресурсоёмких задач """
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, func, *args)
    return result


async def mega_run(func, *args):
    """ Запускает асинхронное выполнение ОЧЕНЬ ресурсоёмких задач """
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, func, *args)
    return result


async def make_classic_vinyl(unique_id: int, photo_path: str, audio_path: str, template: int, offset: str, speed: int, noise: bool) -> tuple[str, str]:
    match template:
        case 1: return await run(make_first_plate_vinil, unique_id, photo_path, audio_path, offset, speed, noise)
        case 2: return await run(make_second_plate_vinil, unique_id, photo_path, audio_path, offset, speed, noise)
        case 3: return await run(make_third_plate_vinil, unique_id, photo_path, audio_path, offset, speed, noise)


async def make_video_vinyl(unique_id: int, video_path: str, audio_path: str, template: int, offset: str, speed: int, noise: bool) -> tuple[str, str]:
    match template:
        case 1: return await run(make_first_plate_video, unique_id, video_path, audio_path, offset, speed, noise)
        case 2: return await run(make_second_plate_video, unique_id, video_path, audio_path, offset, speed, noise)
        case 3: return await run(make_third_plate_video, unique_id, video_path, audio_path, offset, speed, noise)


async def make_player_vinyl(unique_id: int, type: int) -> str:
    video_path = fr'creation/video/{unique_id}_output_video.mp4'
    first_cadr_path = fr'creation/img/{unique_id}_first_cadr.png'
    match type:
        case 1: return await run(make_first_player, unique_id, first_cadr_path, video_path)
        case 2: return await run(make_second_player, unique_id, video_path)
        case 3: return await run(make_third_player, unique_id, first_cadr_path, video_path)


async def make_album(unique_id: int, template: int, photo1: str, photo2: str = None) -> str:
    match template:
        case 1: return await mega_run(make_first_album, unique_id, photo1)
        case 2: return await mega_run(make_second_album, unique_id, photo1, photo2)
        case 3: return await mega_run(make_third_album, unique_id, photo1, photo2)
        case 4: return await mega_run(make_forth_album, unique_id, photo1, photo2)
