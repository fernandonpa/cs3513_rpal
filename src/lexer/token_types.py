from enum import Enum

class TokenType(Enum):
    """Enumeration of token types for RPAL lexical analysis.
    
    This enum defines the different categories of tokens that can be identified
    during the lexical analysis phase of the RPAL interpreter/compiler.
    
    Attributes:
        KEYWORD (int): Reserved words in the RPAL language.
        IDENTIFIER (int): Variable and function names.
        INTEGER (int): Numeric literal values.
        STRING (int): String literal values enclosed in quotes.
        END_OF_TOKENS (int): Special marker indicating the end of input.
        PUNCTUATION (int): Syntactic elements like parentheses, commas, etc.
        OPERATOR (int): Mathematical or logical operation symbols.
    """
    # Language keywords (e.g., 'let', 'in', 'fn', etc.)
    KEYWORD = 1
    
    # Identifiers represent variable names, function names, etc.
    IDENTIFIER = 2
    
    # Integer numeric literals
    INTEGER = 3
    
    # String literals (text enclosed in quotes)
    STRING = 4
    
    # Special token type to mark the end of the token stream
    END_OF_TOKENS = 5
    
    # Punctuation marks like parentheses, commas, semicolons, etc.
    PUNCTUATION = 6
    
    # Operators like +, -, *, /, etc.
    OPERATOR = 7