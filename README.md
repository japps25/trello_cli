# Overview 
A python CLI program for adding cards to a trello.com board. Given a trello board specified by the User, the app can:
- Add a trello card to a list 
- Add labels to a card
- Add a comment to a card

Future features:
- The ability to discard closed trello objects 
- Delete trello objects from account 


# Requirements
- Python 3.6 or higher
- Trello API key, token and secret (see [here](https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/) for more information)


# Getting started and Usage 
## Installation
1. Clone the repository
2. Install the requirements: `pip install -r requirements.txt`
3. Create a `.env` file in the root directory of the project and add the following variables: 
```bash
TRELLO_API_KEY = <your_trello_api_key>
TRELLO_API_TOKEN = <your_trello_api_token>
TRELLO_API_SECRET = <your_trello_api_secret>
```
4. Run the package: `python3 -m trello_cli --help` to see the available commands and options
5. Follow the prompts to add a card or comment to a trello board
6. To run the tests: `python3 -m pytests tests/`




