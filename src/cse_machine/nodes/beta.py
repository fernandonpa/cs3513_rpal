from .symbol import Symbol

class Beta(Symbol):
    """Lambda abstraction symbol used in the CSE machine.
    
    This class represents a lambda abstraction (function) in the RPAL language
    during CSE machine execution. A Beta node is created during standardization
    of lambda expressions and marks the beginning of a function body.
    
    When encountered during execution, the CSE machine uses Beta nodes to
    create closures by capturing the current environment with the function body.
    """
    
    def __init__(self):
        """Initialize a new Beta symbol.
        
        Creates a Beta node that represents a lambda abstraction in the
        standardized control tree. The 'beta' identifier is used by the
        CSE machine to identify function entry points.
        """
        super().__init__("beta")  # Initialize as symbol with name 'beta'