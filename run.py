import asyncio
from main import main
from server import create_app
from config import folder

app = create_app(folder)

if __name__ == '__main__':
    try:
        asyncio.run(main())
        print("Сервер запускается...")
        app.run(debug=True, port=5000)
    except KeyboardInterrupt:
        pass