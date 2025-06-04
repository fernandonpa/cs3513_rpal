class Symbol:
    """Base symbol class used in the CSE machine.
    
    This class serves as the fundamental building block for all nodes in the
    CSE machine representation of RPAL programs. It provides storage for a 
    data value and basic accessor methods.
    
    All other node types in the CSE machine (operators, operands, control
    structures) inherit from this base class.
    
    Attributes:
        data: The value or name associated with this symbol
    """
    
    def __init__(self, data):
        """Initialize a new Symbol with the given data.
        
        Args:
            data: The value or name to associate with this symbol
        """
        self.data = data  # Store the symbol's value or name

    def set_data(self, data):
        """Set the data value for this symbol.
        
        Args:
            data: The new value to associate with this symbol
        """
        self.data = data

    def get_data(self):
        """Get the data value for this symbol.
        
        Returns:
            The value associated with this symbol
        """
        return self.data