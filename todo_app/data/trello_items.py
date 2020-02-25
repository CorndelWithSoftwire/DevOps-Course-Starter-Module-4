import requests
from todo_app import trello_config as config

TRELLO_BASE_URL = 'https://api.trello.com/1'

def get_auth_params():
    return { 'key': config.TRELLO_API_KEY, 'token': config.TRELLO_API_SECRET }


def get_board():
    params = get_auth_params()
    path = '/members/me/boards'

    response = requests.get(TRELLO_BASE_URL + path, params = params)
    boards = response.json()

    return boards[-3]


def get_lists():
    board = get_board()
    board_id = board['id']

    params = get_auth_params()
    params.update({ 'cards': 'open' }) # Only return cards that have not been archived
    path = '/boards/' + board_id + '/lists'

    response = requests.get(TRELLO_BASE_URL + path, params = params)
    lists = response.json()
    return lists


def create_item_from_card(card, list):
    return { 'id': card['id'], 'title': card['name'], 'status': list['name'] }


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
            item = create_item_from_card(card, card_list)
            items.append(item)

    return items


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


def add_item(title):
    """
    Adds a new item with the specified title as a Trello card.

    Args:
        title (str): The title of the item.

    Returns:
        item: The saved item.
    """
    todo_list = get_list('To Do')

    params = get_auth_params()
    params.update({ 'name': title, 'idList': todo_list['id'] })
    path = '/cards'

    response = requests.post(TRELLO_BASE_URL + path, params = params)
    card = response.json()

    return create_item_from_card(card, todo_list)


def complete_item(id):
    """
    Moves the item with the specified ID to the "Done" list in Trello.

    Args:
        id (str): The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    done_list = get_list('Done')

    params = get_auth_params()
    params.update({ 'idList': done_list['id'] })
    path = '/cards/' + id

    response = requests.put(TRELLO_BASE_URL + path, params = params)
    card = response.json()

    return create_item_from_card(card, done_list)


def uncomplete_item(id):
    """
    Moves the item with the specified ID to the "To-Do" list in Trello.

    Args:
        id (str): The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    todo_list = get_list('To Do')

    params = get_auth_params()
    params.update({ 'idList': todo_list['id'] })
    path = '/cards/' + id

    response = requests.put(TRELLO_BASE_URL + path, params = params)
    card = response.json()

    return create_item_from_card(card, todo_list)
