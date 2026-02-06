import os
import sys

# Принудительно задаем переменные, которые ищет ctypes
if sys.platform == 'win32':
    os.environ['PATH'] = r"C:\Windows\System32" + os.pathsep + os.environ.get('PATH', '')
    # Этот блок лечит баг Python 3.13 с поиском DLL
    if not hasattr(sys, 'frozen'):
        os.add_dll_directory(r"C:\Windows\System32")
import whisper
import torch

# Фикс для ошибки ctypes в Python 3.13
os.environ["PATH"] += os.pathsep + r"C:/engineer"

def transcribe_voice(file_path):
    print("Загрузка модели Whisper...")
    # Загружаем модель строго на CPU
    model = whisper.load_model("tiny", device="cpu")
    
    print("Начинаю расшифровку...")
    # fp16=False — критически важно для CPU-версии!
    result = model.transcribe(file_path, fp16=False)
    
    return result["text"]