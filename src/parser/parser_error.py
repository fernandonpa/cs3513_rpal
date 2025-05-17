class ParserError(Exception):
    """Base class for all parser errors"""
    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column
        
        location_info = ""
        if line is not None:
            location_info += f" at line {line}"
            if column is not None:
                location_info += f", column {column}"
                
        super().__init__(f"Parser error{location_info}: {message}")

class UnexpectedTokenError(ParserError):
    """Error raised when an unexpected token is encountered"""
    def __init__(self, expected, found, line=None, column=None):
        self.expected = expected
        self.found = found
        message = f"Expected {expected}, but found '{found}'"
        super().__init__(message, line, column)

class SyntaxError(ParserError):
    """Error raised for general syntax errors"""
    pass

class MissingTokenError(ParserError):
    """Error raised when a required token is missing"""
    def __init__(self, expected, line=None, column=None):
        message = f"Missing {expected}"
        super().__init__(message, line, column)