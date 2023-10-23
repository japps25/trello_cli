"""Module for handling API responses from Trello API"""

# local imports
from trello_cli.trello_data import Board, TrelloList, Card, Comment, Label

# standard library imports
from typing import NamedTuple, List


class GetOAuthTokenResponse(NamedTuple):
    """Model to store response when retrieving user oauth tokens

    Attributes
        token (str): oauth token
        secret (str): oauth secret
        status_code (int): success / error
    """
    token: str
    secret: str
    status_code: int


class GetAllBoardsResponse(NamedTuple):
    """Model to store response when retrieving all boards

    Attributes
        res (List[Board]): array of boards
        status_code (int): success / error

    """
    res: List[Board]
    status_code: int


class GetBoardResponse(NamedTuple):
    """Model to store response when retrieving board

    Attributes
        res (Board): board
        status_code (int): success / error

    """
    res: Board
    status_code: int


class GetListResponse(NamedTuple):
    """Model to store response when retrieving a list

    Attributes
        res (TrelloList): list
        status_code (int): success / error

    """
    res: TrelloList
    status_code: int


class GetCardResponse(NamedTuple):
    """Model to store response when retrieving a card

    Attributes
        res (Card): card
        status_code (int): success / error

    """
    res: Card
    status_code: int


class CreateCardResponse(NamedTuple):
    """Model to store response when creating a comment

    Attributes
        res (Card): card
        status_code (int): success / error

    """
    res: Card
    status_code: int


class CreateCommentResponse(NamedTuple):
    """Model to store response when retrieving a comment from a card

    Attributes
        res (Comment): comment
        status_code (int): success / error

    """
    res: Comment
    status_code: int


class AddCardLabelResponse(NamedTuple):
    """Model to store response when adding a label to a card

    Attributes
        res (str): empty string
        status_code (int): success / error

    """
    res: str
    status_code: int
