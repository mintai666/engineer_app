from aiogram import types, Router, F
from aiogram.types import FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, MagicData
from aiogram.enums import ChatAction
import asyncio
import os
from table import create, find_file
from data import (add_to_db, init_db, get_from_db, init_user_db, add_to_user_db, delet_from_db, user_to_check, get_from_user_db, 
                 delet_from_user_db, init_info_db, add_to_info_db, get_from_info_db)
import datetime
from email_report import send_email_report, EMAIL_PATTERN
from voice import transcribe_voice
from keyboards import keyboard1 as kb1, keyboard2 as kb2, keyboard3 as kb3, keyboard4 as kb4, keyboard5 as kb5
import json
from aiogram.types import WebAppInfo

router = Router()


class Base(StatesGroup):
    wait_name = State()
    wait_new_name = State()
    wait_time = State()

@router.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    await message.bot.send_chat_action(chat_id=message.from_user.id, action=ChatAction.TYPING)
    await asyncio.sleep(1)
    await message.answer(text='Добро пожаловать!', reply_markup=kb1, relize_keyboard=True)

@router.message(F.content_type == "web_app_data")
async def handle_web_app_data(message: types.Message):
    raw_data = message.web_app_data.data
    # data = json.loads(raw_data)
    init_db()
    add_to_db(message.from_user.id, raw_data)
    print(f"Получены чекбоксы: {raw_data}")
    await message.answer(f"Данные получены!", reply_markup=kb4)

@router.callback_query(F.data == ('form'))
async def generate_order(callback: types.CallbackQuery):
    await callback.message.answer('Формирование...')
    create(callback.from_user.id)
    await callback.message.answer(text='Отчет сформирован!', reply_markup=kb5)
    
@router.callback_query(F.data == ('show'))
async def show(callback: types.CallbackQuery):
    try:
        excel_file = find_file(callback.from_user.id)
        document = types.FSInputFile(path=excel_file)
        await callback.message.answer_document(document, caption="✅")
    except Exception as e:
        await callback.message.answer(f"⚠️ Произошла ошибка: {e}")

@router.callback_query(F.data == ('send'))
async def send(callback: types.CallbackQuery):
    excel_file = find_file(callback.from_user.id)
    send_email_report(excel_file)
    await callback.message.answer(text='Отчет отправлен на почту')

@router.message(F.text.lower().startswith('запиши'))
async def write(message: types.Message):
    init_info_db()
    data = message.text.replace("запиши", "").strip() if 'запиши'in message.text else message.text.replace("Запиши", "").strip()
    if " это " in data:
        key, val = data.split(" это ", 1)
        add_to_info_db(key.strip(), val.strip())
        await message.answer(text=f"Я сохранил информацию о {key}")
        print(f"Я сохранил информацию о {key}")
    else:
        print("Скажите, например: запиши рецепт это мука и яйца")

# python -m run 

@router.message(F.text.lower().startswith('найди'))
async def read(message: types.Message):
    data = message.text.replace('найди', "").strip() if 'найди' in message.text else message.text.replace('Найди', "").strip()
    await message.answer(get_from_info_db(data))

# @router.message(F.text.lower().startswith('удали'))
# async def read(message: types.Message):
#     data = message.text.replace("удали", "").strip() if 'удали' in message.text else message.text.replace("Удали", "").strip()
#     delet_from_info_db(data)
#     await message.answer(text=f'Информация о {data} удалена')

@router.message(F.text.startswith('Отчёт'))
async def report(message: types.Message):
    try:
        send_email_report()
        # if flag == False:
        #     await message.answer(text='За сегодня записей нет')
        # else:
        await message.answer(text='Отчет отправлен на почту')
    except Exception as e:
        await message.answer(text='Ошибка отправки')
        print(f"Ошибка отправки: {e}")
        return False

@router.message(F.text.startswith('Настройки'))
async def setting(message: types.Message):
    await message.answer(text='Что хотите сделать?', reply_markup=kb2)

@router.callback_query(F.data == ('fio'))
async def fio(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Base.wait_new_name)
    await callback.message.answer(text='Введите новое ФИО в формате "Иванов И.И."')

@router.message(Base.wait_new_name)
async def new_name(message: types.Message, state: FSMContext):
    delet_from_user_db(message.from_user.id)
    add_to_user_db(message.from_user.id, message.text)
    await message.answer(text='ФИО изменено')
    await state.clear()

@router.message(F.text.startswith('Личный кабинет'))
async def personal(message: types.Message, state: FSMContext):
    if user_to_check(message.from_user.id):
        file = open('email.txt', 'r')
        await message.answer(text=f'Ваш профиль:\n'
                            f'user id: {message.from_user.id}\n'
                            f'ФИО: {get_from_user_db(message.from_user.id)}\n'
                            f'Почта для отправки: {file.read()}')
    else:
        await state.set_state(Base.wait_name)
        await message.answer(text='Отправьте ФИО в формате "Иванов И.И."')

@router.message(Base.wait_name)
async def user_id_and_name(message: types.Message, state: FSMContext):
    init_user_db()
    add_to_user_db(message.from_user.id, message.text)
    await message.answer(text='Регистрация прошла успешно', reply_markup=kb3)
    await state.clear()

@router.message(F.data == ('prof'))
async def profile(callback: types.CallbackQuery):
    file = open('email.txt', 'r')
    await callback.message.answer(text=f'Ваш профиль:\n'
                                f'user id: {callback.from_user.id}\n'
                                f'ФИО: {get_from_user_db(callback.from_user.id)}\n'
                                f'Почта для отправки: {file.read()}')

@router.callback_query(F.data == ('timetoreport'))
async def change_time(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Base.wait_time)
    await callback.message.answer(text='Введите время, в которое ежедневно будет отправляться отчет в формате "часы:минуты"')

@router.message(Base.wait_time)
async def handler_time(message: types.Message, state: FSMContext):
    file = open('time.txt', 'w')
    file.write(message.text)
    await message.answer(text=f'Теперь отчеты будут отправляться каждый день в {message.text}')
    await state.clear()

@router.callback_query(F.data == ('setting'))
async def change_email(callback: types.CallbackQuery):
    await callback.message.answer(text='Введите адрес электронной почты, на который будут поступать отчёты')

@router.message(F.text.regexp(EMAIL_PATTERN))
async def handler_email(message: types.Message):
    try:
        file = open('email.txt', 'w')
        file.write(message.text)
        await message.answer(text=f'Теперь отчеты будут отправляться на адрес {message.text}')
    except Exception as e:
        await message.answer(text=f"Ошибка: {e}")

@router.message(F.voice)
async def audio_to_text(message: types.Message):
    status = await message.answer(text='Распознаю вашу речь...')
    try:
        file_id = message.voice.file_id
        file = await message.bot.get_file(file_id)
        file_path = file.file_path
        local_filename = f"c:\engineer\downloads\{file_id}.ogg"
        os.makedirs("c:\engineer\downloads", exist_ok=True)
        await message.bot.download_file(file_path, local_filename)
        text = transcribe_voice(local_filename)
        if text:
            print(text.get("text"))
            await status.edit_text(text.get("text"))
        else:
            await status.edit_text("Не удалось разобрать слова. Попробуйте сказать четче.")

    except Exception as e:
        import traceback
        error_details = traceback.format_exc() 
        print(f"Ошибка: {error_details}")
        await status.edit_text(f"Произошла ошибка при обработке аудио: {e}")
    finally:
        if os.path.exists(local_filename):
            os.remove(local_filename)