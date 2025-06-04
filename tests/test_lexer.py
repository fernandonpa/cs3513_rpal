import pytest
from src.lexer.tokenizer import Tokenizer
from src.lexer.token import Token
from src.lexer.token_types import TokenType
from src.lexer.lexer_error import UnexpectedCharacterError, UnclosedStringError

class TestTokenizer:
    
    def test_empty_input(self):
        tokenizer = Tokenizer("")
        tokens = tokenizer.tokenize()
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.EOF
    
    def test_whitespace(self):
        tokenizer = Tokenizer("   \n\t   ")
        tokens = tokenizer.tokenize()
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.EOF
    
    def test_single_keyword(self):
        tokenizer = Tokenizer("let")
        tokens = tokenizer.tokenize()
        assert len(tokens) == 2
        assert tokens[0].type == TokenType.LET
        assert tokens[0].value == "let"
        assert tokens[1].type == TokenType.EOF
    
    def test_all_keywords(self):
        keywords = [
            "let", "in", "fn", "where", "aug", "or", "and", "not", 
            "gr", "ge", "ls", "le", "eq", "ne", "true", "false", 
            "nil", "dummy", "within", "rec"
        ]
        
        for keyword in keywords:
            tokenizer = Tokenizer(keyword)
            tokens = tokenizer.tokenize()
            assert len(tokens) == 2
            assert tokens[0].value.lower() == keyword  # Case insensitive comparison
            assert tokens[1].type == TokenType.EOF
    
    def test_identifiers(self):
        tokenizer = Tokenizer("x y abc ABC abc123 a_b_c")
        tokens = tokenizer.tokenize()
        assert len(tokens) == 7  # 6 identifiers + EOF
        
        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].value == "x"
        
        assert tokens[1].type == TokenType.IDENTIFIER
        assert tokens[1].value == "y"
        
        assert tokens[2].type == TokenType.IDENTIFIER
        assert tokens[2].value == "abc"
        
        assert tokens[3].type == TokenType.IDENTIFIER
        assert tokens[3].value == "ABC"
        
        assert tokens[4].type == TokenType.IDENTIFIER
        assert tokens[4].value == "abc123"
        
        assert tokens[5].type == TokenType.IDENTIFIER
        assert tokens[5].value == "a_b_c"
    
    def test_integers(self):
        tokenizer = Tokenizer("0 123 456789")
        tokens = tokenizer.tokenize()
        assert len(tokens) == 4  # 3 integers + EOF
        
        assert tokens[0].type == TokenType.INTEGER
        assert tokens[0].value == "0"
        
        assert tokens[1].type == TokenType.INTEGER
        assert tokens[1].value == "123"
        
        assert tokens[2].type == TokenType.INTEGER
        assert tokens[2].value == "456789"
    
    def test_strings(self):
        tokenizer = Tokenizer("'hello' 'world' 'with \\'escape\\''")
        tokens = tokenizer.tokenize()
        assert len(tokens) == 4  # 3 strings + EOF
        
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == "hello"
        
        assert tokens[1].type == TokenType.STRING
        assert tokens[1].value == "world"
        
        # The escaped quotes would be handled at parse time
        assert tokens[2].type == TokenType.STRING
    
    def test_operators(self):
        tokenizer = Tokenizer("+ - * / -> = | > < !")
        tokens = tokenizer.tokenize()
        assert len(tokens) == 11  # 7 operators + EOF
        
        assert tokens[0].type == TokenType.PLUS
        assert tokens[0].value == "+"
        
        assert tokens[1].type == TokenType.MINUS
        assert tokens[1].value == "-"
        
        assert tokens[2].type == TokenType.MULTIPLY
        assert tokens[2].value == "*"
        
        assert tokens[3].type == TokenType.DIVIDE
        assert tokens[3].value == "/"
        
        assert tokens[4].type == TokenType.ARROW
        assert tokens[4].value == "->"
        
        assert tokens[5].type == TokenType.EQUALS
        assert tokens[5].value == "="
        
        assert tokens[6].type == TokenType.PIPE
        assert tokens[6].value == "|"

        assert tokens[7].type == TokenType.GR
        assert tokens[7].value == ">"

        assert tokens[8].type == TokenType.LS
        assert tokens[8].value == "<"

        assert tokens[9].type == TokenType.NOT
        assert tokens[9].value == "!"
    
    def test_punctuation(self):
        tokenizer = Tokenizer("( ) ; ,")
        tokens = tokenizer.tokenize()
        assert len(tokens) == 5  # 4 punctuation + EOF
        
        assert tokens[0].type == TokenType.LEFT_PAREN
        assert tokens[0].value == "("
        
        assert tokens[1].type == TokenType.RIGHT_PAREN
        assert tokens[1].value == ")"
        
        assert tokens[2].type == TokenType.SEMICOLON
        assert tokens[2].value == ";"
        
        assert tokens[3].type == TokenType.COMMA
        assert tokens[3].value == ","
    
    def test_comments(self):
        tokenizer = Tokenizer("let x // This is a comment\n= 5")
        tokens = tokenizer.tokenize()
        assert len(tokens) == 5  # LET + IDENTIFIER + EQUALS + INTEGER + EOF
        
        assert tokens[0].type == TokenType.LET
        assert tokens[1].type == TokenType.IDENTIFIER
        assert tokens[1].value == "x"
        assert tokens[2].type == TokenType.EQUALS
        assert tokens[3].type == TokenType.INTEGER
        assert tokens[3].value == "5"
        assert tokens[4].type == TokenType.EOF
    
    def test_line_and_column_tracking(self):
        tokenizer = Tokenizer("let\nx =\n 5")
        tokens = tokenizer.tokenize()
        
        assert tokens[0].line == 1  # 'let' is on line 1
        assert tokens[0].column == 1
        
        assert tokens[1].line == 2  # 'x' is on line 2
        assert tokens[1].column == 1
        
        assert tokens[2].line == 2  # '=' is on line 2
        assert tokens[2].column == 3
        
        assert tokens[3].line == 3  # '5' is on line 3
        assert tokens[3].column == 2
    
    def test_unclosed_string_error(self):
        tokenizer = Tokenizer("'unclosed string")
        with pytest.raises(UnclosedStringError):
            tokenizer.tokenize()
    
    def test_unexpected_character_error(self):
        tokenizer = Tokenizer("let x = `")
        with pytest.raises(UnexpectedCharacterError):
            tokenizer.tokenize()
    
    def test_complex_program(self):
        program = """
        let Sum(A) = Psum (A, Order A)
        where rec Psum(T, N) = N eq 0 -> 0
                              | Psum(T, N-1) + T N
        in Print(Sum(1, 2, 3, 4, 5))
        """
        
        tokenizer = Tokenizer(program)
        tokens = tokenizer.tokenize()
        
        # Verify a few key tokens
        token_values = [token.value for token in tokens if token.type != TokenType.EOF]
        
        assert "let" in token_values
        assert "Sum" in token_values
        assert "where" in token_values
        assert "rec" in token_values
        assert "Psum" in token_values
        assert "eq" in token_values
        assert "->" in token_values
        assert "+" in token_values
        assert "|" in token_values
        assert "in" in token_values
        assert "Print" in token_values