""" Module for handling Trello API calls"""
from __future__ import annotations

# local imports
from trello_cli import SUCCESS, TRELLO_AUTHENTICATION_ERROR

# 3rd party imports
from requests_oauthlib import OAuth1
import requests
from dotenv import find_dotenv, set_key, load_dotenv

# standard library imports
from enum import Enum
import json
import os
import logging

# set logging
logging.basicConfig(level=logging.INFO)

#load environment vars
load_dotenv()

class RequestType(Enum):
    """Represents common HTTP request types as string"""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class TrelloAPI:
    """
    Class to make POST nad GET requests to Trello API

    Api token, key and secret/ OAuth token and secret are required
    to make API calls. These should be stored in .env file in the root
    directory of the package and configured during initialisation of the
    app which is found in trello_cli/config.py


    """

    def __init__ (self, api_key,api_secret,api_token,oauth_token,oauth_secret) -> None:
        """
        Initializes the TrelloAPI class for making requests to the Trello API

        In order to sign each API request, the user's API key, token and secret
        are required, as well as the oauth token and secret. These are passed in the
        authorization header of each request.


        Parameters
        ----------
        api_key: str
            trello API key ( a 32 character string)
         api_secret: str
            trello API secret (a 64 character string)
        api_token: str
            trello api token (a 64 character string)
        oauth_token: str
            trello oauth token (a 64 character string)
        oauth_secret: str
            trello oauth secret (a 64 character string)

        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.oauth_token = oauth_token
        self.oauth_secret = oauth_secret
        self.api_token = api_token

        # client key for oauth1 session
        if self.api_key and self.api_secret and self.oauth_token and self.oauth_secret:
            self.oauth = OAuth1(
                client_key=self.api_key,
                client_secret=self.api_secret,
                resource_owner_key=self.oauth_token,
                resource_owner_secret=self.oauth_secret)

        else:
            json.dumps({"ERROR": "Authorization Error, please check API & oauth keys/tokens"})
            self.oauth = None

        self.headers = {
            "Accept": "application/json"
        }
        self.base_url = "https://api.trello.com/1/"

    def call_api(self, request_type: str, endpoint: str,
                 payload: dict | str = None) -> str:
        """
        Makes a request to the Trello API

        Parameters
        ----------
        request_type: str
            type of request to make
        endpoint: str
            endpoint to make request to
        payload: dict | str
            payload to send with request

        Returns
        -------
        response: str
            json response from the API call
        """

        try:
            response = ""
            if request_type == "GET":
                response = requests.get(endpoint, timeout=30, headers=self.headers,
                                        params=payload, auth=self.oauth)
            elif request_type == "POST":
                response = requests.post(endpoint, self.headers, headers=self.headers, timeout=30,
                                         params=payload)
            if response.status_code in (200, 201):
                return response
            elif response.status_code == 401:
                return json.dumps({"ERROR": "Authorization Error. Please check API Key"})
            if response.status_code in (400, 403, 404):
                #these error codes are handled by trello_cli/trello_service.py
                return response
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            logging.error(errh)
        except requests.exceptions.ConnectionError as errc:
            logging.error(errc)
        except requests.exceptions.Timeout as errt:
            logging.error(errt)
        except requests.exceptions.RequestException as err:
            logging.error(err)

    def get_all_boards(self) -> str:
        """
        Request for retrieving all the User's boards from the Trello API

        Returns
        -------
        response: str
            response containing the User's trello boards

        """
        boards_url = f"{self.base_url}members/me/boards/?filter=all"

        response = self.call_api(request_type=RequestType.GET.value,
                                 endpoint=boards_url, payload={'fields': ['id', 'name']})

        return response

    def get_board(self, board_id: str) -> str:
        """
        Request for retrieving a specific board from the user's trello account

        Parameters
        ----------
        board_id: str
            id of the board to retrieve from the API

        Returns
        -------
        response: str
            response containing the User's trello board
        """
        board_url = f"{self.base_url}boards/{board_id}"
        if isinstance(board_id, str):
            response = self.call_api(request_type=RequestType.GET.value,
                                     endpoint=board_url, payload={'fields': ['id', 'name', 'labels']})

        else:
            raise ValueError("ERROR - Parameter 'board_id' should be of type str")
        return response

    def get_all_lists(self, board_id: str) -> str:
        """
        Request for retrieving all the lists from a given trello board

        Parameters
        ----------
        board_id: str
            id of the board to retrieve lists from

        Returns
        -------
        response: str
            response containing the lists from the given board
        """
        lists_url = f"{self.base_url}/boards/{board_id}/lists"
        if isinstance(board_id, str):
            response = self.call_api(request_type=RequestType.GET.value,
                                     endpoint=lists_url, payload={'fields': ['id', 'name']})
        else:
            raise ValueError("ERROR - Parameter board_id should be of type str")

        return response

    def get_list(self, list_id: str) -> str:
        """
        Request for retrieving a specific list from the user's trello account

        Parameters
        ----------
        list_id: str
            id of the list to retrieve from the API

        Returns
        -------
        response: str
            response containing the User's trello list
        """
        list_url = f"{self.base_url}/lists/{list_id}"

        if isinstance(list_id, str):
            response = self.call_api(request_type=RequestType.GET.value,
                                     endpoint=list_url)
        else:
            raise ValueError("ERROR - Parameter 'list_id' should be of type str")

        return response

    def create_card(self, name: str, id_list: str) -> str:
        """
        Request for creating a card in a given list

        Parameters
        ----------
        name: str
            name of the card to create
        id_list: str
            id of the list to create the card in

        Returns
        -------
        response: str
            response containing the created card
        """
        create_card_url = f"{self.base_url}/cards/"

        if isinstance(name, str) and isinstance(id_list, str):
            payload = {
                'name': name,
                'idList': id_list,
                'key': self.api_key,
                'token': self.api_token
            }
            response = self.call_api(request_type=RequestType.POST.value,
                                     endpoint=create_card_url,
                                     payload=payload)
        else:
            raise ValueError("ERROR - Parameters 'name' and 'list_id' should be of type str")

        return response

    def get_all_cards(self, list_id: str) -> str:
        """
        Request for retrieving all the cards from a given trello list

        Parameters
        ----------
        list_id: str
            id of the list to retrieve cards from

        Returns
        -------
        response: str
            response containing the cards from the given list
        """
        get_cards_url = f"{self.base_url}/lists/{list_id}/cards"

        if isinstance(list_id, str):
            payload = {'fields': ['id', 'name', 'labels', 'desc', 'badges']}
            response = self.call_api(request_type=RequestType.GET.value,
                                     endpoint=get_cards_url,
                                     payload=payload)
        else:
            raise ValueError("ERROR - Parameter 'list_id' should be of type str")
        return response

    def get_card(self, card_id: str) -> str:
        """
        Request for retrieving a specific card from the user's trello account

        Parameters
        ----------
        card_id: str
            id of the card to retrieve from the API

        Returns
        -------
        response: str
            response containing the User's trello card
        """
        get_card_url = f"{self.base_url}/cards/{card_id}"

        if isinstance(card_id, str):
            payload = {'fields': ['id', 'name', 'labels', 'desc', 'badges']}
            response = self.call_api(request_type=RequestType.GET.value,
                                     endpoint=get_card_url, payload=payload)
        else:
            raise ValueError("ERROR - Parameter 'card_id' should be of type str")
        return response

    def get_actions(self, card_id: str) -> str:
        """
        Request for retrieving all the actions from a given trello card.

        The actions are filtered so that only a commentCard action type
        is returned, containing the comment text and any metadata about the
        comment such as the author and date created.

        Parameters
        ----------
        card_id: str
            id of the card to retrieve actions from

        Returns
        -------
        response: str
            response containing the actions from the given card
        """

        get_actions_url = f"{self.base_url}/cards/{card_id}/actions"
        if isinstance(card_id, str):
            payload = {
                'filter': 'commentCard',
            }
            response = self.call_api(request_type=RequestType.GET.value,
                                     endpoint=get_actions_url, payload=payload)
        else:
            raise ValueError("ERROR - Parameter 'card_id' should be of type str")
        return response

    def create_comment(self, card_id: str, text: str) -> str:
        """
        Request for creating a comment on a given trello card

        Parameters
        ----------
        card_id: str
            id of the card to create the comment on
        text: str
            text of the comment to create

        Returns
        -------
        response: str
            response containing the created comment

        """
        create_comment_url = f"{self.base_url}/cards/{card_id}/actions/comments"

        if isinstance(card_id, str) and isinstance(text, str):
            payload = {
                'text': text,
                'key': self.api_key,
                'token': self.api_token,
            }
            response = self.call_api(request_type=RequestType.POST.value,
                                     endpoint=create_comment_url,
                                     payload=payload)
        else:
            raise ValueError("ERROR - Parameters 'card_id' and 'text' should be of type str")
        return response

    def create_label(self, name: str, color: str, board_id: str) -> str:
        """
        Request for creating a label on a given trello board

        Parameters
        ----------
        name: str
            name of the label to create
        color: str
            color of the label to create
        board_id: str
            id of the board to create the label on

        Returns
        -------
        response: str
            response containing the created label
        """
        create_label_url = f"{self.base_url}/labels"

        if isinstance(board_id, str) and isinstance(name, str) and isinstance(color, str):
            payload = {
                'name': name,
                'color': color,
                'idBoard': board_id,
                'key': self.api_key,
                'token': self.api_token,
            }
            response = self.call_api(request_type=RequestType.POST.value,
                                     endpoint=create_label_url,
                                     payload=payload)
        else:
            raise ValueError("ERROR - Parameters 'board_id', 'name' and 'color' should be of type str")
        return response

    def get_labels(self, board_id: str) -> str:
        """
        Request for retrieving all the labels from a given trello board

        Parameters
        ----------
        board_id: str
            id of the board to retrieve labels from

        Returns
        -------
        response: str
            response containing the labels from the given board
        """
        get_labels_url = f"{self.base_url}/boards/{board_id}/labels"

        if isinstance(board_id, str):
            payload = {
                'fields': ['id', 'name', 'color', 'idBoard', 'uses'],
            }
            response = self.call_api(request_type=RequestType.GET.value,
                                     endpoint=get_labels_url, payload=payload)
        else:
            raise ValueError("ERROR - Parameter 'board_id' should be of type str")
        return response

    def add_card_labels(self, card_id: str, label_id: str) -> str:
        """
        Request for adding a label to a given trello card

        Parameters
        ----------
        card_id: str
            id of the card to add the label to

        label_id: str
            id of the label to add to the card

        Returns
        -------
        response: str
            response containing the added label
        """
        add_card_label_url = f"{self.base_url}/cards/{card_id}/idLabels"

        if isinstance(card_id, str) and isinstance(label_id, str):

            payload = {
                'value': label_id,
                'key': self.api_key,
                'token': self.api_token,
            }
            response = self.call_api(request_type=RequestType.POST.value,
                                     endpoint=add_card_label_url,
                                     payload=payload)
        else:
            raise ValueError("ERROR - Parameters 'card_id' and 'label_id' should be of type str")
        return response

    def __repr__(self):
        return f"TrelloAPI[Oauth Token={self.oauth_token}, Oauth Secret={self.oauth_secret}]"
