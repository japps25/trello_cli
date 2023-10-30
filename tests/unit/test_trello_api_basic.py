""" Unit Tests for Trello API Basic Functionality
"""

# third party imports
import pytest


def test_get_list_arg_type_value_error(trello_api) -> None:
    """
    Test to check that a ValueError is raised when the wrong type is passed to the get_list method
    """
    with pytest.raises(ValueError) as exc_info:
        trello_api.get_all_lists(board_id=dict)
    assert str(exc_info.value) == "ERROR - Parameter board_id should be of type str"

