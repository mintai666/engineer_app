import os
os.environ["NO_PROXY"] = "127.0.0.1,localhost"
import requests


try:
    response = requests.post(
        "http://[::1]:11434/api/generate",
        json={"model": "llama3", "prompt": "Привет!", "stream": False},
        timeout=30
    )
    print("Статус ответа:", response.status_code)
    print("Текст ответа:", response.json().get("response"))
except Exception as e:
    print("Ошибка соединения:", e)