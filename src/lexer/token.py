from .token_types import TokenType

class MyToken:
    """Represents a lexical token in the RPAL language.
    
    A token is the smallest unit of meaning in the language, produced during 
    lexical analysis (scanning). Each token has a type and a value.
    
    Attributes:
        type (TokenType): The category of this token (keyword, identifier, etc.)
        value (str): The actual text or value of the token
    """
    
    def __init__(self, token_type, value):
        """Initialize a new token with a type and value.
        
        Args:
            token_type (TokenType): The category of this token
            value: The actual text or value of the token
            
        Raises:
            ValueError: If token_type is not a valid TokenType enum value
        """
        if not isinstance(token_type, TokenType):
            raise ValueError("token_type must be an instance of TokenType enum")
        self.type = token_type  # Store the token's category (e.g., KEYWORD, IDENTIFIER)
        self.value = value  # Store the actual text or value (e.g., "let", "x", "123")

    def get_type(self):
        """Get the token's type.
        
        Returns:
            TokenType: The category of this token
        """
        return self.type

    def get_value(self):
        """Get the token's value.
        
        Returns:
            The actual text or value of the token
        """
        return self.value