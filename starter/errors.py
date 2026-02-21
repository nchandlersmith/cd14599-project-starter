"""Custom errors go here"""


class FieldValidationError(Exception):
    """
    Custom exception for field validation errors.
    Attributes:
        message (str): The error message describing the validation error.
        status_code (int): The HTTP status code to return when this error 
        is raised (default is 400 for Bad Request).
    """

    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
