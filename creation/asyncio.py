import asyncio
from concurrent.futures import ThreadPoolExecutor


from creation.classic_plate import make_first_plate_vinil, make_second_plate_vinil
from creation.video_plate import make_first_plate_video, make_second_plate_video


async def run(func, *args):
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, func, *args)
    return result


async def make_classic_vinyl(user_id: int, photo_path: str, audio_path: str, offset: str, speed: int, noise: bool):
    return await run(make_first_plate_vinil, user_id, photo_path, audio_path, offset, speed, noise)

async def make_video_vinyl(user_id: int, video_path: str, audio_path: str, offset: str, speed: int, noise: bool):
    return await run(make_first_plate_video, user_id, video_path, audio_path, offset, speed, noise)
