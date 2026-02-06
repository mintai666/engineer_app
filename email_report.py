import sqlite3, datetime, smtplib
from email.message import EmailMessage

EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
msg = EmailMessage()

def send_email_report():
    conn = sqlite3.connect('engineer.db')
    cursor = conn.cursor()
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    cursor.execute("SELECT keyword, info FROM engineer WHERE date = ?", (today,))
    rows = cursor.fetchall()

    flag = False
    
    if not rows:
        print("За сегодня записей нет.")
        return

    report = "Ежедневный отчет:\n" + "\n".join([f"{k}: {v}" for k, v in rows])
    file = open('email.txt', 'r')
    msg.set_content(report)
    msg['Subject'] = f'Отчет за {today}'
    msg['From'] = "engineer.20026@gmail.com"
    msg['To'] = file.read()
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("engineer.20026@gmail.com", "mtxm etrj nirl bxhx")
            smtp.send_message(msg)
            flag = True
            return flag
    except Exception as e:
        print("Ошибка при отправке отчета.")