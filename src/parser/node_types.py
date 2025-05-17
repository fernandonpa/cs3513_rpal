from enum import Enum, auto

class NodeType(Enum):
    """
    Enumeration of all possible node types in the RPAL abstract syntax tree
    """
    # Program structure
    LET = auto()
    WHERE = auto()
    WITHIN = auto()
    REC = auto()
    AND = auto()
    
    # Function-related
    LAMBDA = auto()
    GAMMA = auto()
    FCN_FORM = auto()
    
    # Tuple operations
    TAU = auto()
    AUG = auto()
    
    # Conditionals
    CONDITIONAL = auto()
    
    # Boolean operators
    OR = auto()
    AND_OP = auto()
    NOT = auto()
    
    # Comparison operators
    GT = auto()  # greater than
    GE = auto()  # greater or equal
    LT = auto()  # less than
    LE = auto()  # less or equal
    EQ = auto()  # equal
    NE = auto()  # not equal
    
    # Arithmetic operators
    PLUS = auto()
    MINUS = auto()
    TIMES = auto()
    DIVIDE = auto()
    POWER = auto()
    NEGATE = auto()
    
    # Other operators
    AT = auto()
    COMMA = auto() 
    EQUAL = auto()
    
    # Literals and identifiers
    IDENTIFIER = auto()
    INTEGER = auto()
    STRING = auto()
    TRUE = auto()
    FALSE = auto()
    NIL = auto()
    DUMMY = auto()
    EMPTY = auto()

# Mapping of comparison operators from string to node type
COMPARISON_OPS = {
    'gr': NodeType.GT,
    '>': NodeType.GT,
    'ge': NodeType.GE,
    '>=': NodeType.GE,
    'ls': NodeType.LT,
    '<': NodeType.LT,
    'le': NodeType.LE, 
    '<=': NodeType.LE,
    'eq': NodeType.EQ,
    'ne': NodeType.NE
}