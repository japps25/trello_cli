#module imports 

#dependency imports
#from trello import Board, List as TrelloList, Label, Card 

#misc imports
from typing import List




class Label(object):
    """
    Class representing a Trello Label.
    """
    def __init__(self, client, label_id, name, color=""):
        self.client = client
        self.id = label_id
        self.name = name
        self.color = color

    @classmethod
    def from_json(cls, board, json_obj):
        """
        Deserialize the label json object to a Label object

        :board: the parent board the label is on
        :json_obj: the label json object
        """
        label = Label(board.client,
                      label_id=json_obj['id'],
                      name=json_obj['name'],
                      color=json_obj['color'])
        return label


    @classmethod
    def from_json_list(cls, board, json_objs):
        return [cls.from_json(board, obj) for obj in json_objs]


    def __repr__(self):
        return u'<Label %s>' % self.name

    def fetch(self):
        """Fetch all attributes for this label"""
        json_obj = self.client.fetch_json('/labels/' + self.id)
        self.name = json_obj['name']
        self.color = json_obj['color']
        return self

    
class Card(object):
    """
    class for representing a trello card object

    Attributes:
        id (str) : id of card
        fields(List[str]) : list of fields of card

    """

    @property
    def short_url(self):
        return self.shortUrl

    @property
    def board_id(self):
        return self.idBoard
    
    @property
    def list_id(self):
        return self.idList
    
    @property
    def description(self):
        return self.desc
    
    @description.setter
    def description(self, value):
        self.desc = value
    
    @property
    def idLabels(self):
        return self.label_ids
    
    @idLabels.setter
    def idLabels(self, values):
        self.label_ids = values

    @property
    def list_labels(self):
        if self.labels:
            return self.labels
        return None
    
    @property
    def comments(self):
        """
        Lazily loads and returns the comments
        """
        try:
            if self._comments is None:
                self._comments = self.fetch_comments()
        except AttributeError:
            self._comments = None
        return self._comments
    
    def __init__(self, parent, card_id, name=''):
        """
        :parent: reference to the parent trello list
        :card_id: ID for this card
        """
        if isinstance(parent, List):
            self.trello_list = parent
            self.board = parent.board
        else:
            self.board = parent

        self.client = parent.client
        self.id = card_id
        self.name = name
        self.pos = None

    def __repr__(self):
        return u'<Card %s>' % self.name

    @classmethod
    def from_json(cls, parent, json_obj):
        """
        Deserialize the card json object to a Card object

        :parent: the list object that the card belongs to
        :json_obj: json object

        :rtype: Card
        """
        if 'id' not in json_obj:
            raise Exception("key 'id' is not in json_obj")
        card = cls(parent,
                   json_obj['id'],
                   name=json_obj['name'])
        card.desc = json_obj.get('desc', '')
        card.due = json_obj.get('due', '')
        card.short_url = json_obj['shortUrl']
        card.idLabels = json_obj['idLabels']
        card.idBoard = json_obj['idBoard']
        card.idList = json_obj['idList']
        card.pos = json_obj['pos']
        card.labels = Label.from_json_list(card.board, json_obj['labels'])
        return card
    
    def fetch(self):
        """
        Fetch all attributes for this card

        
        """
        json_obj = self.client.fetch_json(
            '/cards/' + self.id,
            query_params={'badges': False})
        self.id = json_obj['id']
        self.name = json_obj['name']
        self.desc = json_obj.get('desc', '')
        self.idList = json_obj['idList']
        self.idBoard = json_obj['idBoard']
        self.idLabels = json_obj['idLabels']
        self.pos = json_obj['pos']
        self.labels = Label.from_json_list(self.board, json_obj['labels'])
        self._comments = self.fetch_comments()


    def fetch_comments(self,  limit=None):
        comments = []
        if limit is not None:
            limit = 10
        comments = self.client.fetch_json(
            '/cards/' + self.id + '/actions',
            query_params=limit)
        return sorted(comments, key=lambda comment: comment['date'])
    

