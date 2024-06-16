from yoomoney import Client
from creation.CreationManager import CreationManager
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from utility import config, logging
from utility.exceptions import NoConfigFile


try:
    data = config.read_data()

    token: str = data['token']
    admins: list = data['admins']
    bot_url: str = data['bot_url']

    # logging.disable_aiogram()
    logging.set_format()
    logger = logging.get_logger(data['logfile'])

    dbfile = data['dbfile']

    yoomoney_token: str = data['yoomoney_token']
    yoomoney_client = Client(yoomoney_token)
    yoomoney_info = yoomoney_client.account_info()

    cm = CreationManager()


except NoConfigFile:
    print('No config.yaml in working directory!\nSee README.md!')
    quit()
except TypeError:
    print('Seems like config.yaml is invalid!\nSee README.md!')
    quit()


bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
