""" Module to define the CLI commands for the trello_cli package"""
from typing import Optional

# local imports
from trello_cli import (ERRORS, SUCCESS, __app_name__, __version__, config)
from trello_cli.trello_service import TrelloService

# 3rd party imports
import typer

app = typer.Typer()

@app.command()
def init() -> None:
    """Authenticates the user and initialises the application. Only required once.

     Initialization:
      1. locates user's api key and secret in a .env file in root dir
      2. generates an oauth token and secret.
      3. user's boards are loaded into the application.

    Usage:
    python3 -m trello_cli init


    """
    typer.echo("Initializing application...")
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
        typer.secho(
            f"your boards have been loaded:{service_res.res}",
            fg=typer.colors.GREEN,
        )


@app.command()
def get_board(
        board_id: str
) -> None:
    """Gets a trello board from the user's account. 

    Returns board details including name, id and a set of labels

    :param board_id:  can be sourced from the parent board by running the get-board command
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
        typer.secho(
            f"your board has been loaded :{board.res}",
            fg=typer.colors.GREEN,
        )
        typer.secho(
            f"lists: {board[0].get_all_lists()}",
            fg=typer.colors.GREEN,
        )
        typer.secho(
            f"labels:  {board[0].get_labels()}",
            fg=typer.colors.GREEN,
        )


@app.command()
def get_list(
        list_id: str
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
        typer.secho(
            f"your list has been loaded :{trello_list.res}",
            fg=typer.colors.GREEN,
        )
        typer.secho(
            f"cards: {trello_list.res.get_all_cards()}",
            fg=typer.colors.GREEN,
        )


@app.command()
def get_card(
        card_id: str
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
        typer.secho(
            f"your card has been loaded :{card.res}",
            fg=typer.colors.GREEN,
        )
        typer.secho(
            f"comments: {card.res.get_comments()}",
            fg=typer.colors.GREEN,
        )
        typer.secho(
            f"labels: {card.res.labels}",
            fg=typer.colors.GREEN,
        )


@app.command()
def create_card(
        list_id=typer.Argument(...)
) -> None:
    """Creates a new card on a trello list

    :param list_id: can be sourced from the parent board by running the get-board command
    :type list_id: str

    Usage:
    python3 -m trello_cli create-card "65352f31c09f6a38f8df1d0c"

    """
    name = typer.prompt("Enter your card name")
    card = TrelloService().create_card(name, list_id)

    if card.status_code != SUCCESS:
        typer.secho(
            f'Error creating card: {ERRORS[card.status_code]}',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"your card has been created :{card.res}",
            fg=typer.colors.GREEN,
        )


@app.command()
def create_comment(
        card_id=typer.Argument(...)
) -> None:
    """Creates a comment on a given trello card

    :param card_id: can be sourced from the parent list by running the get-list command
    :type card_id: str

    Usage:
    python3 -m trello_cli create-comment "65352f31c09f6a38f8df1d59"
    """
    text = typer.prompt("Enter your comment")
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


@app.command()
def add_card_label(
        card_id=typer.Argument(...),
        label_id: str = typer.Argument(...)
) -> None:
    """Adds a label to a trello card

    :param card_id: can be sourced from the parent list by running the get-list command
    :type card_id: str
    :param card_id: can be sourced from the parent list by running the get-list command
    :type card_id: str
    :param label_id: can be sourced from the parent board by running the get-board command
    :type label_id: str

    Usage:
    python3 -m trello_cli add-card-label "65352f31c09f6a38f8df1d59" "65352f31c09f6a38f8df1d65"

    """
    card = TrelloService().add_card_label(card_id, label_id)
    if card.status_code != SUCCESS:
        typer.secho(
            f'Error adding label: {ERRORS[card.status_code]}',
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


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return
