import psycopg2.extras
import sqlite3
import datetime
from config import password
NAME_PATTERN = r"[А-ЯЁ][а-яё]+(?:\s[А-ЯЁ]\.\s?[А-ЯЁ]\.|(?:\s[А-ЯЁ]\.\s?[А-ЯЁ]\.)?)|[А-ЯЁ]\.\s?[А-ЯЁ]\.\s[А-ЯЁ][а-яё]+"

def init_db():
    conn = psycopg2.connect(database="engineer.db",
                        user="postgres",
                        password=password,
                        host="localhost",
                        port="5432")
    cursor = conn.cursor()
    cursor.execute("SET TIME ZONE 'Asia/Yekaterinburg';")
    cursor.execute('''CREATE TABLE IF NOT EXISTS engineer (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT,
                    payload JSONB,
                    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
''')
    conn.commit()
    return conn

def init_user_db():
    conn = sqlite3.connect(database="user.db",
                        user="postgres",
                        password=password,
                        host="127.0.0.1",
                        port="5432")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user
                      (user_id TEXT, name TEXT)''')
    conn.commit()
    return conn

def init_info_db():
    conn = psycopg2.connect(database="info.db",
                        user="postgres",
                        password=password,
                        host="127.0.0.1",
                        port="5432")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS info 
                      (key TEXT, info TEXT)''')
    conn.commit()
    return conn

def add_to_db(user_id, payload):
    try:
        with psycopg2.connect(database="engineer.db",
                        user="postgres",
                        password=password,
                        host="localhost",
                        port="5432") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO engineer (user_id, payload) VALUES (%s, %s)",
            (user_id, payload))
            conn.commit()
        return True
    except Exception as e:
        print(f"Ошибка БД: {e}")
        return False

def add_to_user_db(user_id, name):
    try:
        with sqlite3.connect('user.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user VALUES (?, ?)", (user_id, name,))
            conn.commit()
        return True
    except Exception as e:
        print(f"Ошибка БД: {e}")
        return False
    
def add_to_info_db(key, info):
    try:
        with psycopg2.connect(database="info.db",
                        user="postgres",
                        password=password,
                        host="127.0.0.1",
                        port="5432") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO info VALUES (?, ?, ?)", (key, info,))
            conn.commit()
        return True
    except Exception as e:
        print(f"Ошибка БД: {e}")
        return False

def get_from_db(user_id):
    with psycopg2.connect(database="engineer.db",
                        user="postgres",
                        password=password,
                        host="127.0.0.1",
                        port="5432") as conn:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT payload FROM engineer WHERE user_id = %s ORDER BY time DESC LIMIT 1", (user_id,))
        result = cursor.fetchone()
        conn.commit()
        return result if result else None
    
def get_from_user_db(user_id):
    with sqlite3.connect('user.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM user WHERE user_id LIKE ?", (user_id,))
        result = cursor.fetchone()
        conn.commit()
        return result[0] if result else None
    
def get_from_info_db(key):
    with sqlite3.connect(database="info.db",
                        user="postgres",
                        password=password,
                        host="127.0.0.1",
                        port="5432") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT info FROM info WHERE key = %s", (key,))
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