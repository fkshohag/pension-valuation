from rest_framework import status

__author__ = 'shohag'

class GenericException(Exception):
    message = 'error occurred.'

    def __init__(self, message, status_code=status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return repr(self.message)