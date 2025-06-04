from .rator import Rator

class Bop(Rator):
    """Binary operator node used in the CSE machine.
    
    This class represents a binary operation (an operation with two operands) 
    during RPAL program execution in the CSE machine. Examples include 
    arithmetic operations (+, -, *, /), comparison operations (eq, ne, gr, etc.), 
    and logical operations (and, or).
    
    When encountered during execution, the CSE machine will pop two values from 
    the stack, apply the operation, and push the result back to the stack.
    
    Attributes:
        data (str): The string representation of the binary operator (e.g., "+", "*", "eq")
    """
    
    def __init__(self, data):
        """Initialize a new binary operator with the specified operation.
        
        Args:
            data (str): The string representation of the binary operator to perform.
                       Common values include "+", "-", "*", "/", "eq", "ne", "gr", etc.
        """
        super().__init__(data)  # Initialize with operator name/symbol