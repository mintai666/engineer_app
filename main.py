# from config import bot, dp, router
from aiogram import Bot, Dispatcher, Router
from data import init_db
from handlers import router
import os
from config import token

os.environ["PATH"] += os.pathsep + os.getcwd()

async def main():
    dp = Dispatcher()
    bot = Bot(token=token)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    dp.include_router(router=router)
    await dp.start_polling(bot)
    init_db()

async def startup():
    print('Включен')

async def shutdown():
    print('Выключен')