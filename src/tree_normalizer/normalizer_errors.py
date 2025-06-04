"""
This module defines custom exceptions for tree normalization errors.
"""

class NormalizerError(Exception):
    """
    Custom exception class for handling tree normalization errors.

    Attributes:
        message (str): The error message describing the normalization issue.
    """
    def __init__(self, message):
        super().__init__(message)
        self.message = message