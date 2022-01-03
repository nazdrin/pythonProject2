
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import os

storage = MemoryStorage()
bot = Bot('2007585933:AAHWk-Z9fq8Fa5iyojR500w5_vurQ5Qxz5Q')
dp = Dispatcher(bot, storage=storage)
id_admin = -474594767
