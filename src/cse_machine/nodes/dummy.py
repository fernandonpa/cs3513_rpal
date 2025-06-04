from .rand import Rand

class Dummy(Rand):
    """Dummy value node used in the CSE machine.
    
    This class represents a dummy value in the RPAL language during execution.
    The dummy value is a special placeholder value that can be used when a value
    is needed syntactically but not semantically important.
    
    In RPAL, the 'dummy' keyword creates this value, which is often used in 
    pattern matching, as a placeholder for ignored parameters, or in situations 
    where a value is required but its actual content doesn't matter.
    """
    
    def __init__(self):
        """Initialize a new Dummy node.
        
        Creates a Dummy node with the fixed value "dummy", which represents
        the RPAL dummy value in the CSE machine.
        """
        super().__init__("dummy")  # Initialize with the fixed value "dummy"