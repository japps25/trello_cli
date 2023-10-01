"""Model class regulates the responses expected in trello_service""" 

#module improts

#dependency imports

#misc imports 
from typing import NamedTuple 

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
    res: List[dict]
    status_code: int

class GetBoardResponse(NamedTuple):
    """response from get_board"""
    res: dict
    status_code: int

class GetAllListsResponse(NamedTuple):
    """response from get_all_lists"""
    res: List[dict]
    status_code: int

class GetListResponse(NamedTuple):
    """response from get_list"""
    res: dict
    status_code: int

