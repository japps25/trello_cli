import pytest
from trello_cli.trello_api import TrelloApi
import os

api_key = os.getenv("TRELLO_API_KEY")
api_secret = os.getenv("TRELLO_API_SECRET")
oauth_token = os.getenv("TRELLO_OAUTH_TOKEN")
oauth_secret = os.getenv("TRELLO_OAUTH_SECRET")
api_token = os.getenv("TRELLO_API_TOKEN")


def trello_api():
    """Create TrelloAPI object"""
    return TrelloApi(api_key, api_token, api_secret, oauth_token, oauth_secret)


