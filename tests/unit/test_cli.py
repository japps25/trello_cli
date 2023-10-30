"""Unit tests for the CLI."""

# local imports
from trello_cli import __app_name__, __version__, cli

# third party imports
from typer.testing import CliRunner
import pytest

# Setup
runner = CliRunner()

# Test data
board_data = {'board_id': '65352f31c09f6a38f8df1d0a', 'name': 'Simple Project Board'}
list_data = {'name': 'DOING ⚙️', 'list_id': '65352f31c09f6a38f8df1d0d'}
card_data = {'name': "✋🏿 Move anything that is actually started here", 'card_id': '65352f31c09f6a38f8df1d5b'}
label_data = {'board_id': '65352f31c09f6a38f8df1d0a', 'label': 'yellow', 'label_id': '65352f31c09f6a38f8df1d6e'}


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert result.stdout == f"{__app_name__} version {__version__}\n"


def test_get_board():
    result = runner.invoke(cli.app, ["get-board"], input=board_data['board_id'])
    assert result.exit_code == 0
    assert board_data['name'] in result.stdout
    assert board_data['board_id'] in result.stdout
    assert "lists" in result.stdout
    assert "labels" in result.stdout


def test_get_cards():
    result = runner.invoke(cli.app, ["get-cards"], input=list_data['list_id'])
    assert result.exit_code == 0
    assert card_data['name'] in result.stdout
    assert card_data['card_id'] in result.stdout


def test_view_card():
    result = runner.invoke(cli.app, ["view-card"], input=card_data['card_id'])
    assert result.exit_code == 0
    assert card_data['name'] in result.stdout
    assert card_data['card_id'] in result.stdout
    assert "comments" in result.stdout
    assert "labels" in result.stdout


def test_make_trello_card():
    result = runner.invoke(cli.app, ["make-trello-card"], input=list_data['list_id'] + "\ntest\n")
    assert result.exit_code == 0
    assert "your card has been created" in result.stdout
    assert "test" in result.stdout


def test_prepend_comment():
    result = runner.invoke(cli.app, ["prepend-comment"], input=card_data['card_id'] + "\ntest\n")
    assert result.exit_code == 0
    assert "your comment has been created" in result.stdout
    assert "test" in result.stdout


def test_prepend_label():
    result = runner.invoke(cli.app, ["prepend-label"],
                           input=card_data['card_id'] + "\n" + label_data['label_id'] + "\n")
    assert "your label has been added" in result.stdout
    assert result.exit_code == 0


def test_prepend_label_param_error():
    result = runner.invoke(cli.app, ["prepend-label"],
                           input=board_data['board_id'] + "\n" + label_data['board_id'] + "\n")
    assert 'Error adding label: card_id and label_id cannot be the same' in result.stdout
    assert result.exit_code == 1
