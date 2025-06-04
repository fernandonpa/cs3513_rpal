from .symbol import Symbol

class B(Symbol):
    """Base environment frame symbol used in the CSE machine.
    
    This class represents a base environment in the RPAL abstract machine.
    It holds symbols (variables and functions) available in the current scope,
    providing the context for expression evaluation.
    
    Attributes:
        symbols (list): List of symbols defined in this environment frame
    """
    
    def __init__(self):
        """Initialize a new base environment frame.
        
        Creates an empty base environment with no symbols initially.
        The 'b' identifier is used to distinguish this as a base environment
        in the CSE machine execution.
        """
        super().__init__("b")  # Initialize as symbol with name 'b'
        self.symbols = []      # Storage for symbols in this environment