class Column (object):
    """
    Class representing a Trello List.
    
    """
    def __init__(self, board, list_id, name):
        self.board = board
        self.client = board.client
        self.id = list_id
        self.name = name
        self.closed =None 
        self.pos = None
    
    @classmethod
    def from_json(cls, board, json_obj):
        """
        Deserialize the list json object to a List object

        :board: the board object that the list belongs to
        :json_obj: the json list object
        """
        column = column(board, json_obj['id'], name=json_obj['name'])
        column.closed = json_obj['closed']
        column.pos = json_obj['pos']
        return column


    def __repr__(self):
        return u'<List %s>' % self.name

    def fetch(self):
        """Fetch all attributes for this list"""
        json_obj = self.client.fetch_json('/columns/' + self.id)
        self.name = json_obj['name']
        self.closed = json_obj['closed']
        self.pos = json_obj['pos']

    def list_cards(self, card_filter="open", actions=None):
        """Lists all cards in this list"""
        query_params = {}
        if card_filter:
            query_params['filter'] = card_filter
        if actions:
            query_params['actions'] = actions
        json_obj = self.client.fetch_json('/lists/' + self.id + '/cards',
                                          query_params=query_params)
        return [Card.from_json(self, c) for c in json_obj]

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
    
    def __init__(self, client = None, board_id = None, name = ''):
        self.id = board_id
        self.client = client
        self.name =name

    @classmethod
    def from_json(cls, trello_client=None, json_obj=None):
        """
		Deserialize the board json object to a Board object

		:trello_client: the trello client
		:json_obj: the board json object

		"""
        board = Board(client=trello_client, board_id=json_obj['id'], name=json_obj['name'])
        board.description = json_obj.get('desc', '')
        board.url = json_obj['url']
        return board
    

    def __repr__(self):
        return u'<Board %s>' % self.name
    
    def fetch(self):
        """Fetch all attributes for this board"""
        json_obj = self.client.fetch_json('/boards/' + self.id)
        self.name = json_obj['name']
        self.description = json_obj.get('desc', '')
        self.closed = json_obj['closed']
        self.url = json_obj['url']


    # Saves a Trello Board
    def save(self):
        json_obj = self.client.fetch_json(
            '/boards/',
            http_method='POST',
            post_args={'name': self.name, "desc": self.description, "defaultLists": False}, )
        # Set initial data from Trello
        self.from_json(json_obj=json_obj)
        self.id = json_obj["id"]

    
    def get_lists(self, list_filter):
        """Returns all lists on this board
        """
        json_obj = self.client.fetch_json(
            '/boards/' + self.id + '/lists',
            query_params={'filter': list_filter})
        return [List.from_json(self, json_obj=obj) for obj in json_obj]
    
    def list_lists(self, list_filter="all"):
        """Returns all lists on this board"""
        return self.get_lists(list_filter = list_filter)
    
    def all_lists(self):
        """Returns all lists on this board

		:rtype: list of List
		"""
        return self.get_lists('all')
    
    def get_labels(self, fields='all', limit=50):
        """Get label
        :rtype: list of Label
		"""
        json_obj = self.client.fetch_json(
            '/boards/' + self.id + '/labels',
            query_params={'fields': fields, 'limit': limit})
        return Label.from_json_list(self, json_obj)
    
    def add_label(self, name, color):
        """Add a label to this board

		:name: name of the label
		:color: the color, either green, yellow, orange
			red, purple, blue, sky, lime, pink, or black
		:return: the label
		:rtype: Label
		"""
        obj = self.client.fetch_json(
            '/labels',
            http_method='POST',
            post_args={'name': name, 'idBoard': self.id, 'color': color}, )
        return Label.from_json(board=self, json_obj=obj)
    
    def all_cards(self):
        """Returns all cards on this board

		:rtype: list of Card
		"""
        filters = {
			'filter': 'all',
			'fields': 'all'
		}
        return self.get_cards(filters)
    
    def get_cards(self, filters=None, card_filter=""):
        """
		:filters: dict containing query parameters. Eg. {'fields': 'all'}
		:card_filter: filters on card status ('open', 'closed', 'all')

		More info on card queries:
		https://trello.com/docs/api/board/index.html#get-1-boards-board-id-cards

		:rtype: list of Card
		"""
        json_obj = self.client.fetch_json(
				'/boards/' + self.id + '/cards/' + card_filter,
				query_params=filters
		)
        return list([Card.from_json(self, json) for json in json_obj])


    
    

    

