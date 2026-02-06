import whisper
import os

os.environ["R_HOME"] = "C:/engineer"

def transcribe_voice(local_filename):
    print("Начинаю загрузку модели Whisper...")
    try:
        model = whisper.load_model('small', device="cpu")
        print("Модель успешно загружена!")
        segments = model.transcribe(local_filename, beam_size=5, fp16=False)

        return segments
    except Exception as e:
        print(f"КРИТИЧЕСКАЯ ОШИБКА ЗАГРУЗКИ МОДЕЛИ: {e}")