import asyncio 
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
import utils
from aiogram.enums import ParseMode
import os
from aiogram.enums.content_type import ContentType
from aiogram.utils.keyboard import InlineKeyboardBuilder

from random import *
from handlers import *
import json

#подрубаем логгер чтобы руки не дрожали и инфа мутилась , лавэха крутилась 
logging.basicConfig(level = logging.INFO)

#создаём самого болта, через token И GetBotToken достаём из yaml сам токен
bot = Bot(token = utils.GetBotToken())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
