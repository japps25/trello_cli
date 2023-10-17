import pytest
from trello_cli.trello_service import TrelloService
from trello_cli.trello_api import TrelloAPI
import os

@pytest.fixture(scope="session")
def trello_job():
    return TrelloService()


@pytest.fixture(scope="session")
def trello_api():
    return TrelloAPI(api_key=os.getenv("TRELLO_API_KEY"), api_token=os.getenv("TRELLO_API_TOKEN"))

