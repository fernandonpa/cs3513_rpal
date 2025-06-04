from .symbol import Symbol

class Err(Symbol):
    """Error symbol used in the CSE machine.
    
    This class represents an error condition during RPAL program execution.
    When operations encounter invalid inputs or other error conditions,
    an Err object may be created to signal that an error has occurred.
    
    The error symbol has an empty string as its data, distinguishing it
    from valid symbols and allowing the interpreter to detect error states.
    """
    
    def __init__(self):
        """Initialize a new Error symbol.
        
        Creates an Error symbol with an empty string as its data value,
        which indicates an error condition in the CSE machine.
        """
        super().__init__("")  # Initialize as symbol with empty string data