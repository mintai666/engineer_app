from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

def app_url(user_id: int):
    app_url = f"https://mintai666.github.io/engineer_app/?user_id={user_id}"
    keyboard1 = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Настройки')],
    [KeyboardButton(text='Личный кабинет')],
    [KeyboardButton(text='Спросить эксперта')],
    [KeyboardButton(text='Начать работу', web_app=WebAppInfo(url=app_url))]
])
    return keyboard1

keyboard2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Настроить почту', callback_data='setting')],
    [InlineKeyboardButton(text='Поменять ФИО', callback_data='fio')],
    [InlineKeyboardButton(text='Задать время отправки', callback_data='timetoreport')]
])

keyboard3 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Профиль', callback_data='prof')]
])

keyboard4 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сформировать отчет', callback_data='form')]
])

keyboard44 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сформировать отчет', callback_data='form')],
    [InlineKeyboardButton(text='Сбросить', callback_data='clear')]
])

keyboard5 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отправить на почту', callback_data='send')],
    [InlineKeyboardButton(text='Посмотреть', callback_data='show')]
])

aikeyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Назад')]
]
)

# keyboard6 = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Добавить заметку', callback_data='add', switch_inline_query_current_chat='Запиши')],
#     [InlineKeyboardButton(text='Удалить заметку', callback_data='del')],
#     [InlineKeyboardButton(text='Посмотреть заметки', callback_data='shownotes')]
# ])

# keyboard7 = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Найти заметку', callback_data='find')],
#     [InlineKeyboardButton(text='Посмотреть все заметки за сегодня', callback_data='allnotes')]
# ])