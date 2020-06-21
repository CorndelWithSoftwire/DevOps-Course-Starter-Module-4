from todo_item import Item
import requests
from flask import current_app as app


def get_auth_params():
    return {'key': app.config['TRELLO_API_KEY'], 'token': app.config['TRELLO_API_SECRET']}


def build_url(endpoint):
    return app.config['TRELLO_BASE_URL'] + endpoint


def build_params(params={}):
    full_params = get_auth_params()
    full_params.update(params)
    return full_params


def get_boards():
    """
    Fetches all boards from Trello.

    Returns:
        list: The list of Trello boards.
    """
    params = build_params()
    url = build_url('/members/me/boards')

    response = requests.get(url, params = params)
    boards = response.json()

    return boards


def get_board(name):
    """
    Fetches the board from Trello with the specified name.

    Args:
        name (str): The name of the list.

    Returns:
        board: The board, or None if no board matches the specified name.
    """
    boards = get_boards()
    return next((board for board in boards if board['name'] == name), None)


def get_lists():
    """
    Fetches all lists for the default Trello board.

    Returns:
        list: The list of Trello lists.
    """
    params = build_params({ 'cards': 'open' }) # Only return cards that have not been archived
    url = build_url('/boards/%s/lists' % app.config['TRELLO_BOARD_ID'])

    response = requests.get(url, params = params)
    lists = response.json()

    return lists


def get_list(name):
    """
    Fetches the list from Trello with the specified name.

    Args:
        name (str): The name of the list.

    Returns:
        list: The list and its items (cards), or None if no list matches the specified name.
    """
    lists = get_lists()
    return next((list for list in lists if list['name'] == name), None)


def get_items():
    """
    Fetches all items (known as "cards") from Trello.

    Returns:
        list: The list of saved items.
    """
    lists = get_lists()

    items = []
    for card_list in lists:
        for card in card_list['cards']:
            items.append(Item.fromTrelloCard(card, card_list))

    return items


def get_item(id):
    """
    Fetches the item ("card") with the specified ID.

    Args:
        id (str): The ID of the item.

    Returns:
        item: The item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item['id'] == id), None)


def add_item(name):
    """
    Adds a new item with the specified name as a Trello card.

    Args:
        name (str): The name of the item.

    Returns:
        item: The saved item.
    """
    todo_list = get_list('To Do')

    params = build_params({ 'name': name, 'idList': todo_list['id'] })
    url = build_url('/cards')

    response = requests.post(url, params = params)
    card = response.json()

    return Item.fromTrelloCard(card, todo_list)


def start_item(id):
    """
    Moves the item with the specified ID to the "Doing" list in Trello.

    Args:
        id (str): The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    doing_list = get_list('Doing')
    card = move_card_to_list(id, doing_list)

    return Item.fromTrelloCard(card, doing_list)


def complete_item(id):
    """
    Moves the item with the specified ID to the "Done" list in Trello.

    Args:
        id (str): The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    done_list = get_list('Done')
    card = move_card_to_list(id, done_list)

    return Item.fromTrelloCard(card, done_list)


def uncomplete_item(id):
    """
    Moves the item with the specified ID to the "To-Do" list in Trello.

    Args:
        id (str): The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    todo_list = get_list('To Do')
    card = move_card_to_list(id, todo_list)

    return Item.fromTrelloCard(card, todo_list)


def move_card_to_list(card_id, list):
    params = build_params({ 'idList': list['id'] })
    url = build_url('/cards/%s' % card_id)

    response = requests.put(url, params = params)
    card = response.json()

    return card
