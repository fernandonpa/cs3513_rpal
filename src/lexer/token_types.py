from enum import Enum, auto

class TokenType(Enum):
    """Enum defining all token types in RPAL language"""
    # Keywords
    LET = auto()
    IN = auto()
    FN = auto()
    WHERE = auto()
    AUG = auto()
    OR = auto()
    AND = auto()
    NOT = auto()
    GR = auto()
    GE = auto()
    LS = auto()
    LE = auto()
    EQ = auto()
    NE = auto()
    TRUE = auto()
    FALSE = auto()
    NIL = auto()
    DUMMY = auto()
    WITHIN = auto()
    REC = auto()
    
    # Literals
    IDENTIFIER = auto()
    INTEGER = auto()
    STRING = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    POWER = auto()
    AT = auto()
    AMPERSAND = auto()
    ARROW = auto()
    EQUALS = auto()
    PIPE = auto()  # For the '|' operator
    
    # Special symbols
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    SEMICOLON = auto()
    COMMA = auto()
    
    # End of file
    EOF = auto()
    
    # For comment handling (not emitted as actual tokens)
    COMMENT = auto()


# Mapping of keywords to their token types (case insensitive)
KEYWORDS = {
    'let': TokenType.LET,
    'in': TokenType.IN,
    'fn': TokenType.FN,
    'where': TokenType.WHERE,
    'aug': TokenType.AUG,
    'or': TokenType.OR,
    'and': TokenType.AND,
    'not': TokenType.NOT,
    'gr': TokenType.GR,
    'ge': TokenType.GE,
    'ls': TokenType.LS,
    'le': TokenType.LE,
    'eq': TokenType.EQ,
    'ne': TokenType.NE,
    'true': TokenType.TRUE,
    'false': TokenType.FALSE,
    'nil': TokenType.NIL,
    'dummy': TokenType.DUMMY,
    'within': TokenType.WITHIN,
    'rec': TokenType.REC
}

# Mapping of operators to their token types
OPERATORS = {
    '+': TokenType.PLUS,
    '-': TokenType.MINUS,
    '*': TokenType.MULTIPLY,
    '/': TokenType.DIVIDE,
    '**': TokenType.POWER,
    '@': TokenType.AT,
    '&': TokenType.AMPERSAND,
    '->': TokenType.ARROW,
    '=': TokenType.EQUALS,
    '|': TokenType.PIPE  # Added pipe operator
}

# Mapping of punctuation to their token types
PUNCTUATION = {
    '(': TokenType.LEFT_PAREN,
    ')': TokenType.RIGHT_PAREN,
    ';': TokenType.SEMICOLON,
    ',': TokenType.COMMA
}