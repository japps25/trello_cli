""" Top-level package for the trello_cli"""

__app_name__ = 'trello_cli'
__version__ = '0.1.0'

(
    SUCCESS,
    TRELLO_READ_ERROR,
    TRELLO_WRITE_ERROR,
    TRELLO_AUTHENTICATION_ERROR,
    OAUTH1_ERROR,

) = range(5)

ERRORS = {
    TRELLO_READ_ERROR: "trello read error",
    TRELLO_WRITE_ERROR: "trello write error",
    TRELLO_AUTHENTICATION_ERROR: "trello api authentication error",
    OAUTH1_ERROR: "oauth1 error"
}
