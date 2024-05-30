import asyncio, os

from create_bot import bot, dp
from routers import private


async def onstartup():
    print('Bot Online!')


async def onshutdown():
    print('Goodbye...')


async def main():
    dp.startup.register(onstartup)
    dp.shutdown.register(onshutdown)

    dp.include_routers(private)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
