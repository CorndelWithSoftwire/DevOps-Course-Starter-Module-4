from todo_app.flask_config import Config
from todo_app.data import trello_items as trello
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    items = trello.get_items()
    return render_template('index.html', items = items)


@app.route('/items/new', methods=['POST'])
def add_item():
    title = request.form['title']
    trello.add_item(title)
    return redirect(url_for('index'))


@app.route('/items/<id>/complete')
def complete_item(id):
    trello.complete_item(id)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
