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
    conn = psycopg2.connect(database="userss",
                        user="postgres",
                        password=password,
                        host="127.0.0.1",
                        port="5432")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                   user_id BIGINT, name TEXT);''')
    conn.commit()
    return conn

def init_info_db():
    conn = psycopg2.connect(database="info.db",
                        user="postgres",
                        password=password,
                        host="127.0.0.1",
                        port="5432")
    cursor = conn.cursor()
    cursor.execute("SET TIME ZONE 'Asia/Yekaterinburg';")
    cursor.execute('''CREATE TABLE IF NOT EXISTS info 
                      (key TEXT, info TEXT, date DATE DEFAULT CURRENT_DATE)''')
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
        with psycopg2.connect(database='userss',
                              user="postgres",
                                password=password,
                                host="127.0.0.1",
                                port="5432") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (user_id, name) VALUES (%s, %s)", (user_id, name,))
            conn.commit()
        return True
    except Exception as e:
        print(f"Ошибка БД: {e}")
        return False
    
def add_to_info_db(key, info, date):
    try:
        with psycopg2.connect(database="info.db",
                        user="postgres",
                        password=password,
                        host="127.0.0.1",
                        port="5432") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO info (key, info, date) VALUES (%s, %s, %s)", (key, info, date))
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
    with psycopg2.connect(database='userss',
                          user="postgres",
                        password=password,
                        host="127.0.0.1",
                        port="5432") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        conn.commit()
        return result[0] if result else None

    
def get_from_info_db(key):
    with psycopg2.connect(database="info.db",
                        user="postgres",
                        password=password,
                        host="127.0.0.1",
                        port="5432") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT info FROM info WHERE key = %s", (key,))
        result = cursor.fetchone()
        conn.commit()
        return result[0] if result else None
    
def get_all_from_info_db(date):
     with psycopg2.connect(database="info.db",
                        user="postgres",
                        password=password,
                        host="127.0.0.1",
                        port="5432") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM info WHERE date = %s", (date,))
        result = cursor.fetchone()
        conn.commit()
        return (result[0],[1]) if result else None
    
def delete_from_db(keyword):
    with psycopg2.connect('engineer.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM engineer WHERE keyword = %s", (keyword,))
        conn.commit()
        print(f"Записей удалено: {cursor.rowcount}")

def delete_from_user_db(user_id):
    with psycopg2.connect(database='userss',
                          user="postgres",
                        password=password,
                        host="127.0.0.1",
                        port="5432") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        conn.commit()

def user_to_check(user_id):
     with psycopg2.connect(database='userss',
                            user="postgres",
                            password=password,
                            host="localhost",
                            port="5432") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        conn.commit()
        return True if result else False