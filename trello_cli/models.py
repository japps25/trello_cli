from typing import NamedTuple, List
from trello_cli.trello_data import Board, List as TrelloList, Card, Comment, Label


class GetOAuthTokenResponse(NamedTuple):
    """Model to store response when retrieving user oauth tokens
    Attributes
        token (str): user oauth token
        secret (str): user oauth token secret
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
        res (List[TrelloList]): array of lists
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
        res (Comment): comment
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

