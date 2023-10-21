# Overview 
A python CLI program for adding cards to a trello.com board. Users can: 
- Add a trello card with labels
- Add a comment to the specified column of board 


# Requirements
- Python 3.6 or higher
- Trello API key and token (see [here](https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/) for more information)


# Getting started and Usage 
## Installation
1. Clone the repository
2. Install the requirements: `pip install -r requirements.txt`
3. Create a `.env` file in the root directory of the project and add the following variables: 
```bash
$ENV:TRELLO_API_KEY = <your_trello_api_key>
$ENV:TRELLO_API_TOKEN = <your_trello_api_token>
$ENV:TRELLO_API_SECRET = <your_trello_api_secret>
```
4. Run the pacakge: `python3 -m trello_cli --help` to see the available commands and options
5. Follow the prompts to add a card or comment to a trello board
6. To run the tests: `python3 -m pytests tests/`




