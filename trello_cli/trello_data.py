
class Comment(object):

    def __init__(self, id, data):
        self.id = id
        self.data = data

    @classmethod
    def from_json(cls, data):
        return cls(id=data['id'], data=data['data']['text'])

    def __repr__(self):
        return (
            f'Action(id = {self.id},text = {self.data}')


class Label(object):
    """
    Class representing a Trello Label.
    """

    def __init__(self, id, name, color, idBoard, uses):
        self.id = id
        self.name = name
        self.color = color
        self.idBoard = idBoard
        self.uses = uses

    @classmethod
    def from_json(cls, data):
        return cls(id=data['id'], name=data['name'], color=data['color'], idBoard=data['idBoard'], uses=['uses'])

    @classmethod
    def from_json_list(cls, data):
        return [cls.from_json(label) for label in data]

    def __repr__(self):
        return (
            f'Label(name = {self.name}, id = {self.id},color = {self.color}, idBoard = {self.idBoard}')


class Card(object):
    """
    class for representing a trello card object

    """

    def __init__(self, name, id, labels):
        self.name = name
        self.id = id
        self.labels = labels

    @classmethod
    def from_json(cls, data):
        return cls(name=data['name'],
                   id=data['id'],
                   labels=data['labels']
                   )

    def __repr__(self):
        return (
            f'Card(id = {self.id}, name = {self.name}, labels = {self.labels}')

    def fetch_labels(self):
        return [Label.from_json(label) for label in self.labels]


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
            f'List(id = {self.id},name = {self.name}')



class Board(object):

    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def __repr__(self):
        return (
            f'{self.name}'
        )
