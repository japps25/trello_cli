""" Module to define the CLI commands for the trello_cli package"""
import sys

# local imports
from trello_cli import (ERRORS, SUCCESS, TRELLO_WRITE_ERROR, __app_name__, __version__, config)
from trello_cli.trello_service import TrelloService

# 3rd party imports
import typer
from typing_extensions import Annotated
from rich.console import Console
from rich.theme import Theme
from typing import Optional

app = typer.Typer(rich_markup_mode="markdown", add_completion=False)

custom_theme = Theme({
    "id": "blue",
})
console = Console(theme=custom_theme)


@app.command(rich_help_panel="1. Getting started")
def app_init() -> None:
    """Authenticates the user and loads trello boards into the app

     Initialization:
      1. locates user's api key and secret in a .env file in root dir
      2. generates an oauth token and secret.
      3. user's boards are loaded into the application.

    Usage:
    python3 -m trello_cli init


    """
    app_init_status = config.init()
    if app_init_status:
        typer.secho(
            f'Error initializing application: {ERRORS[app_init_status]}',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    service_res = TrelloService().get_trello_boards()
    if service_res.status_code != SUCCESS:
        typer.secho(
            f'Error initializing service: {ERRORS[service_res.status_code]}',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    else:
        boards = service_res.res
        console.rule(f"Trello boards")
        for board in boards:
            console.print(f"{board.name}, [id]id: {board.board_id}[/id]")


@app.command(rich_help_panel="2. Retrieve your trello object ID's")
def get_board(
        board_id: Annotated[str, typer.Option(prompt=True)]
) -> None:
    """Gets a board object

    Returns details of a board including list and label ID's 

    :param board_id: id of a trello board (sourced from running trello_cli app-init)
    :type board_id: str

    Usage:
    python3 -m trello_cli get-board "65352f31c09f6a38f8df1d0a"

    """
    board = TrelloService().get_board(board_id)
    if board.status_code != SUCCESS:
        typer.secho(
            f'Error getting board: {ERRORS[board.status_code]}',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        board = board.res
        lists = board.get_all_lists()
        labels = board.get_labels()
        console.print(f"loaded {board.name}: [id]id: {board.board_id}[/id]")

        console.rule(f"lists of {board.name}")
        for list in lists:
            console.print(f"{list.name}, [id]id: {list.list_id}[/id]")

        console.rule(f"labels of {board.name}")
        for label in labels:
            color = label.color
            console.print(f"label: {label.color}, [id]id: {label.label_id}[/id]")


@app.command(rich_help_panel="2. Retrieve your trello object ID's")
def get_cards(
        list_id: Annotated[str, typer.Option(prompt=True)]
) -> None:
    """Gets a list from a given trello board

    :param list_id: can be sourced from the parent board by running the get-board command
    :type list_id: str

    Usage: python3 -m trello_cli get-list "65352f31c09f6a38f8df1d0c"

    """
    trello_list = TrelloService().get_list(str(list_id))
    if trello_list.status_code != SUCCESS:
        typer.secho(
            f'Error getting list: {ERRORS[trello_list.status_code]}',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        trello_list = trello_list.res
        console.print(f"loaded {trello_list.name}: [id]id: {trello_list.list_id}[/id]")
        cards = trello_list.get_all_cards()
        console.rule(f"cards of {trello_list.name}")
        for card in cards:
            console.print(f"{card.name}, [id]id: {card.card_id}[/id]")


@app.command(rich_help_panel="2. Retrieve your trello object ID's")
def view_card(
        card_id: Annotated[str, typer.Option(prompt=True)]
) -> None:
    """Gets a card from a given trello list

    :param card_id: can be sourced from the parent list by running the get-list command
    :type card_id: str

    Usage:
    python3 -m trello_cli get-card "65352f31c09f6a38f8df1d59"

    """
    typer.echo("Getting card...")
    card = TrelloService().get_card(str(card_id))
    if card.status_code != SUCCESS:
        typer.secho(
            f'Error getting card: {ERRORS[card.status_code]}',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        card = card.res
        comments = card.get_comments()
        labels = card.get_labels()

        console.print(f"loaded {card.name}: [id]id: {card.card_id}[/id]")

        console.rule(f"comments of {card.name}")
        for comment in comments:
            console.print(f"{comment}")

        console.rule(f"labels of {card.name}")
        for label in labels:
            color = label.color
            console.print(f"{color},[id]id: {label.label_id}[/id]")


@app.command(rich_help_panel="3. Create trello objects")
def make_trello_card(
        list_id: Annotated[str, typer.Option(prompt=True)],
        name: Annotated[str, typer.Option(prompt=True)]
) -> None:
    """Creates a new card on a trello list

    :param list_id: can be sourced from the parent board by running the get-board command
    :type list_id: str

    Usage:
    python3 -m trello_cli create-card "65352f31c09f6a38f8df1d0c"

    """
    card = TrelloService().create_card(name, list_id)

    if card.status_code != SUCCESS:
        typer.secho(
            f'Error creating card: {ERRORS[card.status_code]}',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        card = card.res
        typer.secho(
            f"your card has been created :{card}",
            fg=typer.colors.GREEN,
        )


@app.command(rich_help_panel="3. Create trello objects")
def prepend_comment(
        card_id: Annotated[str, typer.Option(prompt=True)],
        text: Annotated[str, typer.Option(prompt=True)],
) -> None:
    """Creates a comment on a given trello card

    :param card_id: can be sourced from the parent list by running the get-list command
    :type card_id: str

    Usage:
    python3 -m trello_cli create-comment "65352f31c09f6a38f8df1d59"
    """

    comment = TrelloService().create_comment(card_id, text)
    if comment.status_code != SUCCESS:
        typer.secho(
            f'Error creating comment: {ERRORS[comment.status_code]}',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"your comment has been created :{comment.res}",
            fg=typer.colors.GREEN,
        )


@app.command(rich_help_panel="3. Create trello objects")
def prepend_label(
        card_id: Annotated[str, typer.Option(prompt=True)],
        label_id: Annotated[str, typer.Option(prompt=True)],
) -> None:
    """Adds a label to a trello card

    :param card_id: can be sourced from the parent list by running the get-list command
    :type card_id: str
    :param label_id: can be sourced from the parent board by running the get-board command
    :type label_id: str

    Usage:
    python3 -m trello_cli add-card-label "65352f31c09f6a38f8df1d59" "65352f31c09f6a38f8df1d65"

    """
    # checks if duplicate keys are passed
    if card_id == label_id:
        typer.secho(
            f'Error adding label: card_id and label_id cannot be the same',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    card_res = TrelloService().add_card_label(str(card_id), str(label_id))
    
    if card_res.status_code != SUCCESS:
        typer.secho(
            f'Error adding label: {ERRORS[card_res.status_code]}',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"your label has been added",
            fg=typer.colors.GREEN,
        )


def _version_callback(value: bool) -> None:
    """Callback for the version option
    :param value: bool value to check if version is requested
    """
    if value:
        typer.echo(f"{__app_name__} version {__version__}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
        version: Optional[bool] = typer.Option(
            None,
            "--version",
            "-v",
            help="Show the application's version and exit.",
            callback=_version_callback,
            is_eager=True)
) -> None:
    """Main entry point for trello_cli"""
    typer.secho("try 'trello_cli --help' for commands ", fg=typer.colors.GREEN)
    return
