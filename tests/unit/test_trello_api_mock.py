""" Test module for trello_api.py using mock responses """

# local imports
from trello_cli import (SUCCESS)
from trello_cli.models import *
from trello_cli.config import get_user_oauth_token


def test_get_user_oauth_token(mocker):
    """Test to check success retrieval of user's access token"""
    mock_res = GetOAuthTokenResponse(
        token="test",
        secret="test",
        status_code=SUCCESS
    )
    mocker.patch(
        "trello_cli.config.create_oauth_token",
        return_value=mock_res
    )

    res = get_user_oauth_token()
    assert res.status_code == SUCCESS


def test_init_trello(mocker, trello_api):
    """Test to check success retrieval of all trello boards"""
    mock_res = GetAllBoardsResponse(
        res=[],
        status_code=SUCCESS
    )
    mocker.patch(
        'trello_cli.trello_api.TrelloAPI.get_all_boards',
        return_value=mock_res
    )

    res = trello_api.get_all_boards()
    assert res == mock_res


def test_get_board(mocker, trello_api):
    """Test to check success retrieval of a trello board"""
    mock_res = GetBoardResponse(
        res=Board(board_id="test", name="test"),
        status_code=SUCCESS
    )
    mocker.patch(
        'trello_cli.trello_api.TrelloAPI.get_board',
        return_value=mock_res
    )

    res = trello_api.get_board("test")
    assert res == mock_res


def test_get_list(mocker, trello_api):
    """Test to check success retrieval of a trello list"""
    mock_res = GetListResponse(
        res=None,
        status_code=SUCCESS
    )
    mocker.patch(
        'trello_cli.trello_api.TrelloAPI.get_list',
        return_value=mock_res
    )

    res = trello_api.get_list(list_id="test")
    assert res == mock_res


def test_get_card(mocker, trello_api):
    """Test to check success retrieval of a trello card"""
    mock_res = GetCardResponse(
        res=None,
        status_code=SUCCESS
    )
    mocker.patch(
        'trello_cli.trello_api.TrelloAPI.get_card',
        return_value=mock_res
    )

    res = trello_api.get_card(card_id="test")
    assert res == mock_res


def test_create_card(mocker, trello_api):
    """Test to check success creation of a trello card"""
    mock_res = CreateCardResponse(
        res=None,
        status_code=SUCCESS
    )
    mocker.patch(
        'trello_cli.trello_api.TrelloAPI.create_card',
        return_value=mock_res
    )

    res = trello_api.create_card(name="test", idList="test", desc="test")
    assert res == mock_res
