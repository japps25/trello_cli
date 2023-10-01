
#module improts

#dependency imports
from trello import Board, List as TrelloList, Label, Card 
#misc imports 
from typing import NamedTuple, List 

class GetOAuthTokenResponse(NamedTuple):
    """response from get_user_oauth_token"""
    token: str
    token_secret: str
    status_code: int

class GetAllBoardsResponse(NamedTuple):
    """stores response when retrieving all boards from trello.com

    Attributes:
        res (List[dict]) : list of boards
        status_code (int) : status code of response (success/error)
    
    """
    #res: List[dict]
    res : List[Board]
    status_code: int

class GetBoardResponse(NamedTuple):
    """response from get_board"""
    res: Board
    status_code: int

class GetAllListsResponse(NamedTuple):
    """response from get_all_lists"""
    res: List[TrelloList]
    status_code: int

class GetListResponse(NamedTuple):
    """response from get_list"""
    res: TrelloList
    status_code: int

class GetAllLabelsResponse(NamedTuple):
    """response from get_all_labels"""
    res: List[Label]
    status_code: int

class GetLabelResponse(NamedTuple):
    """response from get_label"""
    res: Label
    status_code: int


class AddCardResponse(NamedTuple):
    """response from add_card"""
    res: Card
    status_code: int

