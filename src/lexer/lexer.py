import re
from enum import Enum
from .token_types import TokenType
from .token import MyToken


def tokenize(input_str):
    """Convert an RPAL source string into a sequence of tokens.
    
    This function performs lexical analysis (scanning) on the input string,
    breaking it down into meaningful tokens according to the RPAL language
    specification. It recognizes keywords, identifiers, literals, operators,
    and other syntactic elements.
    
    Args:
        input_str (str): The RPAL source code to tokenize
        
    Returns:
        list: A list of MyToken objects representing the tokens found
        
    Raises:
        ValueError: If there's an invalid token type in the pattern dictionary
    """
    tokens = []  # List to store the identified tokens
    
    # Dictionary mapping token types to their regex patterns
    # Order matters - multi-character operators must come before single characters
    keywords = {
        'COMMENT': r'//.*',                     # Comments start with // and continue to end of line
        'KEYWORD': r'(let|in|fn|where|aug|or|not|gr|ge|ls|le|eq|ne|true|false|nil|dummy|within|and|rec)\b',  # RPAL reserved words
        'STRING': r'\'(?:\\\'|[^\'])*\'',       # String literals enclosed in single quotes
        'IDENTIFIER': r'[a-zA-Z][a-zA-Z0-9_]*', # Variables and function names
        'INTEGER': r'\d+',                      # Numeric literals
        'MULTI_CHAR_OPERATOR': r'(\*\*|->|>=|<=)',  # Multi-character operators (handle these first!)
        'OPERATOR': r'[+\-*<>&.@/:=~|$\#!%^_\[\]{}"\'?]',  # Single character operators
        'SPACES': r'[ \t\n]+',                  # Whitespace (ignored in output)
        'PUNCTUATION': r'[();,]'                # Punctuation marks
    }
    
    # Process the input string until it's empty
    while input_str:
        matched = False  # Flag to track if we found a matching pattern
        
        # Try each pattern against the start of the remaining input
        for key, pattern in keywords.items():
            match = re.match(pattern, input_str)
            if match:
                # We found a match for this pattern
                if key != 'SPACES':  # Ignore whitespace
                    if key == 'COMMENT':
                        # Found a comment - ignore it but track that we matched something
                        comment = match.group(0)
                        input_str = input_str[match.end():]  # Move past the comment
                        matched = True
                        break
                    else:
                        # For all other token types, create a token
                        # Handle multi-character operators as regular operators
                        if key == 'MULTI_CHAR_OPERATOR':
                            token_type = TokenType.OPERATOR
                        else:
                            token_type = getattr(TokenType, key)  # Get TokenType enum value
                            
                        if not isinstance(token_type, TokenType):
                            raise ValueError(f"Token type '{key}' is not a valid TokenType")
                            
                        # Create a new token and add it to our results
                        tokens.append(MyToken(token_type, match.group(0)))
                        input_str = input_str[match.end():]  # Move past the matched text
                        matched = True
                        break
                # For whitespace, just skip it
                input_str = input_str[match.end():]
                matched = True
                break
                
        # If we couldn't match any pattern, there's an error in the input
        if not matched:
            print("Error: Unable to tokenize input")
            break  # Avoid infinite loop by breaking out
            
    return tokens

