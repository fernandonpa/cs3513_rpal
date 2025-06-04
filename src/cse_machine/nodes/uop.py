from .rator import Rator

class Uop(Rator):
    """Unary operator node used in the CSE machine.
    
    This class represents a unary operation (an operation with one operand) 
    during RPAL program execution in the CSE machine. Examples include 
    negation (-), logical not (not), and other single-operand operations.
    
    When encountered during execution, the CSE machine will pop one value from
    the stack, apply the operation, and push the result back to the stack.
    
    Attributes:
        data (str): The string representation of the unary operator (e.g., "neg", "not")
    """
    
    def __init__(self, data):
        """Initialize a new unary operator with the specified operation.
        
        Args:
            data (str): The string representation of the unary operator to perform.
                       Common values include "neg" for negation and "not" for logical not.
        """
        super().__init__(data)  # Initialize with the operator name/symbol