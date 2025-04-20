from .token_types import TokenType
from .lexer_error import InvalidTokenError

class Token:
    """
    Class representing a token in the RPAL language
    
    Attributes:
        type (TokenType): The type of token
        value (str): The string value of the token
        line (int): Line number where the token appears
        column (int): Column number where the token starts
    """
    
    def __init__(self, token_type, value, line=1, column=1):
        """
        Initialize a new Token
        
        Args:
            token_type (TokenType): The type of token
            value (str): The string value of the token
            line (int, optional): Line number where the token appears. Defaults to 1.
            column (int, optional): Column number where the token starts. Defaults to 1.
            
        Raises:
            InvalidTokenError: If token_type is not a valid TokenType
        """
        if not isinstance(token_type, TokenType):
            raise InvalidTokenError(f"Invalid token type: {token_type}")
        
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column
    
    def __str__(self):
        """String representation of the token"""
        return f"Token({self.type.name}, '{self.value}', line={self.line}, col={self.column})"
    
    def __repr__(self):
        """Formal string representation of the token"""
        return self.__str__()
    
    def __eq__(self, other):
        """
        Check if two tokens are equal
        
        Args:
            other (Token): Another token to compare with
            
        Returns:
            bool: True if tokens are equal, False otherwise
        """
        if not isinstance(other, Token):
            return False
            
        return (self.type == other.type and 
                self.value == other.value and 
                self.line == other.line and 
                self.column == other.column)