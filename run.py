from config import Config
from test_task import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host=Config.FLASK_RUN_HOST, port=Config.FLASK_RUN_PORT)
