from aiogram.dispatcher.router import Router
from aiogram import F
from aiogram.types import *

from create_bot import logger
from keyboards import core as keyboards

from logic.core import *


router = Router(name='vinyl')