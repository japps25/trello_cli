import pytest
from trello_cli.trello_service import TrelloService
from trello_cli.trello_api import TrelloAPI
import os


@pytest.fixture(scope="session")
def trello_api():
    return TrelloAPI(
                api_key=os.getenv("TRELLO_API_KEY"),
                api_secret=os.getenv("TRELLO_API_SECRET"),
                api_token=os.getenv("TRELLO_API_TOKEN"),
                oauth_token=os.getenv("TRELLO_OAUTH_TOKEN"),
                oauth_secret=os.getenv("TRELLO_OAUTH_SECRET")
    )
