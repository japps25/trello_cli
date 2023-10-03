
#module imports 

#dependency imports
#from trello import Board, List as Column, Label, Card
from trello_cli.trello_utils import Board, List as Column, Label, Card

#misc imports 
from typing import NamedTuple, List 

class GetOAuthTokenResponse(NamedTuple):
    """response from get_user_oauth_token"""
    token: str
    token_secret: str
    status_code: int

class GetAllBoardsResponse(NamedTuple):
    """stores response when retrieving all boards

    Attributes:
        res (List[Board]) : list of boards
        status_code (int) : status code of response (success/error)
    
    """
    #res: List[dict]
    res : List[Board]
    status_code: int

class GetBoardResponse(NamedTuple):
    """stores response when retrieving a board
    
    Attributes:
        res (Board) : board
        status_code (int) : status code of response (success/error)

    """
    res: Board
    status_code: int

class GetAllListsResponse(NamedTuple):
    """stores response when retrieving all lists from a board
    
    Attributes:
        res (List[TrelloList]) : list of lists
        status_code (int) : status code of response (success/error)
    
    """
    res: List[Column]
    status_code: int

class GetListResponse(NamedTuple):
    """stores response when retrieving a list from a board
    
    Attributes:
        res (TrelloList) : list
        status_code (int) : status code of response (success/error)
    """
    res: Column
    status_code: int

class GetAllLabelsResponse(NamedTuple):
    """stores response when retrieving all labels
    
    Attributes:
        res (List[Label]) : list of labels
        status_code (int) : status code of response (success/error)
    """
    res: List[Label]
    status_code: int

class GetLabelResponse(NamedTuple):
    """stores response when retrieving a label 
    
    Attributes:
        res (Label) : label
        status_code (int) : status code of response (success/error)
    """
    res: Label
    status_code: int


class AddCardResponse(NamedTuple):
    """stores response when adding a card to a column
    
    Attributes:
        res (Card) : card
        status_code (int) : status code of response (success/error)
    
    """
    res: Card
    status_code: int

