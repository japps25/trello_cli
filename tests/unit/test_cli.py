from typer.testing import CliRunner

from trello_cli.cli import *
import os
from trello_cli.__main__ import main

app.command()(main)

runner = CliRunner()

api_token = os.getenv("TRELLO_API_TOKEN")
api_secret = os.getenv("TRELLO_API_SECRET")
oauth_token = os.getenv("TRELLO_OAUTH_TOKEN")
oauth_secret = os.getenv("TRELLO_OAUTH_SECRET")


def test_init() -> None:
    result = runner.invoke(app, None)
    if not check_api_tokens():
        expected = "Exiting app"
        assert expected in result.output
        assert result.exit_code == 1
    if check_oauth_tokens():
        expected = "Authentication success"
        assert expected in result.output
    else:
        expected = "please try again"
        assert expected in result.output


def test_check_oauth_tokens():
    result = runner.invoke(app, None)
    expected = "checking oauth tokens..."
    assert expected in result.output
    if oauth_token and oauth_secret:
        expected = "retrieved oauth tokens"
    else:
        expected = "fetching oauth1 tokens"
        assert expected in result.output
