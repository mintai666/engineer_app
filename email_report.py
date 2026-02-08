import sqlite3, datetime, smtplib
from email.message import EmailMessage
from config import pw
import os

EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
msg = EmailMessage()

def send_email_report(report):
    file = open('email.txt', 'r')
    msg.set_content(report)
    msg['Subject'] = f'Отчет за {datetime.date.today()}'
    msg['From'] = "engineer.20026@gmail.com"
    msg['To'] = file.read()
    
    with open(report, 'rb') as f:
        file_data = f.read() # Считываем байты файла
        file_name = os.path.basename(report)
        msg.add_attachment(
        file_data,
        maintype='application',
        subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        filename=file_name)
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
        server.starttls() # Вот здесь происходит переход на защищенное соединение
        server.login("engineer.20026@gmail.com", pw)
        server.send_message(msg)
        server.quit()
        print("✅ Успешно отправлено через 587!")
        return True
    except Exception as e:
        print(f"❌ Порт 587 не сработал: {e}")
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 456) as smtp:
            smtp.login("engineer.20026@gmail.com", pw)
            smtp.send_message(msg)
    except Exception as e:
        print(e)
        print("Ошибка при отправке отчета.")