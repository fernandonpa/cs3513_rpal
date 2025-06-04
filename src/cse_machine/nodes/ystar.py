from .symbol import Symbol

class Ystar(Symbol):
    """Fixed-point combinator symbol used in the CSE machine.
    
    This class represents the Y* (Y-star) fixed-point combinator in the RPAL language.
    The Y* combinator is used for implementing recursion through self-application,
    allowing functions to refer to themselves without requiring explicit recursive
    definitions.
    
    When encountered during execution, the CSE machine uses the Y* combinator to
    transform non-recursive functions into recursive ones by providing a mechanism
    for self-reference.
    """
    
    def __init__(self):
        """Initialize a new Ystar (Y*) combinator symbol.
        
        Creates a Y* node with the fixed representation "<Y*>" that identifies
        it as the fixed-point combinator in the CSE machine.
        """
        super().__init__("<Y*>")  # Initialize with the fixed representation "<Y*>"