from .rand import Rand

class Int(Rand):
    """Integer value node used in the CSE machine.
    
    This class represents integer literal values during RPAL program 
    execution in the CSE machine. Integer values can be used in arithmetic 
    operations, comparisons, and as general values in the program.
    
    Attributes:
        data (int): The Python integer value represented by this node
    """
    
    def __init__(self, data):
        """Initialize a new Int node with an integer value.
        
        Args:
            data (int): The Python integer value to store in this node
        """
        super().__init__(data)  # Initialize with the integer value