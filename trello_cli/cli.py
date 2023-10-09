""" This module provides the CLi for the trello_cli package."""
# module imports
from trello_cli.helpers import *
from trello_cli.config import *
# dependencies
import typer
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from dotenv import find_dotenv, set_key

app = typer.Typer()
trello_api = trello_api()


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


def board_choices():
    return inquirer.select(
        message="Pick a board to work with :",
        choices=get_all_boards()
    ).execute()


def list_choices(board_id):
    lists = get_all_lists(board_id)
    if lists:
        return inquirer.select(
            message="Select a column to work with: ",
            choices=lists).execute()
    else:
        print("no lists")


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


def card_options():
    further_card_choices = [
        Choice("Retrieve a card"),
        Choice("Add a card"),
        Choice("Add a label"),
        Choice("Add a comment")
    ]

    return inquirer.select(
        message="Select one:", choices=further_card_choices, multiselect=False
    ).execute()


def color_pick():
    colors = [
        Choice("red"),
        Choice("yellow"),
        Choice("green"),
        Choice("blue")
    ]
    return inquirer.select(
        message="Select one:", choices=colors, multiselect=False
    ).execute()


@app.callback(invoke_without_command=True)
def main():
    selected_board = board_choices()
    selected_list = list_choices(selected_board.id)
    confirm_card_select = card_options()

    if confirm_card_select == "Retrieve a card":
        selected_card = card_choices(selected_list.id)
        get_card(selected_card.id)
        return

    elif confirm_card_select == "Add a card":
        name = typer.prompt("please give your card a name")
        new_card = create_card(str(name), selected_list.id)

        confirm_add_label = inquirer.confirm(
            message="Add label?",
            default=True,
            confirm_letter="y",
            reject_letter="n",
            transformer=lambda result: "yes" if result else "no",
        ).execute()

        if confirm_add_label:
            selected_label = label_choices(selected_board.id)
            add_card_label(new_card.id, selected_label.id)

        confirm_add_comment = inquirer.confirm(
            message="Add comment?",
            default=True,
            confirm_letter="y",
            reject_letter="n",
            transformer=lambda result: "yes" if result else "no",
        ).execute()

        if confirm_add_comment:
            text = inquirer.text(message="Write your comment here:", multiline=False).execute()
            create_comment(new_card.id, str(text))

        print(get_card(new_card.id))

    elif confirm_card_select == "Add a label":
        selected_card = card_choices(selected_list.id)
        selected_label = label_choices(selected_board.id)
        add_card_label(selected_card.id, selected_label.id)
        print(get_card(selected_card.id))

    elif confirm_card_select == "Add a comment":
        selected_card = card_choices(selected_list.id)
        text = inquirer.text(message="Write your comment here:", multiline=False).execute()
        create_comment(selected_card.id, str(text))
        print(get_card(selected_card.id))

    return
