import pytest_mock


def test_mock_get_all_boards(mocker, trello_api) -> None:
    mocked_call_api_value = [
        {
            'id': '6523e63b8e337f3ce55311a2',
            'name': 'Design System Checklist'
        },
        {
            'id': '6523e5aa8c0d41e7537d7b2f',
            'name': 'Kanban Template'
        },
        {
            'id': '6526f7f91942a8eb420c84cc',
            'name': 'Meal Planning'
        },
        {
            'id': '6523e605b0d6b5829b5662e3',
            'name': 'Remote Team Hub'
        }
    ]

    mocker.patch('trello_cli.trello_api.TrelloApi.call_api',
                 return_value=mocked_call_api_value)
    actual_mock_response = trello_api.get_all_boards()
    assert mocked_call_api_value == actual_mock_response


def test_mock_get_board(mocker, trello_api) -> None:
    mocked_call_api_value = {
        'id': '6526f7f91942a8eb420c84cc',
        'name': 'Meal Planning'
    }
    mocker.patch('trello_cli.trello_api.TrelloApi.call_api',
                 return_value=mocked_call_api_value)
    actual_mock_response = trello_api.get_board(board_id='6526f7f91942a8eb420c84cc')
    assert mocked_call_api_value == actual_mock_response


def test_mock_get_list(mocker, trello_api) -> None:
    mocked_call_api_value = [
        {
            'id': '6526f7f91942a8eb420c84cd',
            'name': 'Shopping Lists'
        },
        {
            'id': '6526f7f91942a8eb420c84ce',
            'name': '10/26-11/1 Meal Plan'
        },
        {
            'id': '6526f7f91942a8eb420c84d6',
            'name': 'Make Ahead'
        }
    ]
    mocker.patch('trello_cli.trello_api.TrelloApi.call_api',
                 return_value=mocked_call_api_value)
    actual_mock_response = trello_api.get_all_lists(board_id='6526f7f91942a8eb420c84cc')
    assert mocked_call_api_value == actual_mock_response


def test_get_all_cards(mocker, trello_api) -> None:
    mocked_call_api_value = [
        {
            'id': '6526f7f91942a8eb420c87a6',
            'name': 'Rosemary Pork Burgers',
            'labels': [
                {
                    'id': '6526f7f91942a8eb420c8932',
                    'idBoard': '6526f7f91942a8eb420c84cc',
                    'name': 'Dairy Free',
                    'color': 'sky',
                    'uses': 36
                },
                {
                    'id': '6526f7f91942a8eb420c8936',
                    'idBoard': '6526f7f91942a8eb420c84cc',
                    'name': 'Nut Free',
                    'color': 'red',
                    'uses': 58
                },
                {
                    'id': '6526f7f91942a8eb420c8939',
                    'idBoard': '6526f7f91942a8eb420c84cc',
                    'name': 'Gluten Free',
                    'color': 'orange',
                    'uses': 76
                },
                {
                    'id': '6526f7f91942a8eb420c893c',
                    'idBoard': '6526f7f91942a8eb420c84cc',
                    'name': 'Egg Free',
                    'color': 'purple',
                    'uses': 50
                }
            ],
            'desc': '**Ingredients**\n1 lb ground pork\n1 small onion, diced finely\n1 clove garlic, minced\n1 tbsp '
                    'chopped fresh rosemary or 1 tsp ground dried rosemary\n1 tsp Worchestershire sauce\n1 tbsp Dijon '
                    'mustard\nSalt and pepper to taste\n\n**Procedure**\n1. In a large bowl, mix all ingredients '
                    'together with your hands\n2. Split into 3 or 4 equal parts and form into patties\n3. Grill or '
                    'pan-fry until they reach an internal temperature of 160. They will get very brown, but that adds '
                    'to the flavor\n\n**Recipe Notes**\nThis recipe can be easily doubled, tripled, etc.\nThe patties '
                    'can be made ahead of time and stored in the fridge until ready to cook or even '
                    'frozen\n\n**Serving Suggestions**\nThese are great on their own eaten like sausage '
                    'patties\n\nShared by Kristen Franks',
            'badges': {
                'attachmentsByType': {
                    'trello': {
                        'board': 0,
                        'card': 0
                    }
                },
                'location': False,
                'votes': 0,
                'viewingMemberVoted': False,
                'subscribed': True,
                'fogbugz': '',
                'checkItems': 0,
                'checkItemsChecked': 0,
                'checkItemsEarliestDue': None,
                'comments': 1,
                'attachments': 0,
                'description': True,
                'due': None,
                'dueComplete': False,
                'start': None
            }
        }
    ]
    mocker.patch('trello_cli.trello_api.TrelloApi.call_api',
                 return_value=mocked_call_api_value)
    actual_response = trello_api.get_all_cards(list_id='6526f7f91942a8eb420c84d6')
    assert mocked_call_api_value == actual_response

