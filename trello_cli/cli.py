"""This module provides the Trello CLI."""

from typing import Optional

import typer

from trello_cli import (
    ERRORS, SUCCESS, __app_name__, __version__, config)

from trello_cli.trello_service import TrelloService
from trello_cli.models import *

app = typer.Typer()
trello_service = TrelloService()


@app.command()
def init(
        verbose: Optional[bool] = typer.Option(
            False,
            "--verbose",
            "-v",
            help="Show more information about what the application is doing.",
        )
) -> None:
    """Initialize the application and load trello boards"""
    if verbose:
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


def _version_callback(value: bool) -> None:
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
            is_eager=True
        )
) -> None:
    return
