from flask import Flask, render_template

from todo_app.flask_config import Config
from todo_app.data import session_items as session

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    items = session.get_items()
    return render_template('index.html', items = items)


if __name__ == '__main__':
    app.run()
