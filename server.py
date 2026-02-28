from flask import Flask, request
from werkzeug.utils import secure_filename
import os

def create_app(upload_folder):
    app = Flask(__name__)
    app.config['upload_folder'] = upload_folder
    os.makedirs(upload_folder, exist_ok=True)

    @app.route('/upload', methods=['POST'])
    def upload_file():
        if 'image' not in request.files:
            return "Нет файла", 400
        
        file = request.files['image']
        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_folder, filename))
        return f"Файл {filename} сохранен!", 200
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=5000)
