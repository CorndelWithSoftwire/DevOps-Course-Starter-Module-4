"""Flask configuration class."""
import os


class Config:

    def __init__(self):
        self.TRELLO_BASE_URL = 'https://api.trello.com/1'
        self.TRELLO_API_KEY = os.environ.get('TRELLO_API_KEY')
        self.TRELLO_API_SECRET = os.environ.get('TRELLO_API_SECRET')
        self.TRELLO_BOARD_ID = os.environ.get('TRELLO_BOARD_ID')
