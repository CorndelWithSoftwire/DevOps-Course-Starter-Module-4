import os
from unittest.mock import patch, Mock

import pytest

import app


@pytest.fixture
def client():
    os.environ['SECRET_KEY'] = 'secret'
    os.environ['TRELLO_BOARD_ID'] = 'abcd1234'
    os.environ['TRELLO_API_KEY'] = 'api_key'
    os.environ['TRELLO_API_SECRET'] = 'api_secret'

    test_app = app.create_app()
    test_app.config['TESTING'] = True

    with test_app.test_client() as client:
        yield client


@patch('requests.get')
def test_index_page_loads_tasks(mock_trello_request, client):
    mock_trello_request.return_value = Mock(ok=True)
    mock_trello_request.return_value.json.return_value = \
        [
            {
                "id": "5ede55964f947a716e858011",
                "name": "To Do",
                "cards": [
                    {
                        "id": "5ee100cac4bbbf5bd0350b3d",
                        "dateLastActivity": "2020-06-10T15:48:26.091Z",
                        "name": "My New Task"
                    }
                ]
            },
            {
                "id": "5ede55a73f8b9a79b0aee43e",
                "name": "Doing",
                "cards": []
            },
            {
                "id": "5ede55ad3db1df04ce28fb9b",
                "name": "Done",
                "cards": []
            }
        ]

    response = client.get('/')

    assert 'My New Task' in response.data.decode()
