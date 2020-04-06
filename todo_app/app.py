from flask import Flask, render_template, redirect, url_for, request

from todo_app.flask_config import Config
from todo_app.data import session_items as session

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    items = session.get_items()
    return render_template('index.html', items = items)


@app.route('/items/new', methods=['POST'])
def add_item():
    title = request.form['title']
    session.add_item(title)
    return redirect(url_for('index'))


@app.route('/items/<id>/complete')
def complete_item(id):
    session.complete_item(id)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
