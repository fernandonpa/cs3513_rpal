from .token import Token
from .token_types import TokenType, KEYWORDS, OPERATORS, PUNCTUATION
from .lexer_error import UnexpectedCharacterError, UnclosedStringError

class Tokenizer:
    """
    Lexical analyzer for RPAL language that converts source code into a stream of tokens
    """
    
    def __init__(self, source_code):
        """
        Initialize the tokenizer with source code
        
        Args:
            source_code (str): The source code to tokenize
        """
        self.source = source_code
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self.current_char = self.source[0] if self.source else None
    
    def advance(self):
        """
        Move to the next character in the source code
        """
        # Update line and column before advancing
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
            
        self.position += 1
        
        if self.position >= len(self.source):
            self.current_char = None
            return
        
        self.current_char = self.source[self.position]
    
    def peek(self, offset=1):
        """
        Look ahead at a character without advancing
        
        Args:
            offset (int, optional): How many characters ahead to look. Defaults to 1.
            
        Returns:
            str or None: The character at the offset or None if out of bounds
        """
        peek_position = self.position + offset
        if peek_position >= len(self.source):
            return None
        return self.source[peek_position]
    
    def skip_whitespace(self):
        """
        Skip whitespace characters (space, tab, newline)
        """
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def skip_comment(self):
        """
        Skip comments (starting with //)
        """
        # Skip '//'
        self.advance()
        self.advance()
        
        # Skip until end of line
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
            
        # Skip the newline
        if self.current_char == '\n':
            self.advance()
    
    def identifier_or_keyword(self):
        """
        Process an identifier or keyword
        
        Returns:
            Token: The identifier or keyword token
        """
        start_column = self.column
        start_line = self.line
        result = ''
        
        # First character must be a letter
        if self.current_char.isalpha():
            result += self.current_char
            self.advance()
            
            # Subsequent characters can be letters, digits, or underscores
            while (self.current_char is not None and 
                  (self.current_char.isalnum() or self.current_char == '_')):
                result += self.current_char
                self.advance()
            
            # Check if it's a keyword
            token_type = KEYWORDS.get(result.lower(), TokenType.IDENTIFIER)
            return Token(token_type, result, start_line, start_column)
        
        return None
    
    def number(self):
        """
        Process a number literal
        
        Returns:
            Token: The integer token
        """
        start_column = self.column
        start_line = self.line
        result = ''
        
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        
        return Token(TokenType.INTEGER, result, start_line, start_column)
    
    def string(self):
        """
        Process a string literal
        
        Returns:
            Token: The string token
            
        Raises:
            UnclosedStringError: If the string is not properly closed
        """
        start_column = self.column
        start_line = self.line
        result = ''
        
        # Skip the opening quote
        self.advance()
        
        while self.current_char is not None and self.current_char != '\'':
            # Handle escape sequences
            if self.current_char == '\\' and self.peek() == '\'':
                result += self.current_char + self.peek()
                self.advance()  # Skip '\'
                self.advance()  # Skip escaped quote
            else:
                result += self.current_char
                self.advance()
        
        # Check if we reached the end of the string
        if self.current_char is None:
            raise UnclosedStringError(start_line, start_column)
        
        # Skip the closing quote
        self.advance()
        
        return Token(TokenType.STRING, result, start_line, start_column)
    
    def operator(self):
        """
        Process an operator
        
        Returns:
            Token: The operator token or None if not an operator
        """
        start_column = self.column
        start_line = self.line
        
        # Check for two-character operators
        if self.current_char == '-' and self.peek() == '>':
            operator = '->'
            token_type = OPERATORS.get(operator)
            self.advance()  # Skip '-'
            self.advance()  # Skip '>'
            return Token(token_type, operator, start_line, start_column)
            
        # Check for single-character operators
        operator = self.current_char
        token_type = OPERATORS.get(operator)
        
        if token_type is not None:
            self.advance()
            return Token(token_type, operator, start_line, start_column)
        
        # Special case for '|' which is also an operator in RPAL
        if self.current_char == '|':
            self.advance()
            return Token(TokenType.OR, '|', start_line, start_column)
        
        return None
    
    def punctuation(self):
        """
        Process punctuation
        
        Returns:
            Token: The punctuation token or None if not punctuation
        """
        start_column = self.column
        start_line = self.line
        char = self.current_char
        token_type = PUNCTUATION.get(char)
        
        if token_type is not None:
            self.advance()
            return Token(token_type, char, start_line, start_column)
        
        return None
    
    def get_next_token(self):
        """
        Get the next token from the source code
        
        Returns:
            Token: The next token
            
        Raises:
            UnexpectedCharacterError: If an unexpected character is encountered
        """
        while self.current_char is not None:
            # Skip whitespace
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            # Skip comments
            if self.current_char == '/' and self.peek() == '/':
                self.skip_comment()
                continue
            
            # Identifier or keyword
            if self.current_char.isalpha():
                return self.identifier_or_keyword()
            
            # Number
            if self.current_char.isdigit():
                return self.number()
            
            # String
            if self.current_char == '\'':
                return self.string()
            
            # Operator
            operator_token = self.operator()
            if operator_token:
                return operator_token
            
            # Punctuation
            punctuation_token = self.punctuation()
            if punctuation_token:
                return punctuation_token
            
            # Unexpected character
            raise UnexpectedCharacterError(
                self.current_char, self.line, self.column
            )
        
        # End of file
        return Token(TokenType.EOF, '', self.line, self.column)
    
    def tokenize(self):
        """
        Tokenize the entire source code
        
        Returns:
            list: List of tokens
        """
        tokens = []
        
        while True:
            token = self.get_next_token()
            tokens.append(token)
            
            # Stop at end of file
            if token.type == TokenType.EOF:
                break
        
        return tokens