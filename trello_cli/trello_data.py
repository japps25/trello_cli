"""Module for representing trello data"""

# local imports
from trello_cli.models import *
from trello_cli.trello_api import TrelloAPI

# standard library imports
import os


class TrelloBase(object):
    """
    Base class for trello objects

    Attributes
        client (TrelloAPI): TrelloAPI object
            fetches attributes for trello objects from the trello api
    """

    def __init__(self):
        self.client = TrelloAPI(
            api_key=os.getenv("TRELLO_API_KEY"),
            api_secret=os.getenv("TRELLO_API_SECRET"),
            api_token=os.getenv("TRELLO_API_TOKEN"),
            oauth_token=os.getenv("TRELLO_OAUTH_TOKEN"),
            oauth_secret=os.getenv("TRELLO_OAUTH_SECRET"))


class Comment(TrelloBase):
    """A class used to represent a trello comment object

    Attributes
    ----------
        comment_id: str
            id for a comment object
        data: str
            comment text
        member_creator: str
            name of the member who created the comment
        date: str
            date the comment was created

    Methods
    -------
        from_json(cls, data): creates a comment object from json data
        __repr__(self): returns a string representation of a comment object
    """

    def __init__(self, comment_id, data, member_creator, date):
        super().__init__()
        self.comment_id = comment_id
        self.data = data
        self.member_creator = member_creator
        self.date = date

    @classmethod
    def from_json(cls, data):
        """
        Creates a comment object from json data

        Parameters
        ----------
            data: dict
                json dict containing data for a comment object
        """
        return cls(comment_id=data['id'],
                   data=data['data']['text'],
                   member_creator=data['memberCreator']['fullName'],
                   date=data['date'])

    def __repr__(self):
        """
        Creates a string representation of a comment object
        """
        date_segments = self.date.split("T")
        time = date_segments[1][:-5]
        calendar_date = date_segments[0]
        return (
            f'{self.member_creator}: "{self.data}" @ {time}, {calendar_date}'
        )


class Label(TrelloBase):
    """
    Class representing a Trello Label object

    Attributes
    ----------
        label_id: str
            id for a label object
        name: str
            name of the label
        color: str
            color of the label
        board_id: str
            id of the board the label belongs to

    Methods
    -------
        from_json(cls, data): creates a label object from json data
        from_json_list(cls, data): creates a list of label objects from json data
        __repr__(self): returns a string representation of a label object

    """

    def __init__(self, label_id, name, color, board_id):
        super().__init__()
        self.label_id = label_id
        self.name = name
        self.color = color
        self.board_id = board_id

    @classmethod
    def from_json(cls, data):
        """
        Creates a label object from json data

        Parameters
        ----------
            data: dict
                json dict containing data for a label object
        """
        return cls(label_id=data['id'], name=data['name'], color=data['color'], board_id=data['idBoard'])

    @classmethod
    def from_json_list(cls, data):
        """
        Creates a list of label objects from json data

        Parameters
        ----------
            data: list
                list of json dicts containing data for label objects

        """
        return [cls.from_json(label) for label in data]

    def __repr__(self):
        """
        Creates a string representation of a label object
        """
        return (
            f'(name = {self.name},color = {self.color}, id = {self.label_id}'
        )


class Card(TrelloBase):
    """
    class for representing a trello card object

    Attributes
    ----------
        name: str
            name of the card
        card_id: str
            id of the card
        labels: list
            list of labels associated with the card
        desc: str
            description of the card
        comments: int
            number of comments on the card

    Methods
    -------
        from_json(cls, data): creates a card object from json data
        get_comments(self): returns a list of comments on a card in reverse
        chronological order
        __repr__(self): returns a string representation of a card object

    """

    def __init__(self, name, card_id, labels, desc, comments):
        super().__init__()
        self.name = name
        self.card_id = card_id
        self.labels = labels
        self.desc = desc
        self.comments = comments

    @classmethod
    def from_json(cls, data):
        """
        Creates a card object from json data

        Parameters
        ----------
            data: dict
                json dict containing data for a card object

        """
        card = cls(card_id=data['id'],
                   name=data['name'],
                   labels=data['labels'],
                   desc=data['desc'],
                   comments=data['badges']['comments']
                   )
        return card

    def __repr__(self):
        """
        Creates a string representation of a card object
        """
        return (
            f' (id = {self.card_id}, name={self.name})'
        )

    def get_comments(self):
        """
        Returns a list of comments on a card in reverse chronological order

        Returns
        -------
            comments: list
                list of comments on a card in reverse chronological order

        """
        json_payload = self.client.get_actions(self.card_id)
        comments = [Comment.from_json(comment) for comment in json_payload.json()]
        comments = sorted(comments, key=lambda comment: comment.date, reverse=True)
        return comments


class TrelloList(TrelloBase):
    """
    Class representing a Trello List

    Attributes
    ----------
        list_id: str
            id of the list
        name: str
            name of the list

    Methods
    -------
        from_json(cls, data): creates a TrelloList object from json data
        get_all_cards(self): returns a list of cards associated with the list
        __repr__(self): returns a string representation of a TrelloList object

    """

    def __init__(self, list_id, name):
        super().__init__()
        self.list_id = list_id
        self.name = name

    @classmethod
    def from_json(cls, data):
        """
        Creates a TrelloList object from json data

        Parameters
        ----------
            data: dict
                json dict containing data for a TrelloList object

        """
        return cls(list_id=data['id'], name=data['name'])

    def __repr__(self):
        """
        Creates a string representation of a TrelloList object
        """
        return (
            f'(id= {self.list_id}, name={self.name})'
        )

    def get_all_cards(self):
        """
        Returns all cards associated with a list
        """
        json_payload = self.client.get_all_cards(self.list_id)
        cards = [Card.from_json(card) for card in json_payload.json()]
        return cards


class Board(TrelloBase):
    """
    Class representing a Trello Board

    Attributes
    ----------
        board_id: str
            id of the board
        name: str
            name of the board

    Methods
    -------
        from_json(cls, data): creates a Board object from json data
        get_all_lists(self): returns a list of TrelloLists associated with a board
        get_labels(self): returns a list of labels associated with a board
        __repr__(self): returns a string representation of a Board object

    """

    def __init__(self, board_id, name):
        super().__init__()
        self.board_id = board_id
        self.name = name

    @classmethod
    def from_json(cls, data):
        """
        Creates a Board object from json data

        Parameters
        ----------
            data: dict
                json dict containing data for a Board object
        """
        return cls(board_id=data['id'],
                   name=data['name']
                   )

    def __repr__(self):
        """
        Creates a string representation of a Board object
        """
        return f'(id= {self.board_id}, name={self.name})'

    def get_all_lists(self):
        """
        Returns all lists associated with a board
        """
        json_payload = self.client.get_all_lists(self.board_id)
        trello_lists = [TrelloList.from_json(trello_list) for trello_list in json_payload.json()]
        return trello_lists

    def get_labels(self):
        """
        Returns all labels associated with a board
        """
        json_payload = self.client.get_labels(self.board_id)
        labels = Label.from_json_list(json_payload.json())
        return labels
