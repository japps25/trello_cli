# module imports
from trello_cli.trello_data import Board, List as TrelloList, Card, Comment, Label
from trello_cli.config import trello_api
# dependencies
from typing import List
from requests_oauthlib import OAuth1Session

trello_api = trello_api()


def get_all_boards() -> List[Board]:
    response = trello_api.get_all_boards()
    return [Board.from_json(board) for board in response]


def get_board(board_id: str) -> Board:
    response = trello_api.get_board(board_id)
    return Board.from_json(response)


def get_all_lists(board_id: str) -> List[TrelloList]:
    response = trello_api.get_all_lists(board_id)
    trello_lists = [TrelloList.from_json(trello_list) for trello_list in response]
    return trello_lists


def get_list(list_id: str) -> TrelloList:
    response = trello_api.get_list(list_id)
    trello_list = TrelloList.from_json(response)
    return trello_list


def create_card(name: str, list_id: str) -> Card:
    json_payload = trello_api.create_card(name, list_id)
    return Card.from_json(json_payload)


def get_all_cards(list_id: str) -> List[Card]:
    json_payload = trello_api.get_all_cards(list_id)
    cards = [Card.from_json(card) for card in json_payload]
    return cards


def get_card(card_id: str) -> Card:
    json_payload = trello_api.get_card(card_id)
    card = Card.from_json(json_payload)
    return card


def get_comments(card_id: str) -> List[Comment]:
    json_payload = trello_api.get_actions(card_id)
    comments = [Comment.from_json(comment) for comment in json_payload]
    return sorted(comments)


def create_comment(card_id: str, text: str) -> Comment:
    json_payload = trello_api.create_comment(card_id, text)
    comment = Comment.from_json(json_payload)
    return comment


def create_label(name: str, color: str, board_id: str) -> Label:
    json_payload = trello_api.create_label(name, board_id, color)
    label = Label.from_json(json_payload)
    return label


def get_labels(board_id: str) -> List[Label]:
    json_payload = trello_api.get_labels(board_id)
    labels = Label.from_json_list(json_payload)
    return labels


def add_card_label(card_id: str, label_id: str):
    trello_api.add_card_labels(card_id, label_id)


def create_oauth_token(key=None, secret=None, verbose=False):
    """
    Script to obtain an OAuth token from Trello.

    Must have TRELLO_API_KEY and TRELLO_API_SECRET set in your environment
    To set the token's expiration, set TRELLO_EXPIRATION as a string in your
    environment settings (eg. 'never'), otherwise it will default to 30 days.

    More info on token scope here:
        https://trello.com/docs/gettingstarted/#getting-a-token-from-a-user
    """
    request_token_url = 'https://trello.com/1/OAuthGetRequestToken'
    authorize_url = 'https://trello.com/1/OAuthAuthorizeToken'
    access_token_url = 'https://trello.com/1/OAuthGetAccessToken'

    expiration = '30days'
    scope = 'read,write'
    trello_key = api_key
    trello_secret = api_secret
    name = 'trello_cli'

    # Step 1: Get a request token. This is a temporary token that is used for
    # having the user authorize an access token and to sign the request to obtain
    # said access token.

    session = OAuth1Session(client_key=trello_key, client_secret=trello_secret)
    response = session.fetch_request_token(request_token_url)
    resource_owner_key, resource_owner_secret = response.get('oauth_token'), response.get('oauth_token_secret')

    if verbose:
        print("This is the Request Token :")
        print("    - oauth_token        = %s" % resource_owner_key)
        print("    - oauth_token_secret = %s" % resource_owner_secret)
        print("")

    # Step 2: Redirect to the provider. Since this is a CLI script we do not
    # redirect. In a web application you would redirect the user to the URL
    # below.

    print("Go to the following link in your browser:")
    print("{authorize_url}?oauth_token={oauth_token}&scope={scope}&expiration={expiration}&name={name}".format(
        authorize_url=authorize_url,
        oauth_token=resource_owner_key,
        expiration=expiration,
        scope=scope,
        name=name
    ))

    # After the user has granted access to you, the consumer, the provider will
    # redirect you to whatever URL you have told them to redirect to. You can
    # usually define this in the oauth_callback argument as well.

    # Python 3 compatibility (raw_input was renamed to input)
    input_func = input

    print("To proceed with authentication via Trello.com, follow the link")
    oauth_verifier = input_func('What is the PIN? ')

    # Step 3: Once the consumer has redirected the user back to the oauth_callback
    # URL you can request the access token the user has approved. You use the
    # request token to sign this request. After this is done you throw away the
    # request token and use the access token returned. You should store this
    # access token somewhere safe, like a database, for future use.
    session = OAuth1Session(client_key=trello_key, client_secret=trello_secret,
                            resource_owner_key=resource_owner_key, resource_owner_secret=resource_owner_secret,
                            verifier=oauth_verifier)
    access_token = session.fetch_access_token(access_token_url)

    if verbose:
        print("This is Access Token:")
        print("    - oauth_token        = %s" % access_token['oauth_token'])
        print("    - oauth_token_secret = %s" % access_token['oauth_token_secret'])
        print("")
        print("You may now access protected resources using the access tokens above.")
        print("")

    return access_token

# boards = get_all_boards()
#
# # [{'id': '6523e63b8e337f3ce55311a2', 'name': 'Design System Checklist'},
# #  {'id': '6523e5aa8c0d41e7537d7b2f', 'name': 'Kanban Template'},
# #  {'id': '6523e605b0d6b5829b5662e3', 'name': 'Remote Team Hub'}]
#
# board_id = '6523e63b8e337f3ce55311a2'
# lists = get_all_lists(board_id)
# print(lists)
