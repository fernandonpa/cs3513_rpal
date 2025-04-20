class LexerError(Exception):
    """Base exception for all lexer errors"""
    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(self._format_message())
    
    def _format_message(self):
        location = ""
        if self.line is not None:
            location += f" at line {self.line}"
            if self.column is not None:
                location += f", column {self.column}"
        
        return f"Lexer error{location}: {self.message}"


class UnexpectedCharacterError(LexerError):
    """Raised when the lexer encounters an unexpected character"""
    def __init__(self, char, line, column):
        super().__init__(f"Unexpected character '{char}'", line, column)


class InvalidTokenError(LexerError):
    """Raised when an invalid token is constructed"""
    pass


class UnclosedStringError(LexerError):
    """Raised when a string literal is not properly closed"""
    def __init__(self, line, column):
        super().__init__("Unclosed string literal", line, column)