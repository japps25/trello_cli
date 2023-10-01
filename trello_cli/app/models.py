"""regulates responses we're expecting in trelloservice""" 

#module improts

#dependency imports

#misc imports 
from typing import NamedTuple 

class GetOAuthTokenResponse(NamedTuple):
    """response from get_user_oauth_token"""
    token: str
    token_secret: str
    status_code: int

    