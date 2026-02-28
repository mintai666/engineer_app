import threading
from aiogram import Bot, Dispatcher
from data import init_db
from handlers import router
import os
from config import token, folder
from server import create_app


os.environ["PATH"] += os.pathsep + os.getcwd()

def run_flask():
    app = create_app(folder)
    print("--- Flask сервер запускается на http://127.0.0.1:5000 ---")
    # debug=True может конфликтовать с потоками, для начала ставим False
    app.run(port=5000, debug=False, use_reloader=False)

async def main():
    dp = Dispatcher()
    bot = Bot(token=token)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    dp.include_router(router=router)
    init_db()
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True # Поток умрет сам при выключении основного кода
    flask_thread.start()

    await dp.start_polling(bot)
    
async def startup():
    print('Включен')

async def shutdown():
    print('Выключен')