class ParserError(Exception):
    """
    Custom exception class for handling parser errors.

    Attributes:
        message (str): The error message describing the parser issue.
    """
    def __init__(self, message):
        super().__init__(message)
        self.message = message