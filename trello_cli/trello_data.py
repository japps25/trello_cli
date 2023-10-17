from trello_cli.models import *
from trello_cli.trello_api import TrelloAPI
import os


class TrelloBase(object):
    """class used to represent a trello object"""

    def __init__(self):
        self.client = TrelloAPI(api_key=os.getenv("TRELLO_API_KEY"), api_token=os.getenv("TRELLO_API_TOKEN"))


class Comment(TrelloBase):
    """A class used to represent a trello comment object

    Attributes
        comment_id (str): comment id
        data (str): comment text
        member_creator (str): member who created the comment
        date (str): date the comment was created

    Methods

        from_json(cls, data): creates a comment object from json data


    """

    def __init__(self, comment_id, data, member_creator, date):
        super().__init__()
        self.comment_id = comment_id
        self.data = data
        self.member_creator = member_creator
        self.date = date

    @classmethod
    def from_json(cls, data):
        return cls(comment_id=data['id'],
                   data=data['data']['text'],
                   member_creator=data['memberCreator']['fullName'],
                   date=data['date'])

    def __repr__(self):
        date_segments = self.date.split("T")
        time = date_segments[1][:-5]
        calendar_date = date_segments[0]
        return (
            f'{self.member_creator}: "{self.data}" @ {time}, {calendar_date}'
        )


class Label(TrelloBase):
    """
    Class representing a Trello Label

    Attributes
        label_id (str): label id
        name (str): label name
        color (str): label color
        board_id (str): board id

    Methods

        from_json(cls, data): creates a label object from json data
        from_json_list(cls, data): creates a list of label objects from json data

    """

    def __init__(self, label_id, name, color, board_id):
        super().__init__()
        self.label_id = label_id
        self.name = name
        self.color = color
        self.board_id = board_id

    @classmethod
    def from_json(cls, data):
        return cls(label_id=data['id'], name=data['name'], color=data['color'], board_id=data['idBoard'])

    @classmethod
    def from_json_list(cls, data):
        return [cls.from_json(label) for label in data]

    def __repr__(self):
        return (
            f'(name = {self.name},color = {self.color}, id = {self.label_id}'
        )


class Card(TrelloBase):
    """
    class for representing a trello card object

    Attributes
        name (str): card name
        card_id (str): card id
        labels (List[Label]): list of labels
        desc (str): card description
        comments (int): number of comments on the card

    Methods

        from_json(cls, data): creates a card object from json data
        get_comments(self): returns a list of comments on the card

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
        card = cls(card_id=data['id'],
                   name=data['name'],
                   labels=data['labels'],
                   desc=data['desc'],
                   comments=data['badges']['comments']
                   )
        return card

    def __repr__(self):
        return (
            f' (id = {self.card_id}, name={self.name})'
        )

    def get_comments(self):
        """
        Fetches comments on a card
        :return: list of comments on a card in reverse chronological order
        """
        json_payload = self.client.get_actions(self.card_id)
        comments = [Comment.from_json(comment) for comment in json_payload.json()]
        comments = sorted(comments, key=lambda comment: comment.date, reverse=True)
        return comments


class TrelloList(TrelloBase):
    """
    Class representing a Trello List

    Attributes
        list_id (str): list id
        name (str): list name

    Methods

        from_json(cls, data): creates a list object from json data
        get_all_cards(self): returns a list of cards in the list

    """

    def __init__(self, list_id, name):
        super().__init__()
        self.list_id = list_id
        self.name = name

    @classmethod
    def from_json(cls, data):
        return cls(list_id=data['id'], name=data['name'])

    def __repr__(self):
        return (
            f'(id= {self.list_id}, name={self.name})'
        )

    def get_all_cards(self):
        """
        Fetches all cards associated with a TrelloList
        :return: list of cards
        """
        json_payload = self.client.get_all_cards(self.list_id)
        cards = [Card.from_json(card) for card in json_payload.json()]
        return cards


class Board(TrelloBase):
    """
    Class representing a Trello Board

    Attributes
        board_id (str): board id
        name (str): board name

    Methods

        from_json(cls, data): creates a board object from json data
        get_all_lists(self): returns a list of TrelloLists associated with the board
        get_labels(self): returns a list of labels associated with the board

    """

    def __init__(self, board_id, name):
        super().__init__()
        self.board_id = board_id
        self.name = name

    @classmethod
    def from_json(cls, data):
        return cls(board_id=data['id'],
                   name=data['name']
                   )

    def __repr__(self):
        return f'(id= {self.board_id}, name={self.name})'

    def get_all_lists(self):
        """
        Fetches all TrelloLists associated with a board
        :rtype: a list of TrelloLists
        """
        json_payload = self.client.get_all_lists(self.board_id)
        trello_lists = [TrelloList.from_json(trello_list) for trello_list in json_payload.json()]
        return trello_lists

    def get_labels(self):
        """
        Fetches all labels associated with a board
        :rtype: a list of Trello Labels
        """
        json_payload = self.client.get_labels(self.board_id)
        labels = Label.from_json_list(json_payload.json())
        return labels
