import os

from trello_cli.trello_api import TrelloApi


def test_list_boards(trello_api) -> None:
    """
    Unit Test to List Trello Boards
    :param trello_api: Class Object Parameter from conftest. Type - TrelloAPI
    :return: None
    """
    expected_response = [
        {
            "id": "6519d9743e28661e3a7c07a2",
            "name": "1-on-1 Meeting Agenda"
        },
        {
            "id": "5a822682910e15e3551d250c",
            "name": "Customer Service - RealFoodSource - 13/02"
        },
        {
            "id": "5a8226831568e7f5602fe3f7",
            "name": "Untitled board"
        },
        {
            "id": "5a82267fd787a99d39f3b8d6",
            "name": "Welcome Board"
        }]

    actual_response = trello_api.list_boards(query_dict={'fields': ['name', 'id']})
    assert actual_response == expected_response
