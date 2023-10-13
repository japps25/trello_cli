""" This module provides the CLi for the trello_cli package."""


# dependencies
import typer
from InquirerPy import inquirer
import time

from dotenv import find_dotenv, set_key
from rich import print
from time import sleep
from rich.console import Console
from rich.panel import Panel
import os
# module imports
from trello_cli.helpers import *

app = typer.Typer()
console = Console()


delay = 1.2
card_width = 50


def init():
    if not check_api_tokens():
        typer.echo("Exiting app")
        raise typer.Exit(1)
    elif check_oauth_tokens():
        typer.echo("Authentication success")
        return
    else:
        typer.echo("Please try again")
        init()


def check_api_tokens() -> bool:
    console.print("Checking api tokens...")
    if os.getenv("TRELLO_API_TOKEN") and os.getenv("TRELLO_API_SECRET"):
        return True


def check_oauth_tokens():
    print("checking oauth tokens...")
    if os.getenv("TRELLO_OAUTH_TOKEN") and os.getenv("TRELLO_OAUTH_SECRET"):
        console.print("retrieved oauth tokens")
        return True
    else:
        console.print("fetching oauth1 tokens")
        access_token = create_oauth_token()
        if access_token is None:
            typer.secho("Authentication has failed")
            return False
        else:
            save_auth_credentials(access_token)
            return True


def save_auth_credentials(access_token) -> None:
    dotenv_path = find_dotenv()
    set_key(
        dotenv_path=dotenv_path,
        key_to_set="TRELLO_OAUTH_TOKEN",
        value_to_set=access_token['oauth_token']
    )
    set_key(
        dotenv_path=dotenv_path,
        key_to_set="TRELLO_OAUTH_SECRET",
        value_to_set=access_token['oauth_token_secret']
    )


def main_menu():
    print(" trello_cli is a command line app that helps you manage your trello cards")

    selected_board = inquirer.select(
        message="Pick a board to work with:",
        choices=get_all_boards()
    ).execute()

    lists = get_all_lists(selected_board.id)

    selected_list = inquirer.select(
        message="Pick a list to work with:",
        choices=lists
    ).execute()

    card_actions(selected_list.id, selected_board.id)


def card_actions(list_id: str, board_id: str):
    card_action = inquirer.select(
        message="Select an action:",
        choices=[
            "Retrieve a card",
            "Add a card",
            "Update card",
            "Main Menu"
        ]
    ).execute()

    if card_action == "Retrieve a card":

        selected_card = retrieve_trello_card(list_id)
        console.print(Panel(selected_card, width=card_width))

        choices = inquirer.select(
            message="Select an action:",
            choices=[
                "View comments",
                "Main Menu"
            ]
        ).execute()

        if choices == "View comments":
            view_comments(selected_card.id)
        elif choices == "Main Menu":
            main_menu()

    elif card_action == "Add a card":
        name = typer.prompt("please give your card a name")
        new_card = create_card(str(name), list_id)
        console.print(Panel(new_card))
        card_additions(new_card.id, board_id)

    elif card_action == "Update card":
        selected_card = retrieve_trello_card(list_id)
        card_additions(selected_card.id, board_id)

    else:
        return main_menu()


def card_additions(card_id, board_id):
    confirm_add_label = inquirer.confirm(
        message="Add label?",
        default=True,
        confirm_letter="y",
        reject_letter="n",
        transformer=lambda result: "yes" if result else "no",
    ).execute()

    if confirm_add_label:
        add_trello_label(card_id, board_id)

        choices = inquirer.select(
            message="Select an action:",
            choices=[
                "View Card",
                "Main Menu"
            ]
        ).execute()

        if choices == "View Card":
            card = get_card(card_id)
            console.print(Panel(card), width=card_width)
            sleep(delay)

        if choices == "Main Menu":
            main_menu()

    confirm_add_comment = inquirer.confirm(
        message="Add comment?",
        default=True,
        confirm_letter="y",
        reject_letter="n",
        transformer=lambda result: "yes" if result else "no",
    ).execute()

    if confirm_add_comment:
        add_trello_comment(card_id)

        choices = inquirer.select(
            message="Select an action:",
            choices=[
                "View comments",
                "Main Menu"
            ]
        ).execute()

        if choices == "View comments":
            view_comments(card_id)
            main_menu()
        elif choices == "Main Menu":
            main_menu()


def label_choices(selected_board):
    labels = get_labels(selected_board)
    if labels:
        return inquirer.select(
            message="Pick a label to add :",
            choices=labels
        ).execute()
    else:
        print("no labels")


def card_choices(list_id):
    cards = get_all_cards(list_id)

    if cards:
        return inquirer.select(
            message="Pick a card to work with :",
            choices=cards
        ).execute()
    else:
        print("no cards")


def add_trello_label(card_id, board_id):
    selected_label = label_choices(board_id)
    add_card_label(card_id, selected_label.id)
    return


def add_trello_comment(card_id):
    text = inquirer.text(message="Write your comment here:", multiline=False).execute()
    create_comment(card_id, str(text))


def retrieve_trello_card(list_id):
    selected_card = card_choices(list_id)
    card = get_card(selected_card.id)
    return card


def view_comments(card_id):
    comments = get_comments(card_id)
    if comments:
        console.print(Panel(comments, width=80))
    else:
        sleep(delay)
        console.print("returning to main menu")
        sleep(delay)
        main_menu()
    return


@app.callback(invoke_without_command=True)
def main():
    init()
    main_menu()
