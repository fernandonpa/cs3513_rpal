from .rand import Rand

class Bool(Rand):
    """Boolean value node used in the CSE machine.
    
    This class represents a boolean literal value (true/false) during RPAL 
    program execution in the CSE machine. Boolean values can be used in 
    conditional expressions, logical operations, and as general values.
    
    Attributes:
        data (bool): The Python boolean value (True or False) represented by this node
    """
    
    def __init__(self, data):
        """Initialize a new Bool node with a boolean value.
        
        Args:
            data (bool): The Python boolean value (True or False) to store
                        in this node. This should be a Python bool type.
        """
        super().__init__(data)  # Initialize with the boolean value