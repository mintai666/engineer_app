# import subprocess
# try:
#     res = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
#     print("FFmpeg найден!")
# except FileNotFoundError:
#     print("Python НЕ ВИДИТ FFmpeg. Проверьте переменную PATH или укажите путь явно.")

# import os
# import shutil
# from faster_whisper import WhisperModel
# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context

# 1. Принудительная настройка путей для FFmpeg
# Укажи здесь путь к папке bin, которую ты создал
# ffmpeg_path = r"C:\engineer" 
# os.environ["PATH"] += os.pathsep + ffmpeg_path

# def check_env():
#     print("--- Проверка окружения ---")
#     ffmpeg = shutil.which("ffmpeg")
#     print(f"Путь к FFmpeg: {ffmpeg}")
    
#     # Проверка на кириллицу в пути (проблема с пользователем 'Полина')
#     model_root = "C:/whisper_cache" # Создадим папку в корне диска C
#     if not os.path.exists(model_root):
#         os.makedirs(model_root)
#     print(f"Папка для моделей: {model_root}")
#     return model_root

# def load_model(root):
#     print("\n--- Загрузка модели ---")
#     print("Попытка загрузить модель 'tiny' (самая легкая)...")
#     try:
#         # download_root переносит кэш из C:\Users\Полина\ в C:\whisper_cache
#         model = WhisperModel("tiny", device="cpu", compute_type="int8", download_root=root)
#         print("✅ Модель успешно загружена!")
#         return model
#     except Exception as e:
#         print(f"❌ Ошибка при загрузке модели: {e}")
#         return None

# if __name__ == "__main__":
#     root = check_env()
#     model = load_model(root)
#     if model:
#         print("\nВсе системы готовы к работе!")

# import os
# import whisper 

# # Используем обычные слеши, это надежнее в Python
# model_path = r"C:\engineer\models\model.bin"

# # Проверка для диагностики
# if not os.path.exists(model_path):
#     print(f"❌ ПАПКА НЕ СУЩЕСТВУЕТ: {model_path}")
# else:
#     files = os.listdir(model_path)
#     print(f"📁 Файлы в папке: {files}")
#     if "model.bin" not in files:
#         print("❌ ФАЙЛА model.bin НЕТ В ПАПКЕ!")

# try:
#     # Загружаем, указывая только ПУТЬ к папке
#     model = whisper.load_model(
#         model_path, 
#         device="cpu", 
#         compute_type="int8", 
#         local_files_only=True,
#         cpu_threads=1
#     )
#     print("✅ МОДЕЛЬ ЗАГРУЖЕНА УСПЕШНО")
# except Exception as e:
#     print(f"❌ ОШИБКА: {e}")

# def transcribe_voice(file_path):
#     segments, info = model.transcribe(file_path, beam_size=1)
#     text = " ".join([segment.text for segment in segments])
#     return text


import whisper
import os

# Путь к вашему файлу (замените имя файла на ваше)
# Используем r"" для путей Windows
model_file = r"C:\engineer\models\model.bin" 

if not os.path.exists(model_file):
    print("❌ Файл не найден!")
else:
    try:
        print("Загрузка модели... Это может занять минуту.")
        # Стандартный whisper умеет загружать модель напрямую из файла .bin/.pt
        model = whisper.load_model('small')
        print("✅ Ура! Модель загружена.")
        
        # Проверка
        # result = model.transcribe("audio.mp3")
        # print(result["text"])
    except Exception as e:
        print(f"❌ Ошибка загрузки: {e}")