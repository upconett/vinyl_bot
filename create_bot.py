from creation.CreationManager import CreationManager
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from utility import config, logging
from utility.exceptions import NoConfigFile, NoResFolder


try:
    data = config.read_data()

    token: str = data['token']
    admins: list = data['admins']

    # logging.disable_aiogram()
    logging.set_format()
    logger = logging.get_logger(data['logdir'])

    dbfile = data['dbfile']

    cm = CreationManager()

except NoConfigFile:
    print('No config.yaml in working directory!\nSee README.md!')
    quit()
except TypeError:
    print('Seems like config.yaml is invalid!\nSee README.md!')
    quit()
except NoResFolder as e:
    print(e)
    quit()


bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
