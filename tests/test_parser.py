import unittest
from src.lexer.tokenizer import Tokenizer
from src.parser.parser import Parser

class TestParser(unittest.TestCase):
    def test_let_in_expr(self):
        code = "let x = 10 in x + 1"
        tokens = Tokenizer(code).tokenize()
        parser = Parser(code)
        ast = parser.parse()
        ast_list = ast.to_list()
        expected = [
            "let",
            ".=",
            "..<IDENTIFIER:x>",
            "..<INTEGER:10>",
            ".+",
            "..<IDENTIFIER:x>",
            "..<INTEGER:1>"
        ]
        self.assertEqual(flatten(ast_list), expected)

    def test_fn_expr(self):
        code = "fn x -> x + 1"
        parser = Parser(code)
        ast = parser.parse()
        ast_list = ast.to_list()
        expected = [
            "lambda",
            "vars",
            "..<IDENTIFIER:x>",
            "->",
            ".+",
            "..<IDENTIFIER:x>",
            "..<INTEGER:1>"
        ]

        self.assertEqual(flatten(ast_list), expected)

    def test_nested_let_expr(self):
        code = "let x = 10 in let y = x + 1 in y"
        tokens = Tokenizer(code).tokenize()
        parser = Parser(code)
        ast = parser.parse()
        ast_list = ast.to_list()
        expected = [
            "let",
            ".=",
            "..<IDENTIFIER:x>",
            "..<INTEGER:10>",
            "let",
            ".=",
            "..<IDENTIFIER:y>",
            ".+",
            "..<IDENTIFIER:x>",
            "..<INTEGER:1>",
            "..<IDENTIFIER:y>"
        ]
        self.assertEqual(flatten(ast_list), expected)

    def test_expression_with_parentheses(self):
        code = "let x = (10 + 5) in x"
        tokens = Tokenizer(code).tokenize()
        parser = Parser(code)
        ast = parser.parse()
        ast_list = ast.to_list()
        expected = [
            "let",
            ".=",
            "..<IDENTIFIER:x>",
            ".+",
            "..<INTEGER:10>",
            "..<INTEGER:5>",
            "..<IDENTIFIER:x>"
        ]
        self.assertEqual(flatten(ast_list), expected)

def flatten(lst):
    if isinstance(lst, str):
        return [lst]
    result = []
    for item in lst:
        result.extend(flatten(item))
    return result

if __name__ == "__main__":
    unittest.main()