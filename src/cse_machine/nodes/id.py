from .rand import Rand

class Id(Rand):
    """Identifier node used in the CSE machine.
    
    This class represents variable identifiers in the RPAL language during
    CSE machine execution. When encountered, identifiers are looked up in
    the current environment to retrieve their bound values.
    
    Identifiers serve as references to values stored in the environment,
    allowing variables to be used in expressions and functions.
    
    Attributes:
        data (str): The name of the identifier (variable name)
    """
    
    def __init__(self, data):
        """Initialize a new identifier node.
        
        Args:
            data (str): The name of the identifier/variable
        """
        super().__init__(data)  # Initialize with the identifier name
    
    def get_data(self):
        """Get the name of this identifier.
        
        Returns:
            str: The identifier's name
        """
        return super().get_data()  # Return the identifier name from parent class