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
list_data = {'name': 'TODO', 'id': '65352f31c09f6a38f8df1d0c'}
card_data = {'name': "Move anything 'ready' here", 'id': '65352f31c09f6a38f8df1d59'}
label_data = {'board_id': '65352f31c09f6a38f8df1d0a', 'label': 'blue', 'id': '65352f31c09f6a38f8df1d65'}


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert result.stdout == f"{__app_name__} version {__version__}\n"


def test_get_board():
    result = runner.invoke(cli.app, ["get-board"], input=board_data['id'])
    assert result.exit_code == 0
    assert board_data['name'] in result.stdout
    assert board_data['id'] in result.stdout
    assert "lists" in result.stdout
    assert "labels" in result.stdout


def test_get_cards():
    result = runner.invoke(cli.app, ["get-cards"], input=list_data['id'])
    assert result.exit_code == 0
    assert card_data['name'] in result.stdout
    assert card_data['id'] in result.stdout


def test_view_card():
    result = runner.invoke(cli.app, ["view-card"], input=card_data['id'])
    assert result.exit_code == 0
    assert card_data['name'] in result.stdout
    assert card_data['id'] in result.stdout
    assert "comments" in result.stdout
    assert "labels" in result.stdout


def test_make_trello_card():
    result = runner.invoke(cli.app, ["make-trello-card"], input=list_data['id'] + "\ntest\n")
    assert result.exit_code == 0
    assert "your card has been created" in result.stdout
    assert "test" in result.stdout


def test_prepend_comment():
    result = runner.invoke(cli.app, ["prepend-comment"], input=card_data['id'] + "\ntest\n")
    assert result.exit_code == 0
    assert "your comment has been created" in result.stdout
    assert "test" in result.stdout


def test_prepend_label():
    result = runner.invoke(cli.app, ["prepend-label"], input=card_data['id'] + "\n" + label_data['id'] + "\n")
    assert result.exit_code == 0
    assert "your label has been added" in result.stdout

