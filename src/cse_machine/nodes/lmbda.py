from .symbol import Symbol

class Lambda(Symbol):
    """Lambda abstraction node used in the CSE machine.
    
    This class represents a function (lambda abstraction) during RPAL program
    execution. Lambda nodes hold environment information, parameter identifiers,
    and the function body, forming closures that capture variables from their
    defining scope.
    
    Attributes:
        index (int): A numeric identifier for this lambda
        environment (E): The environment in which this lambda was defined
        identifiers (list): List of parameter names expected by this function
        delta (Delta): Reference to the delta node marking function's environment boundary
    """
    
    def __init__(self, i):
        """Initialize a new Lambda node.
        
        Args:
            i (int): The index value for this lambda
        """
        super().__init__("lambda")  # Initialize as symbol with name 'lambda'
        self.index = i            # Store the numeric identifier
        self.environment = None   # Will reference the defining environment
        self.identifiers = []     # Will store parameter names
        self.delta = None         # Will reference the function's delta node

    def set_environment(self, n):
        """Set the environment for this lambda.
        
        Args:
            n (E): The environment in which this lambda is defined
        """
        self.environment = n

    def get_environment(self):
        """Get the environment for this lambda.
        
        Returns:
            E: The environment in which this lambda was defined
        """
        return self.environment

    def set_delta(self, delta):
        """Set the delta node for this lambda.
        
        Args:
            delta (Delta): The delta node marking this function's environment boundary
        """
        self.delta = delta

    def get_delta(self):
        """Get the delta node for this lambda.
        
        Returns:
            Delta: The delta node for this function
        """
        return self.delta
        
    def get_index(self):
        """Get the index for this lambda.
        
        Returns:
            int: The index value
        """
        return self.index