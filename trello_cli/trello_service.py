import os
from trello_cli.trello_api import TrelloAPI
from trello_cli.models import *
from trello_cli.trello_data import Board, TrelloList, Card, Comment, Label
from typing import List
from trello_cli import (
    SUCCESS, TRELLO_AUTHENTICATION_ERROR, OAUTH1_ERROR, TRELLO_READ_ERROR, TRELLO_WRITE_ERROR)


class TrelloService:
    """Class to implement the business logic needed to interact with Trello"""

    def __init__(self) -> None:
        self.__client = TrelloAPI(
            api_key=os.getenv("TRELLO_API_KEY"),
            api_token=os.getenv("TRELLO_API_TOKEN")
        )

    def init_trello(self) -> GetAllBoardsResponse:
        """populate the app with boards"""
        try:
            json_payload = self.__client.get_all_boards()
            boards = [Board.from_json(board) for board in json_payload]
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
        """method to get a board from user's account"""
        try:
            json_payload = self.__client.get_board(board_id)
            board = Board.from_json(json_payload)
            return GetBoardResponse(
                res=board,
                status_code=SUCCESS
            )
        except ValueError:
            return GetBoardResponse(
                res=None,
                status_code=TRELLO_READ_ERROR
            )

    def get_list(self, list_id) -> GetListResponse:
        """method to get a list from a trello board """
        try:
            json_payload = self.__client.get_list(list_id)
            trello_list = TrelloList.from_json(json_payload)
            return GetListResponse(
                res=trello_list,
                status_code=SUCCESS
            )
        except ValueError:
            return GetListResponse(
                res=None,
                status_code=TRELLO_READ_ERROR
            )


    def get_card(self, card_id) -> GetCardResponse:
        """method to get a card from a trello board """
        try:
            json_payload = self.__client.get_card(card_id)
            card = Card.from_json(json_payload)
            return GetCardResponse(
                res=card,
                status_code=SUCCESS
            )
        except ValueError:
            return GetCardResponse(
                res=None,
                status_code=TRELLO_READ_ERROR
            )

    def create_card(self, name, list_id) -> CreateCardResponse:
        """method to create a card from a trello board """
        try:
            json_payload = self.__client.create_card(name, list_id)
            card = Card.from_json(json_payload)
            return CreateCardResponse(
                res=card,
                status_code=SUCCESS
            )
        except ValueError:
            return CreateCardResponse(
                res=None,
                status_code=TRELLO_WRITE_ERROR
            )

    def create_comments(self, card_id, text) -> CreateCommentResponse:
        """method to create a comment from a trello card """
        try:
            json_payload = self.__client.create_comment(card_id, text)
            comment = Comment.from_json(json_payload)
            return CreateCommentResponse(
                res=comment,
                status_code=SUCCESS
            )
        except ValueError:
            return CreateCommentResponse(
                res=None,
                status_code=TRELLO_WRITE_ERROR
            )

