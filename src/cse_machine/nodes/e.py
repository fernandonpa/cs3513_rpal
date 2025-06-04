from .symbol import Symbol

class E(Symbol):
    """Environment node used in the CSE machine.
    
    This class represents an execution environment in the RPAL abstract machine.
    Environments store variable bindings and maintain the lexical scope during
    program execution. Each environment has a unique index and may have a parent
    environment, creating a chain for variable lookups.
    
    Attributes:
        index (int): A numeric identifier for this environment
        parent (E): Parent environment in the lexical scope chain
        is_removed (bool): Flag indicating if this environment has been removed
        values (dict): Dictionary mapping identifiers to their bound values
    """
    
    def __init__(self, i):
        """Initialize a new Environment.
        
        Args:
            i (int): The index value for this environment
        """
        super().__init__("e")  # Initialize as symbol with name 'e'
        self.index = i         # Store the numeric identifier
        self.parent = None     # Initially has no parent environment
        self.is_removed = False  # Not marked as removed initially
        self.values = {}       # Empty dictionary of variable bindings

    def set_parent(self, e):
        """Set the parent environment.
        
        Args:
            e (E): The parent environment to set
        """
        self.parent = e

    def get_parent(self):
        """Get the parent environment.
        
        Returns:
            E: The parent environment or None if this is a top-level environment
        """
        return self.parent

    def set_index(self, i):
        """Set the index for this environment.
        
        Args:
            i (int): The new index value to set
        """
        self.index = i
    
    def get_index(self):
        """Get the index for this environment.
        
        Returns:
            int: The current index value of this environment
        """
        return self.index

    def set_is_removed(self, is_removed):
        """Mark this environment as removed or not.
        
        Args:
            is_removed (bool): True if the environment should be marked as removed
        """
        self.is_removed = is_removed

    def get_is_removed(self):
        """Check if this environment is marked as removed.
        
        Returns:
            bool: True if the environment has been marked as removed
        """
        return self.is_removed

    def lookup(self, id):
        """Look up a variable in this environment or its ancestors.
        
        This method implements lexical scoping by first looking for the variable
        in the current environment, then checking parent environments if not found.
        
        Args:
            id (Symbol): The identifier to look up
            
        Returns:
            Symbol: The value bound to the identifier, or a new Symbol with the 
                   same name if not found (representing an unbound variable)
        """
        # Look for the variable in the current environment
        for key in self.values:
            if key.get_data() == id.get_data():
                return self.values[key]
                
        # If not found and we have a parent, try looking there
        if self.parent is not None:
            return self.parent.lookup(id)
        else:
            # Not found in any environment, return an unbound symbol
            return Symbol(id.get_data())