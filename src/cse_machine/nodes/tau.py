from .symbol import Symbol

class Tau(Symbol):
    """Tuple constructor node used in the CSE machine.
    
    This class represents tuple construction in the RPAL language during CSE
    machine execution. Tau nodes combine multiple values into a single tuple value,
    allowing compound data to be created and manipulated.
    
    When encountered during execution, the CSE machine pops n values from the stack
    and combines them into a tuple structure.
    
    Attributes:
        n (int): The number of elements in the tuple
    """
    
    def __init__(self, n):
        """Initialize a new Tau node for tuple construction.
        
        Args:
            n (int): The number of elements this tuple will contain
        """
        super().__init__("tau")  # Initialize as symbol with name 'tau'
        self.set_n(n)          # Set the tuple size

    def set_n(self, n):
        """Set the number of elements in this tuple.
        
        Args:
            n (int): The number of elements
        """
        self.n = n

    def get_n(self):
        """Get the number of elements in this tuple.
        
        Returns:
            int: The number of elements
        """
        return self.n