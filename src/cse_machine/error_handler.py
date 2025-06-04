"""
This module defines custom exceptions for handling errors in the CSE Machine.
"""

class CSEMachineError(Exception):
    """
    Custom exception class for handling errors in the CSE Machine.

    Attributes:
        message (str): The error message describing the issue.
    """
    def __init__(self, message):
        super().__init__(message)
        self.message = message