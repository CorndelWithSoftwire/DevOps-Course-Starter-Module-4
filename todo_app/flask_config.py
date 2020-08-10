import os


class Config:
    """Base configuration variables."""
    TRELLO_BASE_URL = 'https://api.trello.com/1'
    TRELLO_API_KEY = os.environ.get('TRELLO_API_KEY')
    TRELLO_API_SECRET = os.environ.get('TRELLO_API_SECRET')
    TRELLO_BOARD_ID = os.environ.get('TRELLO_BOARD_ID')
