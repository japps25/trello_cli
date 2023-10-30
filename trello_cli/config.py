"""Module to handle cli configurations"""

# local imports
from trello_cli import (
    SUCCESS, TRELLO_AUTHENTICATION_ERROR, OAUTH1_ERROR)
from trello_cli.models import GetOAuthTokenResponse

# third party imports
import os
from dotenv import find_dotenv, set_key, load_dotenv
from requests_oauthlib import OAuth1Session

# Trello API URLs
REQUEST_TOKEN_URL = 'https://trello.com/1/OAuthGetRequestToken'
AUTHORIZE_URL = 'https://trello.com/1/OAuthAuthorizeToken'
ACCESS_TOKEN_URL = 'https://trello.com/1/OAuthGetAccessToken'


def init() -> int:
    """
    Authenticates the user's Trello account and sets the necessary
    environment variables

    Returns
    -------
    status code: int
        representing the status of the authentication process
    """
    status = init_trello_api()
    if status != SUCCESS:
        return status

    auth_status = _load_oauth_token_env_var()
    if auth_status != SUCCESS:
        return auth_status
    return SUCCESS


def init_trello_api() -> int:
    """
    Initialization helper for checking if the user has set the necessary
    environment variables for the Trello API

    Returns
    -------
    status code: int
        representing the status of the authentication process
    """
    load_dotenv()
    if not os.getenv("TRELLO_API_TOKEN") and not os.getenv("TRELLO_API_SECRET"):
        print("Please visit https://trello.com/app-key to obtain your API key and secret.")
        return TRELLO_AUTHENTICATION_ERROR
    return SUCCESS


def _load_oauth_token_env_var() -> int:
    """
    Loads the user's oauth token into the environment variables if it
    is not already set

    Returns
    -------
    status code: int
        representing the status of the authentication process
    """
    # loads env variables for get_user_oauth_token()
    load_dotenv()
    if not os.getenv("TRELLO_OAUTH_TOKEN"):
        res = get_user_oauth_token()
        if res.status_code == SUCCESS:
            dotenv_path = find_dotenv()
            set_key(
                dotenv_path=dotenv_path,
                key_to_set="TRELLO_OAUTH_TOKEN",
                value_to_set=res.token
            )
            set_key(
                dotenv_path=dotenv_path,
                key_to_set="TRELLO_OAUTH_SECRET",
                value_to_set=res.secret
            )

        else:
            print("User denied access.")
            _load_oauth_token_env_var()

    load_dotenv()
    return SUCCESS


def get_user_oauth_token() -> GetOAuthTokenResponse:
    """Retrieves the user's oauth token

    Returns
    -------
    GetOAuthTokenResponse: namedtuple
        named typle containing the user's oauth access code and the status
    """
    try:
        res = create_oauth_token()
        return GetOAuthTokenResponse(
            token=res.token,
            secret=res.secret,
            status_code=SUCCESS
        )
    except (ValueError, KeyError):
        return GetOAuthTokenResponse(
            token="",
            secret="",
            status_code=OAUTH1_ERROR
        )


def create_oauth_token(verbose=False) -> dict:
    """
    Generates a pair of user-specific credentials to specify the Trello account
    that the requests are being made on behalf of. This is done via the OAuth1
    protocol.

    Code is adapted from py-trello oauth1 example.

    Authentication flow:
    1. Get a request token
    2. Redirect to the provider
    3. Provider asks the user to authenticate
    4. Request access token the user has approved

    Parameters
    ----------
    verbose: bool
        gives the user more information about the oauth process

    Returns
    -------
    access_token: dict
        dictionary containing the user's oauth token and secret
    """
    expiration = '30days'
    scope = 'read,write'
    trello_key = os.getenv("TRELLO_API_KEY")
    trello_secret = os.getenv("TRELLO_API_SECRET")
    name = 'trello_cli'

    # Step 1: Get a request token.
    session = OAuth1Session(client_key=trello_key, client_secret=trello_secret)
    response = session.fetch_request_token(REQUEST_TOKEN_URL)
    resource_owner_key, resource_owner_secret = response.get('oauth_token'), response.get('oauth_token_secret')

    if verbose:
        print("This is the Request Token :")
        print("    - oauth_token        = %s" % resource_owner_key)
        print("    - oauth_token_secret = %s" % resource_owner_secret)
        print("")

    # Step 2: Redirect to the provider.
    print("Go to the following link in your browser:")
    print("{authorize_url}?oauth_token={oauth_token}&scope={scope}&expiration={expiration}&name={name}".format(
        authorize_url=AUTHORIZE_URL,
        oauth_token=resource_owner_key,
        expiration=expiration,
        scope=scope,
        name=name
    ))

    input_func = input

    print("To proceed with authentication via Trello.com, follow the link above")
    oauth_verifier = input_func('What is the PIN? ')

    # step 4: Request access token the user has approved
    session = OAuth1Session(client_key=trello_key, client_secret=trello_secret,
                            resource_owner_key=resource_owner_key, resource_owner_secret=resource_owner_secret,
                            verifier=oauth_verifier)
    access_token = session.fetch_access_token(ACCESS_TOKEN_URL)

    if verbose:
        print("This is Access Token:")
        print("    - oauth_token        = %s" % access_token['oauth_token'])
        print("    - oauth_token_secret = %s" % access_token['oauth_token_secret'])
        print("")
        print("You may now access protected resources using the access tokens above.")
        print("")

    return access_token
