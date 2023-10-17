# local imports
from trello_cli import (ERRORS, SUCCESS, __app_name__, __version__, config)
from trello_cli.trello_service import TrelloService

# 3rd party imports
import typer

app = typer.Typer()
trello_service = TrelloService()


@app.command()
def init() -> None:
    """Initializes the application by authenticating the user and then loads
    the user's boards into the application.

    In order for the user to be successfully authenticated, the user must visit
    https://trello.com/app-key to obtain an API key and secret.This must be stored
    in an .env file in the root directory of the package.

    During initialisation, the app locates the user's api key and secret and
    generates an oauth token and secret. This is stored in the .env file.
    Once complete, the user's boards are loaded into the application.

    Authentication is only required once.


    Examples
    --------
    python -m trello_cli init
    Initializing application...
    your boards have been loaded:[<Board Meal Planning>]

    """
    typer.echo("Initializing application...")
    app_init_error = config.init()
    if app_init_error:
        typer.secho(
            f'Error initializing application: {ERRORS[app_init_error]}',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    service_res = trello_service.init_trello()
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
    """CLI command to get a trello board from user's account

    Parameters
    ----------
    board_id: str
        id required for retrieving a board can be sourced from the parent
        board by running the get-board command


    Examples
    --------
    python -m trello_cli get-board "6526f7f91942a8eb420c84cc"
    your board has been loaded :[<Board Meal Planning>]
    lists: [<List Guidelines>]


    """
    board = trello_service.get_board(board_id)
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


@app.command()
def get_list(
        list_id: str
) -> None:
    """ CLI command to get a list from a specific trello board

    Parameters
    ----------
    list_id: str
        required for retrieval from a trello board. Can be sourced
        from the parent board by running the get-board command

    Examples
    --------
    python -m trello_cli get-list "6523e63b8e337f3ce55311a3"
    your list has been loaded :[<List Guidelines>]
    cards: [<Card Grid-Based Design>]

    """
    trello_list = trello_service.get_list(str(list_id))
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
    """ CLI command to gets a card from a trello list

    Parameters
    ----------
    card_id: str
        id required for retrieving a card. Can be sourced from
        the parent list by running the get-list command

    Examples
    --------
    python -m trello_cli get-card "6523e63b8e337f3ce55312f5"
    your card has been loaded :[<Card Grid-Based Design>]
    comments: [<Comment This is a test comment>]
    labels: [<Label green>]

    """
    typer.echo("Getting card...")
    card = trello_service.get_card(str(card_id))
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
    """CLI command to create a card from a trello board

    Parameters
    ----------
    list_id: str
        id for retrieving a list from a trello board. Can be sourced
        from the parent board by running the get-board command

    Examples
    --------
    python -m trello_cli create-card "6523e63b8e337f3ce55311a3"
    Enter your card name: test
    your card has been created :[<Card test>]

    """
    name = typer.prompt("Enter your card name")
    card = trello_service.create_card(name, list_id)

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
    """CLI command to create a comment from a trello card

    Parameters
    ----------
    card_id: str
        id for retrieving a card from a trello board to add a
        comment to. Can be sourced from the parent list by running
        the get-list command


    Examples
    --------
    python -m trello_cli create-comment "6523e63b8e337f3ce55312f5"
    Enter your comment: This is a test comment
    your comment has been created :[<Comment This is a test comment>]
    """
    text = typer.prompt("Enter your comment")
    comment = trello_service.create_comment(card_id, text)
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
    """CLI command to add a label to a trello card

    Parameters
    ----------
    card_id: str
        id of card to add label to. Can be sourced from the parent
        list by running the get-list command

    label_id: str
        id of desired label to add to card. Can be sourced from the
        parent board by running the get-board command

    Examples
    --------
    python -m trello_cli add-card-label "6523e63b8e337f3ce55312f5" "6523e63b8e337f3ce55312f5"
    your label has been added

    """
    card = trello_service.add_card_label(card_id, label_id)
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
def main() -> None:
    return
