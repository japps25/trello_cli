
#module imports
from trello_cli import TRELLO_READ_ERROR, TRELLO_WRITE_ERROR, SUCCESS
from trello_cli.trello_service import TrelloService
from trello_cli.models import *

#dependency imports

#misc imports


def test_get_access_token(mocker):
    """test to check whether user is authenticated or not"""
    
    mock_rest = GetOAuthTokenResponse(
        token = "test", 
        token_secret="test", 
        status_code = SUCCESS
    )
    mocker.patch(
        "trello_cli.trello_service.TrelloService.get_user_oauth_token",
            return_value=mock_rest   
  )
    trellojob = TrelloService()
    res = trellojob.get_user_oauth_token()
    assert res.status_code == SUCCESS

def test_get_all_boards(mocker):
    """test to check that boards have been fetched"""

    mock_res = GetAllBoardsResponse(
        res = [],
        status_code = SUCCESS
    )
    mocker.patch(
        "trello_cli.trello_service.TrelloService.get_all_boards",
        return_value=mock_res 
  )
    trellojob = TrelloService()
    res = trellojob.get_all_boards()

    assert res.status_code == SUCCESS

def test_get_board(mocker):
    """test to check that board has been retrieved"""
    
    mock_res = GetBoardResponse(
        res = None,
        status_code = SUCCESS
    )
    mocker.patch(
        "trello_cli.trello_service.TrelloService.get_board",
        return_value=mock_res 
  )
    trellojob = TrelloService()
    res = trellojob.get_board(board_id="test")

    assert res.status_code == SUCCESS

def test_get_all_lists(mocker):
    """test to check that lists have been fetched"""
    
    mock_res = GetAllListsResponse(
        res = [],
        status_code = SUCCESS
    )
    mocker.patch(
        "trello_cli.trello_service.TrelloService.get_all_lists",
        return_value=mock_res 
  )
    trellojob = TrelloService()
    res = trellojob.get_all_lists(board=None)

    assert res.status_code == SUCCESS

def test_get_list(mocker):
    """test to check that list has been retrieved"""
    
    mock_res = GetListResponse(
        res = None,
        status_code = SUCCESS
    )
    mocker.patch(
        "trello_cli.trello_service.TrelloService.get_list",
        return_value=mock_res 
  )
    trellojob = TrelloService()
    res = trellojob.get_list(board=None, list_id="")

    assert res.status_code == SUCCESS

def test_get_all_labels(mocker):
    """test to check that labels have been fetched"""
    
    mock_res = GetAllLabelsResponse(
        res = [],
        status_code = SUCCESS
    )
    mocker.patch(
        "trello_cli.trello_service.TrelloService.get_all_labels",
        return_value=mock_res 
  )
    trellojob = TrelloService()
    res = trellojob.get_all_labels(board=None)

    assert res.status_code == SUCCESS

def test_get_label(mocker):
    """test to check that label has been retrieved"""
    
    mock_res = GetLabelResponse(
        res = None,
        status_code = SUCCESS
    )
    mocker.patch(
        "trello_cli.trello_service.TrelloService.get_label",
        return_value=mock_res 
  )
    trellojob = TrelloService()
    res = trellojob.get_label(board=None, label_id="")

    assert res.status_code == SUCCESS

def test_add_card(mocker):
    """checks success of adding a new card to trello.com board"""
    mock_res = AddCardResponse(
        res = None,
        status_code = SUCCESS
        )
    mocker.patch(
        "trello_cli.trello_service.TrelloService.add_card",
        return_value=mock_res 
    )
    trellojob = TrelloService()
    res = trellojob.add_card(col=None, name="")
    
    assert res.status_code == SUCCESS
