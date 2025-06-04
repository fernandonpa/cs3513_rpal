from .symbol import Symbol

class Eta(Symbol):
    """Recursive function environment marker used in the CSE machine.
    
    This class represents a recursive function binding in the RPAL abstract machine.
    Eta nodes are used to implement recursive functions by establishing a reference
    to the function's own closure within its environment, allowing it to call itself.
    
    Attributes:
        index (int): A numeric identifier for this recursive binding
        environment (E): The environment in which this recursive function exists
        identifier (Symbol): The name of the recursive function
        lambda_ (Lambda): The function body of the recursive function
    """
    
    def __init__(self):
        """Initialize a new Eta node for recursive function binding.
        
        Creates an Eta node with null references that will be populated later
        to establish the recursive binding structure.
        """
        super().__init__("eta")  # Initialize as symbol with name 'eta'
        self.index = None        # Will hold the index for this recursive binding
        self.environment = None  # Will reference the environment containing this binding
        self.identifier = None   # Will hold the function name
        self.lambda_ = None      # Will reference the function implementation

    def set_index(self, i):
        """Set the index for this recursive binding.
        
        Args:
            i (int): The index value to set
        """
        self.index = i

    def get_index(self):
        """Get the index for this recursive binding.
        
        Returns:
            int: The current index value
        """
        return self.index

    def set_environment(self, e):
        """Set the environment for this recursive binding.
        
        Args:
            e (E): The environment in which this recursive function exists
        """
        self.environment = e

    def get_environment(self):
        """Get the environment for this recursive binding.
        
        Returns:
            E: The environment for this recursive function
        """
        return self.environment

    def set_identifier(self, identifier):
        """Set the identifier (name) for this recursive function.
        
        Args:
            identifier (Symbol): The name symbol for this recursive function
        """
        self.identifier = identifier

    def set_lambda(self, lambda_):
        """Set the lambda (function body) for this recursive function.
        
        Args:
            lambda_ (Lambda): The function implementation
        """
        self.lambda_ = lambda_

    def get_lambda(self):
        """Get the lambda (function body) for this recursive function.
        
        Returns:
            Lambda: The function implementation
        """
        return self.lambda_