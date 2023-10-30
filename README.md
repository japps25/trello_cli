# Overview

A python CLI program for adding cards to a trello board. Given a board specified by the user:

- Add a trello card to a list
- Add labels to a card
- Add a comment to a card

#### Future features:

- Filter closed trello objects
- Delete trello objects from account
- Render trello objects in the terminal

## Requirements

- Python 3.6 or higher
- Trello API key, token and secret (
  see [here](https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/) for more information)

## Installation

1. Clone the repository
2. Install the requirements: `pip install -r requirements.txt`
3. Create a `.env` file in the root directory of the project and add the following variables:

```bash
TRELLO_API_KEY = <your_trello_api_key>
TRELLO_API_TOKEN = <your_trello_api_token>
TRELLO_API_SECRET = <your_trello_api_secret>
```

## Usage

1. Run the package:
    1. `python3 -m trello_cli init` to initialize the app and load trello boards with their id's and names
    2. `python3 -m trello_cli --help` to see the available commands and options
     
    3. Check for required id's by running the command with the `--help` flag. For example, to add a card to a trello
       list, run `python3 -m trello_cli add_card --help` to see the required id and usage example
     
2. To run the tests: `python3 -m pytests tests/`




