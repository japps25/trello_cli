#module imports 

#dependency imports
#from trello import Board, List as TrelloList, Label, Card 

#misc imports
from typing import List

class Label(object):
    """
    class for representing a trello label object

    Attributes:
        id (str) : id of label
        fields (List[str]) : list of fields of label
    """
    def __init__(self, id, fields):
        self.id = id
        self.fields = fields 

    def __str__(self):
        return f"label id: {self.id}, fields: {self.fields}"
    
    def __repr__(self):
        return f"label id: {self.id}, fields: {self.fields}"
    
class Card(object):
    """
    class for representing a trello card object

    Attributes:
        id (str) : id of card
        fields(List[str]) : list of fields of card

    """
    def __init__(self, id, fields):
        self.id = id
        self.fields = fields

    def __str__(self):
        return f"card id: {self.id}, fields: {self.fields}"

    def __repr__(self):
        return f"card id: {self.id}, fields: {self.fields}"

class Column(object):
    """
    class for representing a trello list object

    Attributes:
        id (str) : id of list
        fields (List[str]) : list of fields of list
    
    """

    def __init__(self, id, fields):
        self.id = id
        self.fields = fields

    def __str__(self):
        return f"list id: {self.id}, fields: {self.fields}"

    def __repr__(self):
        return f"list id: {self.id}, fields: {self.fields}"

class Board(object):
    """
    class for representing a trello board object 

    Attributes:
        id (str) : id of board
        fields (List[str]) : list of fields of board
        columns (List[Column]) : columns in board
        cards (List[Card]) : cards in board
        labels (List[Label]) : labels in board
   
        """
    
    def __init__(self, id, fields, columns, cards, labels):
        self.id = id
        self.fields = fields
        self.columns = columns
        self.cards = cards
        self.labels = labels

    def __str__(self):
        return f"board id: {self.id}, fields: {self.fields}, columns: {self.columns}, cards: {self.cards}, labels: {self.labels}"

    def __repr__(self):
        return f"board id: {self.id}, fields: {self.fields}, columns: {self.columns}, cards: {self.cards}, labels: {self.labels}"
