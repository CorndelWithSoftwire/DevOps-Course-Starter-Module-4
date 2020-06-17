import os
from unittest.mock import patch, Mock

import pytest

import app


class TrelloConfig:
    TRELLO_BASE_URL = 'https://api.trello.com/1'
    TRELLO_API_KEY = 'api_key'
    TRELLO_API_SECRET = 'api_secret'
    TRELLO_BOARD_ID = 'abcd1234'


@pytest.fixture
def client():
    os.environ['SECRET_KEY'] = 'secret'

    test_app = app.create_app()
    test_app.config['TESTING'] = True

    with test_app.test_client() as client:
        yield client


@patch('trello_items.config', new=TrelloConfig())
@patch('requests.get')
def test_index_page(mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_lists

    response = client.get('/')

    response_html = response.data.decode()
    assert 'My Next Task' in response_html
    assert 'My In Progress Task' in response_html
    assert 'My Completed Task' in response_html


@patch('trello_items.config', new=TrelloConfig())
@patch('requests.get')
@patch('requests.post')
def test_add_item(mock_post_request, mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_lists
    mock_post_request.return_value.json.return_value = sample_trello_card
    form_data = dict(name='My new task')

    response = client.post('/items/new', data=form_data)

    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/'
    mock_post_request.assert_called_once_with(
        'https://api.trello.com/1/cards',
        params={"key": "api_key", "token": "api_secret", "name": "My new task", "idList": TODO_LIST_ID}
    )


@patch('trello_items.config', new=TrelloConfig())
@patch('requests.get')
@patch('requests.put')
def test_start_item(mock_put_request, mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_lists
    mock_put_request.return_value.json.return_value = sample_trello_card

    response = client.get(f'/items/{TODO_ITEM_ID}/start')

    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/'
    mock_put_request.assert_called_once_with(
        f'https://api.trello.com/1/cards/{TODO_ITEM_ID}',
        params={"key": "api_key", "token": "api_secret", "idList": DOING_LIST_ID}
    )


@patch('trello_items.config', new=TrelloConfig())
@patch('requests.get')
@patch('requests.put')
def test_complete_item(mock_put_request, mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_lists
    mock_put_request.return_value.json.return_value = sample_trello_card

    response = client.get(f'/items/{DOING_ITEM_ID}/complete')

    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/'
    mock_put_request.assert_called_once_with(
        f'https://api.trello.com/1/cards/{DOING_ITEM_ID}',
        params={"key": "api_key", "token": "api_secret", "idList": DONE_LIST_ID}
    )


@patch('trello_items.config', new=TrelloConfig())
@patch('requests.get')
@patch('requests.put')
def test_uncomplete_item(mock_put_request, mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_lists
    mock_put_request.return_value.json.return_value = sample_trello_card

    response = client.get(f'/items/{DONE_ITEM_ID}/uncomplete')

    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/'
    mock_put_request.assert_called_once_with(
        f'https://api.trello.com/1/cards/{DONE_ITEM_ID}',
        params={"key": "api_key", "token": "api_secret", "idList": TODO_LIST_ID}
    )


TODO_LIST_ID = "5ede55964f947a716e858011"
DOING_LIST_ID = "5ede55a73f8b9a79b0aee43e"
DONE_LIST_ID = "5ede55ad3db1df04ce28fb9b"

TODO_ITEM_ID = "5ee100cac4bbbf5bd0350b3d"
DOING_ITEM_ID = "5ee100cac4bbbf5bd0350b3e"
DONE_ITEM_ID = "5ee100cac4bbbf5bd0350b3f"

sample_trello_lists_response = [
    {
        "id": TODO_LIST_ID,
        "name": "To Do",
        "cards": [
            {
                "id": TODO_ITEM_ID,
                "dateLastActivity": "2020-06-10T15:48:26.091Z",
                "name": "My Next Task"
            }
        ]
    },
    {
        "id": DOING_LIST_ID,
        "name": "Doing",
        "cards": [
            {
                "id": DOING_ITEM_ID,
                "dateLastActivity": "2020-06-10T15:48:26.091Z",
                "name": "My In Progress Task"
            }
        ]
    },
    {
        "id": DONE_LIST_ID,
        "name": "Done",
        "cards": [
            {
                "id": DONE_ITEM_ID,
                "dateLastActivity": "2020-06-10T15:48:26.091Z",
                "name": "My Completed Task"
            }
        ]
    }
]


sample_trello_card = {
    "id": TODO_ITEM_ID,
    "dateLastActivity": "2020-06-10T15:48:26.091Z",
    "name": "My Next Task"
}


def mock_get_lists(url, params):
    if url == 'https://api.trello.com/1/boards/abcd1234/lists':
        response = Mock(ok=True)
        response.json.return_value = sample_trello_lists_response
        return response

    return None
