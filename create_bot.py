from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from utility import config, logging
from utility.exceptions import NoConfigFile


try:
    data = config.read_data()

    token: str = data['token']

    logging.disable_aiogram()
    logging.set_format()
    logger = logging.get_logger(data['logfile'])
    

except NoConfigFile:
    print('No config.yaml in working directory!\nSee README.md!')
    quit()
except TypeError:
    print('Seems like config.yaml is invalid!\nSee README.md!')
    quit()


bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
