from flask import Flask

from todo_app.app_config import Config
from todo_app.routes import todo


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    app.register_blueprint(todo)
    return app

if __name__ == '__main__':
    create_app().run()
