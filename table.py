import openpyxl
from datetime import datetime

# Загружаем ваш шаблон
wb = openpyxl.load_workbook('Зака - наряд.xlsx')
sheet = wb.active

# Данные для заполнения
order_number = "2026-05"
customer = "Картоноделательная машина №2"
works = [
    ("Чистка вала", 1),
    ("Проверка затяжки болтов", 12),
    ("Замена смазки", 2)
]

# 1. Заполняем заголовок (Номер и Дата)
sheet['A4'] = f"ЗАКАЗ - ПАСПОРТ № ПР-{order_number} от {datetime.now().strftime('%d.%m.%Y')}"

# 2. Меняем заказчика
sheet['A6'] = f"Заказчик: {customer}"

# 3. Заполняем таблицу работ (начиная с 13 строки)
start_row = 13
for i, (name, qty) in enumerate(works):
    current_row = start_row + i
    sheet.cell(row=current_row, column=1).value = i + 1    # Номер п/п
    sheet.cell(row=current_row, column=2).value = name     # Наименование
    sheet.cell(row=current_row, column=12).value = qty    # Количество

# Сохраняем результат
wb.save('Готовый_Заказ_Наряд.xlsx')
print("Документ успешно заполнен!")