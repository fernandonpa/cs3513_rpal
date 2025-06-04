from .symbol import Symbol

class Rand(Symbol):
    """Operand base class used in the CSE machine.
    
    This class serves as a base class for all operand types in the RPAL language,
    including literals (Int, Str, Bool) and identifiers. Operands represent values
    that can be used in expressions and passed to functions.
    
    Attributes:
        data: The value represented by this operand
    """
    
    def __init__(self, data):
        """Initialize a new operand with a value.
        
        Args:
            data: The value to store in this operand
        """
        super().__init__(data)  # Initialize with the operand's value

    def get_data(self):
        """Get the value of this operand.
        
        Returns:
            The value stored in this operand
        """
        return super().get_data()  # Return the value from parent class