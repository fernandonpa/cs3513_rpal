from .symbol import Symbol

class Rator(Symbol):
    """Operator base class used in the CSE machine.
    
    This class serves as a base class for all operators in the RPAL language,
    including arithmetic, logical, and comparison operators. Operators take
    operands and produce results during program execution.
    
    Attributes:
        data (str): The string representation of the operator (e.g., "+", "*")
    """
    
    def __init__(self, data):
        """Initialize a new operator with the specified operation.
        
        Args:
            data (str): The string representation of the operator
        """
        super().__init__(data)  # Initialize with the operator's symbol