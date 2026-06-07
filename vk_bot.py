import os
import logging
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from data import init_user_db_vk, user_to_check_vk
from keyboards import kbvk, kbvk_main
from vkbottle.bot import Bot, Message
from config import vk_token, vk_id

# TOKEN = os.getenv(vk_token, vk_id)
bot_vk = Bot(token=vk_token)

logging.basicConfig(level=logging.INFO)

async def run_vk():
    await bot_vk.run_polling()
    print("Бот ВК стартовал и слушает сервер...")


@bot_vk.on.private_message(text=["/start", "Начать"])
async def start_handler(message: Message):
    init_user_db_vk()
    if user_to_check_vk(message.from_id):
        await message.answer(message='Добро пожаловать!', keyboard=kbvk_main, relize_keyboard=True)
    else:
        await message.answer(message='Добро пожаловать! Пройдите регистрацию', keyboard=kbvk, relize_keyboard=True)

@bot_vk.on.private_message(text="Регистрация")
async def help_handler(message: Message):
    await message.answer("Здесь могла быть ваша инструкция по использованию бота.")


# 3. Пример инлайн-клавиатуры (кнопки внутри сообщения)
@bot_vk.on.private_message(text="Инлайн-меню")
async def inline_handler(message: Message):
    inline_keyboard = (
        Keyboard(inline=True)
        .add(Text("Кнопка 1", payload={"cmd": "btn1"}), color=KeyboardButtonColor.PRIMARY)
        .add(Text("Кнопка 2", payload={"cmd": "btn2"}), color=KeyboardButtonColor.NEGATIVE)
    ).get_json()

    await message.answer("Это пример инлайн-кнопок:", keyboard=inline_keyboard)


# 4. Обработка нажатий на инлайн-кнопки (через payload)
@bot_vk.on.private_message(payload={"cmd": "btn1"})
async def inline_btn1_handler(message: Message):
    await message.answer("Вы нажали первую инлайн-кнопку!")


# 5. Хендлер для отправки картинок (В ВК это делается через Uploader)
@bot_vk.on.private_message(text="Отправь фото")
async def send_photo(message: Message):
    await message.answer("Загружаю фото, подождите...")
    
    # Загружаем фото на серверы ВК (можно передать путь к файлу или bytes)
    # path_to_file = "image.png"
    # attachment = await bot.uploader.upload_message_photo(path_to_file)
    
    # Для теста отправим просто текст, если файла нет
    await message.answer("Фото успешно отправлено! (Раскомментируйте код выше для работы с файлами)")


# 6. Эхо-хендлер (ловит любые сообщения, которые не подошли под правила выше)
# ВАЖНО: этот хендлер должен быть самым последним в коде!
@bot_vk.on.private_message()
async def echo_handler(message: Message):
    await message.answer(f"Вы написали: {message.text}\nЯ пока не знаю такой команды.")