def test_mock_get_actions(mocker, trello_api):
    mocked_call_api_value = [
        {
            'id': '6527c11e67d1e61487d2c4c8',
            'idMemberCreator': '5a82267fd787a99d39f3b8d3',
            'data': {
                'text': 'test comment',
                'textData': {
                    'emoji': {}
                },
                'card': {
                    'id': '6526f7f91942a8eb420c87a6',
                    'name': 'Rosemary Pork Burgers',
                    'idShort': 43,
                    'shortLink': 'SKSfyg4S'
                },
                'board': {
                    'id': '6526f7f91942a8eb420c84cc',
                    'name': 'Meal Planning',
                    'shortLink': 'plXaShGM'
                },
                'list': {
                    'id': '6526f7f91942a8eb420c84d6',
                    'name': 'Make Ahead'
                }
            },
            'appCreator': None,
            'type': 'commentCard',
            'date': '2023-10-12T09:49:18.502Z',
            'limits': {
                'reactions': {
                    'perAction': {
                        'status': 'ok',
                        'disableAt': 900,
                        'warnAt': 720
                    },
                    'uniquePerAction': {
                        'status': 'ok',
                        'disableAt': 17,
                        'warnAt': 14
                    }
                }
            },
            'memberCreator': {
                'id': '5a82267fd787a99d39f3b8d3',
                'activityBlocked': False,
                'avatarHash': '094eb293b4637f4a4f4f36b9ff325349',
                'avatarUrl': 'https://trello-members.s3.amazonaws.com/5a82267fd787a99d39f3b8d3/094eb293b4637f4a4f4f36b9ff325349',
                'fullName': 'Jessica Apps',
                'idMemberReferrer': None,
                'initials': 'JA',
                'nonPublic': {},
                'nonPublicAvailable': True,
                'username': 'jessicaapps'
            }
        }
    ]
    mocker.patch('trello_cli.trello_api.TrelloApi.call_api',
                 return_value=mocked_call_api_value)
    actual_response = trello_api.get_actions(card_id='6526f7f91942a8eb420c87a6')
    assert actual_response == mocked_call_api_value

def test_get_labels(mocker,trello_api):
    mocked_call_api_value = [
        {
            'id': '6526f7f91942a8eb420c8939',
            'name': 'Gluten Free',
            'color': 'orange',
            'idBoard': '6526f7f91942a8eb420c84cc',
            'uses': 76
        },
        {
            'id': '6526f7f91942a8eb420c8936',
            'name': 'Nut Free',
            'color': 'red',
            'idBoard': '6526f7f91942a8eb420c84cc',
            'uses': 58
        },
        {
            'id': '6526f7f91942a8eb420c893c',
            'name': 'Egg Free',
            'color': 'purple',
            'idBoard': '6526f7f91942a8eb420c84cc',
            'uses': 50
        },
        {
            'id': '6526f7f91942a8eb420c8932',
            'name': 'Dairy Free',
            'color': 'sky',
            'idBoard': '6526f7f91942a8eb420c84cc',
            'uses': 36
        },
        {
            'id': '6526f7f91942a8eb420c8925',
            'name': 'Vegetarian',
            'color': 'green',
            'idBoard': '6526f7f91942a8eb420c84cc',
            'uses': 32
        },
        {
            'id': '6526f7f91942a8eb420c893f',
            'name': 'Vegan',
            'color': 'yellow',
            'idBoard': '6526f7f91942a8eb420c84cc',
            'uses': 15
        }
    ]
    mocker.patch('trello_cli.trello_api.TrelloApi.call_api',
                 return_value=mocked_call_api_value)
    actual_response = trello_api.get_labels(board_id='6526f7f91942a8eb420c84cc')
    assert mocked_call_api_value == actual_response

