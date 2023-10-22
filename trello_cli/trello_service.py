""" This module contains the business logic needed to interact Trello API"""
from __future__ import annotations

# local imports
from trello_cli.trello_api import TrelloAPI
from trello_cli.models import *
from trello_cli.trello_data import Board, TrelloList, Card, Comment, Label
from trello_cli import (
    SUCCESS, TRELLO_READ_ERROR, TRELLO_WRITE_ERROR)

# standard library imports
import os


class TrelloService:
    """Class to handle responses from Trello API

    Attributes:
        __client: TrelloAPI object

    Methods:
        init_trello: populate the app with boards
        get_board: method to get a board from user's account
        get_list: method to get a list from a trello board
        get_card: method to get a card from a trello board
        create_card: method to create a card from a trello board
        create_comment: method to create a comment from a trello card
        add_card_label: method to add a label to a trello card
    """

    def __init__(self):
        self.__client = TrelloAPI(
            api_key=os.getenv("TRELLO_API_KEY"),
            api_secret=os.getenv("TRELLO_API_SECRET"),
            api_token=os.getenv("TRELLO_API_TOKEN"),
            oauth_token=os.getenv("TRELLO_OAUTH_TOKEN"),
            oauth_secret=os.getenv("TRELLO_OAUTH_SECRET")
        )

    def get_trello_boards(self) -> GetAllBoardsResponse:
        """
        Method to handle the get_all_boards response from Trello API

        Returns
        -------
        GetAllBoardsResponse : named tuple
            res: list of boards from the user's account
            status_code: status code of the response

        """
        try:
            response = self.__client.get_all_boards()
            boards = [Board.from_json(board) for board in response.json()]
            return GetAllBoardsResponse(
                res=boards,
                status_code=SUCCESS
            )
        except ValueError:
            return GetAllBoardsResponse(
                res=[],
                status_code=TRELLO_READ_ERROR
            )

    def get_board(self, board_id) -> GetBoardResponse:
        """
        Method to handle the get_board response from Trello API

        Parameters
        ----------
        board_id : str
            id of the board to be retrieved

        Returns
        -------
        GetBoardResponse : named tuple
            res: board from the user's account
            status_code: status code of the response

        """
        try:
            response = self.__client.get_board(board_id)
            board = Board.from_json(response.json())
            return GetBoardResponse(
                res=board,
                status_code=SUCCESS
            )
        except (ValueError, KeyError):
            return GetBoardResponse(
                res=None,
                status_code=TRELLO_READ_ERROR
            )


    def get_list(self, list_id) -> GetListResponse:
        """Method to hande the get_list response from Trello API

        Parameters
        ----------
        list_id : str
            id of the list to be retrieved

        Returns
        -------
        GetListResponse : named tuple
            res: list from the user's account
            status_code: status code of the response

        """
        try:
            response = self.__client.get_list(list_id)
            trello_list = TrelloList.from_json(response.json())
            return GetListResponse(
                res=trello_list,
                status_code=SUCCESS
            )
        except (ValueError, KeyError):
            return GetListResponse(
                res=None,
                status_code=TRELLO_READ_ERROR
            )

    def get_card(self, card_id) -> GetCardResponse:
        """Method to handle the get_card response from Trello API

        Parameters
        ----------
        card_id : str
            id of the card to be retrieved

        Returns
        -------
        GetCardResponse : named tuple
            res: card from the user's account
            status_code: status code of the response

        """
        try:
            response = self.__client.get_card(card_id)
            card = Card.from_json(response.json())
            return GetCardResponse(
                res=card,
                status_code=SUCCESS
            )
        except TypeError:
            return GetCardResponse(
                res=None,
                status_code=TRELLO_READ_ERROR
            )

    def create_card(self, name, list_id) -> CreateCardResponse:
        """ Method for handling the create_card response from Trello API

        Parameters
        ----------
        name : str
            name of the card to be created
        list_id : str
            id of the list where the card will be created

        Returns
        -------
        CreateCardResponse : named tuple
            res: card created
            status_code: status code of the response
        """
        try:
            json_response = self.__client.create_card(name, list_id)
            card = Card.from_json(json_response.json())
            return CreateCardResponse(
                res=card,
                status_code=SUCCESS
            )
        except (ValueError, KeyError):
            return CreateCardResponse(
                res=None,
                status_code=TRELLO_WRITE_ERROR
            )

    def create_comment(self, card_id, text) -> CreateCommentResponse:
        """ Method for handling the create_comment response from Trello API

        Parameters
        ----------
        card_id : str
            id of the card where the comment will be created
        text : str
            text of the comment to be created

        Returns
        -------
        CreateCommentResponse : named tuple
            res: comment created
            status_code: status code of the response
        """
        try:
            response = self.__client.create_comment(card_id, text)
            comment = Comment.from_json(response.json())
            return CreateCommentResponse(
                res=comment,
                status_code=SUCCESS
            )
        except ValueError:
            return CreateCommentResponse(
                res=None,
                status_code=TRELLO_WRITE_ERROR
            )

    def add_card_label(self, card_id, label_id) -> AddCardLabelResponse:
        """Method for handling the add_card_label response from Trello API

        Parameters
        ----------
        card_id : str
            id of the card where the label will be added
        label_id : str
            id of the label to be added

        Returns
        -------
        AddCardLabelResponse : named tuple
            res: label added
            status_code: status code of the response

        """
        try:
            response = self.__client.add_card_labels(card_id, label_id)
            label = Label.from_json(response.json())
            return AddCardLabelResponse(
                res=label,
                status_code=SUCCESS
            )
        except (ValueError, KeyError):
            return AddCardLabelResponse(
                res=None,
                status_code=TRELLO_WRITE_ERROR
            )
