from flask import Flask
from config import Config
from flask_migrate import Migrate

from test_task.cli_commands.cli_commands import cli_commands
from test_task.models import db
from test_task.products.views import products


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(cli_commands)
    app.register_blueprint(products)

    db.init_app(app)
    migrate = Migrate(compare_type=True)
    migrate.init_app(app, db)

    return app
