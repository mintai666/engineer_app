import os
os.environ["NO_PROXY"] = "127.0.0.1,localhost"
import threading
from aiogram import Bot, Dispatcher
from data import init_db, init_db_vk
from handlers import router
from config import token, folder
from server import create_app
from vk_bot import run_vk
import asyncio

os.environ["PATH"] += os.pathsep + os.getcwd()

def run_flask():
    app = create_app(folder)
    print("--- Flask сервер запускается на http://127.0.0.1:5000 ---")
    # debug=True может конфликтовать с потоками, для начала ставим False
    app.run(port=5000, host='127.0.0.1', debug=False, use_reloader=False)

async def main():
    dp = Dispatcher()
    bot = Bot(token=token)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    dp.include_router(router=router)
    init_db()
    init_db_vk()
    await asyncio.gather(
        dp.start_polling(bot),  
        run_vk()                
    )
    
async def startup():
    print('Включен')

async def shutdown():
    print('Выключен')