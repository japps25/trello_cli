
__app_name__ = 'trello_cli'
__version__ = '0.1.0'

( 
    SUCCESS,
    TRELLO_WRITE_ERROR, 
    TRELLO_READ_ERROR
) = range(3)


ERRORS = {
    TRELLO_WRITE_ERROR: 'Error writing to Trello',
    TRELLO_READ_ERROR: 'Error reading from Trello'
}