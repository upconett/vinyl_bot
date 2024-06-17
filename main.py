import asyncio

from create_bot import bot, dp, logger, cm
from routers import core, subscription, vinyl, album, admin

from creation.CreationManager import Vinyl, VinylTypes


async def onstartup():
    logger.info('Bot Online!')


async def onshutdown():
    logger.info('Goodbye...')


async def main():
    dp.startup.register(onstartup)
    dp.shutdown.register(onshutdown)

    dp.include_routers(
        core,
        subscription,
        vinyl,
        album,
        admin
    )

    asyncio.create_task(cm.startVinyl())
    asyncio.create_task(cm.startPlayer())

    # await cm.createVinyl(Vinyl(
    #     user_id=6626616767,
    #     unique_id=1718633817455313,
    #     template=1,
    #     type=VinylTypes.PHOTO,
    #     audio_path='creation/audio/audio.mp3',
    #     cover_path='creation/img/photo.jpeg',
    #     offset='00:00', speed=1, noise=False)
    # )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
