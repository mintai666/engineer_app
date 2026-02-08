import openpyxl
from datetime import datetime
import os
from data import get_from_db
import glob

def create(user_id):
    file_path = None
    data = get_from_db(user_id)['payload']
    print(data)
    if not data:
        return None
    if isinstance(data, dict):
        try:
            wb = openpyxl.load_workbook('Заказ - наряд.xlsx')
        except FileNotFoundError:
            print("Ошибка: Не найден файл шаблона 'Заказ - наряд.xlsx'")
            return None
            
        ws = wb.active
        start_row = 14

        for row in range(start_row, 200):
            cell_name = ws.cell(row=row, column=2).value
                
            if not cell_name:
                continue

            work_name = str(cell_name).strip()

            if work_name in data:
                value = data[work_name]
            
                quantity = 0
                if value is True:
                    quantity = 1
                elif value is False:
                    quantity = 0
                elif isinstance(value, (int, float)):
                    quantity = value
                
                if quantity > 0:
                    ws.cell(row=row, column=12).value = quantity
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"Order_{user_id}_{timestamp}.xlsx"
                os.makedirs(r"c:\engineer\reports", exist_ok=True)
                file_path = os.path.join('reports', filename)
            wb.save(file_path)
        return file_path
    
def find_file(user_id):
    search_pattern = f"c:/engineer/reports/Order_{user_id}_*.xlsx"
    print(f"Ищу файлы по пути: {search_pattern}")
    files = glob.glob(search_pattern)
    
    if not files:
        return None
    last_file = max(files, key=os.path.getmtime)
    
    return last_file