import pytest
from trello_cli.trello_api import TrelloApi
import os


@pytest.fixture(scope="session")
def trello_api():
    """Create TrelloAPI object"""
    return TrelloApi(api_key=os.getenv("TRELLO_API_KEY"), api_token=os.getenv("TRELLO_API_TOKEN"))


