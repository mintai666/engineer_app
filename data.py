import sqlite3
import datetime
NAME_PATTERN = r"[А-ЯЁ][а-яё]+(?:\s[А-ЯЁ]\.\s?[А-ЯЁ]\.|(?:\s[А-ЯЁ]\.\s?[А-ЯЁ]\.)?)|[А-ЯЁ]\.\s?[А-ЯЁ]\.\s[А-ЯЁ][а-яё]+"

def init_db():
    conn = sqlite3.connect('engineer.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS engineer 
                      (keyword TEXT, info TEXT, date TEXT)''')
    conn.commit()
    return conn

def init_user_db():
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user
                      (user_id TEXT, name TEXT)''')
    conn.commit()
    return conn

def add_to_db(keyword, info, date):
    try:
        with sqlite3.connect('engineer.db') as conn:
            cursor = conn.cursor()
            date = datetime.datetime.now().strftime('%Y-%m-%d')
            cursor.execute("INSERT INTO engineer VALUES (?, ?, ?)", (keyword, info, date,))
            conn.commit()
        return True
    except Exception as e:
        print(f"Ошибка БД: {e}")
        return False

def add_to_user_db(user_id, name):
    try:
        with sqlite3.connect('user.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user VALUES (?, ?)", (user_id, name))
            conn.commit()
        return True
    except Exception as e:
        print(f"Ошибка БД: {e}")
        return False

def get_from_db(keyword):
    with sqlite3.connect('engineer.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT info FROM engineer WHERE keyword LIKE ?", (keyword,))
        result = cursor.fetchone()
        conn.commit()
        return result[0] if result else None
    
def get_from_user_db(user_id):
    with sqlite3.connect('user.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM user WHERE user_id LIKE ?", (user_id,))
        result = cursor.fetchone()
        conn.commit()
        return result[0] if result else None
    
def delet_from_db(keyword):
    with sqlite3.connect('engineer.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM engineer WHERE keyword LIKE ?", (keyword,))
        conn.commit()
        print(f"Записей удалено: {cursor.rowcount}")

def delet_from_user_db(user_id):
    with sqlite3.connect('user.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user WHERE user_id LIKE ?", (user_id,))
        conn.commit()

def user_to_check(user_id):
     with sqlite3.connect('user.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM user WHERE user_id LIKE ?", (user_id,))
        result = cursor.fetchone()
        conn.commit()
        return True if result else False