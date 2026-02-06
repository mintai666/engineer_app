from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

keyboard1 = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Настройки')],
    [KeyboardButton(text='Отчёт')],
    [KeyboardButton(text='Личный кабинет')],
    [KeyboardButton(text='Начать работу', web_app=WebAppInfo(url="https://mintai666.github.io/engineer_app/"))]
])

keyboard2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Настроить почту', callback_data='setting')],
    [InlineKeyboardButton(text='Поменять ФИО', callback_data='fio')],
    [InlineKeyboardButton(text='Задать время отправки', callback_data='timetoreport')]
])

keyboard3 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Профиль', callback_data='prof')]
])