"""Pytest configuration file for unit tests."""

# local imports
from trello_cli.trello_api import TrelloAPI

# standard library imports
import os

# Third party imports
import pytest


@pytest.fixture(scope="session")
def trello_api():
    """
    Fixture to create a TrelloAPI object for testing.
    """
    return TrelloAPI(
        api_key=os.getenv("TRELLO_API_KEY"),
        api_secret=os.getenv("TRELLO_API_SECRET"),
        api_token=os.getenv("TRELLO_API_TOKEN"),
        oauth_token=os.getenv("TRELLO_OAUTH_TOKEN"),
        oauth_secret=os.getenv("TRELLO_OAUTH_SECRET")
    )
