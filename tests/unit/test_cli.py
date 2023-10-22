"""Unit tests for the CLI."""

# local imports
from trello_cli import __app_name__, __version__, cli

# third party imports
from typer.testing import CliRunner
import pytest

# Setup
runner = CliRunner()

# Test data
board_data = {'id': '65352f31c09f6a38f8df1d0a', 'name': 'Simple Project Board'}
list_data = {'name': 'Guidelines', 'id': '6523e63b8e337f3ce55311a3'}
card_data = {'name': 'Grid-Based Design', 'id': '6523e63b8e337f3ce55312f5'}


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert result.stdout == f"{__app_name__} version {__version__}\n"


def test_get_board():
    result = runner.invoke(cli.app, ["get-board", board_data['id']])
    assert result.exit_code == 0
    assert board_data['name'] in result.stdout
    assert "lists" in result.stdout


def test_get_list():
    result = runner.invoke(cli.app, ["get-list", list_data['id']])
    assert result.exit_code == 0
    assert list_data['name'] in result.stdout
    assert "cards" in result.stdout


def test_get_card():
    result = runner.invoke(cli.app, ["get-card", card_data['id']])
    assert result.exit_code == 0
    assert card_data['name'] in result.stdout
    assert "comments" in result.stdout
    assert "labels" in result.stdout


@pytest.mark.parametrize(
    "list_id",
    [
        pytest.param(
            list_data["id"]
        )
    ],
)
def test_create_card(list_id):
    result = runner.invoke(cli.app, ["create-card", list_id], input="test")
    assert result.exit_code == 0
    assert "your card has been created" in result.stdout


@pytest.mark.parametrize(
    "card_id",
    [
        pytest.param(
            card_data["id"]
        )
    ],
)
def test_create_comment(card_id):
    result = runner.invoke(cli.app, ["create-comment", card_id], input="test")
    assert result.exit_code == 0
    assert "your comment has been created" in result.stdout
    assert "test" in result.stdout
