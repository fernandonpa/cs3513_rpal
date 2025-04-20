import unittest
from src.lexer.tokenizer import Tokenizer
from src.lexer.token_types import TokenType
from src.lexer.lexer_error import LexicalError

class TestTokenizer(unittest.TestCase):
    def setUp(self):
        self.tokenizer = Tokenizer()

    def test_keywords_and_identifiers(self):
        result = self.tokenizer.tokenize("let in x y123")
        types = [token.token_type for token in result[:-1]]  # skip EOF
        self.assertEqual(types, [TokenType.KEYWORD, TokenType.KEYWORD, TokenType.IDENTIFIER, TokenType.IDENTIFIER])

    def test_integer_and_operator(self):
        result = self.tokenizer.tokenize("123 + 456")
        types = [token.token_type for token in result[:-1]]
        self.assertEqual(types, [TokenType.INTEGER, TokenType.OPERATOR, TokenType.INTEGER])

    def test_string_literal(self):
        result = self.tokenizer.tokenize("'hello world'")
        self.assertEqual(result[0].token_type, TokenType.STRING)

    def test_punctuation(self):
        result = self.tokenizer.tokenize("( ; , )")
        types = [token.token_type for token in result if token.token_type != TokenType.END_OF_TOKENS]
        self.assertTrue(all(t == TokenType.PUNCTUATION for t in types))

    def test_invalid_token(self):
        with self.assertRaises(LexicalError):
            self.tokenizer.tokenize("@invalid&^")

if __name__ == '__main__':
    unittest.main()
