import pytest
from trello_cli.trello_api import TrelloApi
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("TRELLO_API_KEY")
api_secret = os.getenv("TRELLO_API_SECRET")
oauth_token = os.getenv("TRELLO_OAUTH_TOKEN")
oauth_secret = os.getenv("TRELLO_OAUTH_KEY")


@pytest.fixture(scope="session")
def trello_api():
    """Create DogAPI object"""
    trello_api = TrelloApi(api_key, api_secret, oauth_token, oauth_secret)
    return trello_api
