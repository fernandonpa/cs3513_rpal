"""
This module defines a custom exception for lexer errors.
"""

class LexerError(Exception):
    """
    Custom exception class for handling lexer errors.

    Attributes:
        message (str): The error message describing the lexer issue.
    """
    def __init__(self, message):
        super().__init__(message)
        self.message = message