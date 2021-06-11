from flask import render_template, request, redirect, url_for, Blueprint

from todo_app.data import trello_items as trello
from todo_app.view_model import ViewModel

todo = Blueprint('todo', __name__)

@todo.route('/')
def index():
    items = trello.get_items()
    return render_template('index.html', model=ViewModel(items))

@todo.route('/items/new', methods=['POST'])
def add_item():
    name = request.form['name']
    trello.add_item(name)
    return redirect(url_for('todo.index'))

@todo.route('/items/<item_id>/start')
def start_item(item_id):
    trello.start_item(item_id)
    return redirect(url_for('todo.index'))

@todo.route('/items/<item_id>/complete')
def complete_item(item_id):
    trello.complete_item(item_id)
    return redirect(url_for('todo.index'))

@todo.route('/items/<item_id>/uncomplete')
def uncomplete_item(item_id):
    trello.uncomplete_item(item_id)
    return redirect(url_for('todo.index'))
