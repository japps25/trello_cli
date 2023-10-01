# module imports
from trello_cli import TRELLO_READ_ERROR, TRELLO_WRITE_ERROR, SUCCESS
from trello_cli.models import *

# dependencies imports
from trello import TrelloClient, create_oauth_token


# misc imports
import os

class TrelloService:
    """class to interact with trello.com api"""

    def __init__(self) -> None:
        pass

    def get_user_oauth_token() -> GetOAuthTokenResponse:
        pass 

    def get_all_boards() -> GetAllBoardsResponse:
        pass

    def get_board() -> GetBoardResponse:
        pass

    def get_all_lists() -> GetAllListsResponse:
        pass

    def get_list() -> GetListResponse:
        pass

    def get_all_labels() -> GetAllLabelsResponse:
        pass

    def get_label() -> GetLabelResponse:
        pass

    def add_card() -> AddCardResponse:
        pass

    



