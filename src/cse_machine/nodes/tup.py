from .rand import Rand

class Tup(Rand):
    """Tuple value node used in the CSE machine.
    
    This class represents tuple values during RPAL program execution in the CSE machine.
    Tuples are compound data structures that can hold multiple values of different types.
    They are created by the tau operator and can be used for structured data storage,
    pattern matching, and returning multiple values from functions.
    
    Attributes:
        symbols (list): List of symbols (values) contained in this tuple
    """
    
    def __init__(self):
        """Initialize a new Tup node.
        
        Creates an empty tuple that can store multiple values. The tuple is
        initially created with the fixed name "tup" and an empty list of symbols.
        """
        super().__init__("tup")  # Initialize with the name "tup"
        self.symbols = []       # Initialize empty list for tuple elements