# module imports
from trello_cli import TRELLO_READ_ERROR, TRELLO_WRITE_ERROR, SUCCESS, TRELLO_AUTHORIZATION_ERROR
from trello_cli.models import *
from trello_cli.trello_authenticate import create_oauth_token
# dependency imports
from dotenv import load_dotenv, find_dotenv, set_key
from trello_cli.trello_client import TrelloClient
# misc imports
import os
import json
import requests


class TrelloService:
    """class to interact with trello.com api"""

    def __init__(self) -> None:
        self.__load_oauth_token_env_var()

        self.__client = TrelloClient(
            api_key=os.getenv("TRELLO_API_KEY"),
            api_secret=os.getenv("TRELLO_API_SECRET"),
            token=os.getenv("TRELLO_OAUTH_TOKEN"),
            #token_secret=os.getenv("TRELLO_OAUTH_SECRET")
        )

    def __load_oauth_token_env_var(self) -> None:
        """stores oauth token as an environment variable"""
        load_dotenv()
        if not os.getenv("TRELLO_OAUTH_TOKEN"):
            res = self.get_user_oauth_token()
            if res.status_code == SUCCESS:
                dotenv_path = find_dotenv()
                set_key(
                    dotenv_path = dotenv_path,
                    key_to_set= "TRELLO_OAUTH_TOKEN",
                    value_to_set= res.token
            )
            else:
                print("User denied access")
                self.__load_oauth_token_env_var()
        
    def get_user_oauth_token(self) -> GetOAuthTokenResponse:
        """Method to retrieve user's oauth token 
        
        Returns 
            GetOAuthTokenResponse: user's oauth token 

        """
        try:
            res = create_oauth_token()
            return GetOAuthTokenResponse(
                token=res["oauth_token"],
                token_secret=res["oauth_token_secret"],
                status_code=SUCCESS
            )   
        except:
            return GetOAuthTokenResponse(
                token="",
                token_secret="",
                status_code=TRELLO_AUTHORIZATION_ERROR
            )

#-------------------- HELPERS --------------------

    def get_all_boards(self) -> GetAllBoardsResponse:
        """
        List's all boards from user's accounts 
        """

        try:
            res = self.__client.list_boards()
            return GetAllBoardsResponse(
                res=res,
                status_code=SUCCESS
            )
        except:
            return GetAllBoardsResponse(
                res=[],
                status_code=TRELLO_READ_ERROR
            )

    def get_board(self, board_id: str) -> GetBoardResponse:
        """
        Retrieves a board from user's account

        Required args: board_id (str): board_id 

        Returns: GetBoardResponse: board
    
        """
        try:
            res = self.__client.get_board(board_id=board_id)
            return GetBoardResponse(
                res=res,
                status_code=SUCCESS
            )
        
        except:
            return GetBoardResponse(
                res=None,
                status_code=TRELLO_READ_ERROR
            )
        
    def get_all_lists(self, board: Board) -> GetAllListsResponse:
        """
        Method to list all lists (columns) from the trello board 

        Required Args 
            board (Board): trello board

        Returns
            GetAllListsResponse: list of lists

        """
        try:
            res = board.all_lists()
            return GetAllListsResponse(
                res= board.all_lists(),
                status_code=SUCCESS
            )
        except:
            return GetAllListsResponse(
                res=[],
                status_code=TRELLO_READ_ERROR
            )
    

    def get_list(self, board:Board, list_id: str) -> GetListResponse:

        """
        Method to retireve list(column) from the trello board

        Required args: board (Board) 
        list_id (str) : list_id

        Returns: 
        GetListResponse: trello list 
        
        """

        try:
            res = Board.get_list(list_id=list_id)
            return GetListResponse(
                res=res,
                status_code=SUCCESS
            )
        
        except:
            return GetListResponse(
                res=None,
                status_code=TRELLO_READ_ERROR
            )


    def get_all_labels(self, board: Board) -> GetAllLabelsResponse:
        """
        Method to list all labels from the trello board

        Required args:
            board (Board): trello board

        Returns:
            GetAllLabelsResponse: list of labels

        """

        try:
            res = board.get_labels()
            return GetAllLabelsResponse(
                res=res,
                status_code=SUCCESS
            )
        
        except:
            return GetAllLabelsResponse(
                res=None,
                status_code=TRELLO_READ_ERROR
            )
        
    def get_label(self, board: Board, label_id: str) -> GetLabelResponse:
        """
        Method to retrieve a label from the trello board

        Required args:
            board (Board): trello board
            label_id (str): label_id

        Returns:
            GetLabelResponse: trello label

        """

        try:
            res = board.get_label(label_id=label_id)
            return GetLabelResponse(
                res=res,
                status_code=SUCCESS
            )
        
        except:
            return GetLabelResponse(
                res=None,
                status_code=TRELLO_READ_ERROR
            )
        
    def add_card(self, col: Column, name: str) -> AddCardResponse:
        """
        Method to add a card to the trello board

        Required args:
            list (TrelloList): trello list
            name (str): name of card
  

        Returns:
            AddCardResponse: trello card

        """

        try:
            new_Card = col.add_card(name = name)
          
            return AddCardResponse(
                res=new_Card,
                status_code=SUCCESS
            )
        
        except:
            return AddCardResponse(
                res=None,
                status_code=TRELLO_WRITE_ERROR
            )