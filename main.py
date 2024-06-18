import asyncio

from create_bot import bot, dp, logger, cm
from routers import core, subscription, vinyl, album, admin
from utility.scheduler import start_scheduler


async def onstartup(): logger.info('Bot Online!')


async def onshutdown(): logger.info('Goodbye...')


async def main():
    dp.startup.register(onstartup)
    dp.shutdown.register(onshutdown)

    dp.include_routers(
        admin,
        core,
        subscription,
        vinyl,
        album
    )

    asyncio.create_task(cm.startVinyl())
    asyncio.create_task(cm.startPlayer())

    start_scheduler()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
