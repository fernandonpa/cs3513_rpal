from .rand import Rand

class Str(Rand):
    """String value node used in the CSE machine.
    
    This class represents string literal values during RPAL program
    execution in the CSE machine. String values can be used in
    string operations, printed as output, or used as general values.
    
    Attributes:
        data (str): The Python string value represented by this node
    """
    
    def __init__(self, data):
        """Initialize a new Str node with a string value.
        
        Args:
            data (str): The Python string value to store in this node
        """
        super().__init__(data)  # Initialize with the string value