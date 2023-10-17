from typing import List

from rich.console import Console, ConsoleOptions, RenderResult
from trello_cli.models import *
from trello_cli.trello_api import TrelloAPI
from trello_cli import (SUCCESS)
import os


class TrelloBase(object):
    def __init__(self):
        self.client = TrelloAPI(api_key=os.getenv("TRELLO_API_KEY"), api_token=os.getenv("TRELLO_API_TOKEN"))


class Comment(TrelloBase):

    def __init__(self, id, data, member_creator, date):
        super().__init__()
        self.id = id
        self.data = data
        self.member_creator = member_creator
        self.date = date

    @classmethod
    def from_json(cls, data):
        return cls(id=data['id'],
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

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        yield f"[b]Comment:{self.member_creator}: {self.data} {self.date} [/b]"


class Label(TrelloBase):
    """
    Class representing a Trello Label.
    """

    def __init__(self, id, name, color, idBoard):
        super().__init__()
        self.id = id
        self.name = name
        self.color = color
        self.idBoard = idBoard

    @classmethod
    def from_json(cls, data):
        return cls(id=data['id'], name=data['name'], color=data['color'], idBoard=data['idBoard'])

    @classmethod
    def from_json_list(cls, data):
        return [cls.from_json(label) for label in data]

    def __repr__(self):
        return (
            f'name = {self.name},color = {self.color}')

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        yield f"[b]name:{self.name}[/b]"
        yield f"[b]color:{self.color}[/b]"


class Card(TrelloBase):
    """
    class for representing a trello card object

    """

    def __init__(self, name, id, labels, desc, comments):
        super().__init__()
        self.name = name
        self.id = id
        self.labels = labels
        self.desc = desc
        self.comments = comments

    @classmethod
    def from_json(cls, data):
        card = cls(id=data['id'],
                   name=data['name'],
                   labels=Label.from_json_list(data['labels']),
                   desc=data['desc'],
                   comments=data['badges']['comments']
                   )
        return card

    def __repr__(self):
        return (
            f'{self.name}'
        )

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        labels = []
        for label in self.labels:
            labels.append(label.color)
        yield f"[b]Card:{self.name}[/b]"
        yield f"[b]Desc:{self.desc}[/b]"
        yield f"[b]Labels: {labels}[/b]"
        yield f"[b]Comments:{self.comments}[/b]"

    def get_comments(self):
        json_payload = self.client.get_actions(self.id)
        comments = [Comment.from_json(comment) for comment in json_payload]
        comments = sorted(comments, key=lambda comment: comment.date, reverse=True)
        for comment in comments:
            print(comment)


class TrelloList(TrelloBase):
    """
    Class representing a Trello List.
    
    """

    def __init__(self, id, name):
        super().__init__()
        self.id = id
        self.name = name

    @classmethod
    def from_json(cls, data):
        return cls(id=data['id'], name=data['name'])

    def __repr__(self):
        return (
            f'{self.name}'
        )

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        yield f"[b]TrelloList:{self.name}[/b]"

    def get_all_cards(self):
        json_payload = self.client.get_all_cards(self.id)
        cards = [Card.from_json(card) for card in json_payload]
        return cards




class Board(TrelloBase):

    def __init__(self, id, name):
        super().__init__()
        self.id = id
        self.name = name

    @classmethod
    def from_json(cls, data):
        return cls(id=data['id'],
                   name=data['name']
                   )

    def __repr__(self):
        return f'{self.name}'

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        yield f"[b]Board:[/b] #{self.name}"

    def get_all_lists(self):
        json_payload = self.client.get_all_lists(self.id)
        trello_lists = [TrelloList.from_json(trello_list) for trello_list in json_payload]
        return trello_lists

    def get_labels(self):
        json_payload = self.client.get_labels(self.id)
        labels = Label.from_json_list(json_payload)
        return labels

    def get_all_cards(self):
        json_payload = self.client.get_all_cards(self.id)
        cards = [Card.from_json(card) for card in json_payload]
        return cards
