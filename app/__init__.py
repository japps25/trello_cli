#trello_cli/__init__.py

__app_name__ = 'trello_cli'
__version__ = '0.1.0'

( 
    SUCCESS,
    TELLO_WRITE_ERROR, 
    TRELLO_READ_ERROR,
    TRELLO_UPDATE_ERROR,

) = range(3)


ERRORS = {
    TELLO_WRITE_ERROR: 'Error writing to Trello',
    TRELLO_READ_ERROR: 'Error reading from Trello',
    TRELLO_UPDATE_ERROR: 'Error updating Trello'
}