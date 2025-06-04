from .symbol import Symbol

class Gamma(Symbol):
    """Function application symbol used in the CSE machine.
    
    This class represents function application in the RPAL abstract machine.
    When a Gamma node is encountered during execution, the CSE machine applies
    the function (rator) to the argument (rand) by:
    
    1. Popping the argument value from the stack
    2. Popping the function value from the stack
    3. Applying the function to the argument
    4. Pushing the result back onto the stack
    
    Gamma nodes are fundamental to the CSE machine's execution model and
    implement the core evaluation strategy of the RPAL language.
    """
    
    def __init__(self):
        """Initialize a new Gamma node for function application.
        
        Creates a Gamma node with the fixed name "gamma" to represent
        function application in the standardized control tree.
        """
        super().__init__("gamma")  # Initialize as symbol with name 'gamma'