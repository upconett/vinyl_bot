import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from utility import config
from utility.exceptions import NoConfigFile


try:
    data = config.read_data()

    token: str = data['token']

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler(filename=data['logfile'], encoding='utf-8')
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s | %(message)s",
        datefmt="%d.%m.%y [%H:%M:%S]"
    )
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

except NoConfigFile:
    print('No config.yaml in working directory!\nSee README.md!')
    quit()
except TypeError:
    print('Seems like config.yaml is invalid!\nSee README.md!')
    quit()


bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
