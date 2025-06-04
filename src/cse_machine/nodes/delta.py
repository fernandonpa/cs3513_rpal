from .symbol import Symbol

class Delta(Symbol):
    """Environment marker symbol used in the CSE machine.
    
    This class represents an environment boundary in the RPAL abstract machine.
    Delta nodes are used during the standardization process to mark where new
    environments should be created during execution, typically at function
    boundaries. Each Delta has a unique index that helps locate the corresponding
    environment during runtime.
    
    Attributes:
        index (int): A numeric identifier for this environment marker
        symbols (list): List of symbols defined in this environment scope
    """
    
    def __init__(self, i):
        """Initialize a new Delta environment marker.
        
        Args:
            i (int): The index value for this Delta, used to identify
                    the corresponding environment during execution
        """
        super().__init__("delta")  # Initialize as symbol with name 'delta'
        self.index = i           # Store the numeric identifier for this environment
        self.symbols = []        # Initialize empty list of symbols for this environment
    
    def set_index(self, i):
        """Set the index for this Delta environment marker.
        
        Args:
            i (int): The new index value to set
        """
        self.index = i
    
    def get_index(self):
        """Get the index for this Delta environment marker.
        
        Returns:
            int: The current index value of this Delta
        """
        return self.index