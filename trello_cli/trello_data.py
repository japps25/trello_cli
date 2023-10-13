from rich.console import Console, ConsoleOptions, RenderResult
import os


class Comment(object):

    def __init__(self, id, data, member_creator, date):
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


class Label(object):
    """
    Class representing a Trello Label.
    """

    def __init__(self, id, name, color, idBoard):
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


class Card(object):
    """
    class for representing a trello card object

    """

    def __init__(self, name, id, labels, desc, comments, list_id):
        self.name = name
        self.id = id
        self.labels = labels
        self.desc = desc
        self.comments = comments
        self.list_id = list_id

    @classmethod
    def from_json(cls, data):
        card = cls(id=data['id'],
                   name=data['name'],
                   labels=Label.from_json_list(data['labels']),
                   desc=data['desc'],
                   comments=data['badges']['comments'],
                   list_id=data['idList'])
        return card

    def __repr__(self):
        return (
            f'{self.name}, {self.id}'
        )

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        labels = []
        for label in self.labels:
            labels.append(label.color)
        yield f"[b]Card:{self.name}[/b]"
        yield f"[b]Desc:{self.desc}[/b]"
        yield f"[b]Labels: {labels}[/b]"
        yield f"[b]Comments:{self.comments}[/b]"

    # def __init__(self, name, id, labels, desc, comments, due, start, closed):
    #     self.name = name
    #     self.id = id
    #     self.labels = labels
    #     self.desc = desc
    #     self.comments = comments
    #     self.due = due
    #     self.start = start
    #     self.closed = closed
    #
    # @classmethod
    # def from_json(cls, data):
    #     card = cls(id=data['id'],
    #                name=data['name'],
    #                labels=Label.from_json_list(data['labels']),
    #                desc=data['desc'],
    #                comments=data['badges']['comments'],
    #                due=data['due'],
    #                start=data['start'],
    #                closed=data['closed'])
    #     return card


class List(object):
    """
    Class representing a Trello List.
    
    """

    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def from_json(cls, data):
        return cls(id=data['id'], name=data['name'])

    def __repr__(self):
        return (
            f'{self.name}, {self.id}'
        )

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        yield f"[b]List:{self.name}[/b]"


class Board(object):

    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def from_json(cls, data):
        return cls(id=data['id'],
                   name=data['name']
                   )

    def __repr__(self):
        return f'{self.id},{self.name}'

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        yield f"[b]Board:[/b] #{self.name}"
