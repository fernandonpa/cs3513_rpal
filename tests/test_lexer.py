import pytest
from src.lexer.lexer import tokenize
from src.lexer.token_types import TokenType

# Helper function to extract (type, value) from token list
def tokens_to_type_value_list(tokens):
    return [(token.get_type(), token.get_value()) for token in tokens]


def test_sum_of_first_n():
    code = """
    let rec SumOfFirstN (number) = 
        number eq 0 -> 0 | number + SumOfFirstN(number - 1)
    in
    print(SumOfFirstN(100))
    """
    tokens = tokenize(code)
    expected = [
        (TokenType.KEYWORD, 'let'),
        (TokenType.KEYWORD, 'rec'),
        (TokenType.IDENTIFIER, 'SumOfFirstN'),
        (TokenType.PUNCTUATION, '('),
        (TokenType.IDENTIFIER, 'number'),
        (TokenType.PUNCTUATION, ')'),
        (TokenType.OPERATOR, '='),
        (TokenType.IDENTIFIER, 'number'),
        (TokenType.KEYWORD, 'eq'),
        (TokenType.INTEGER, '0'),
        (TokenType.OPERATOR, '->'),
        (TokenType.INTEGER, '0'),
        (TokenType.OPERATOR, '|'),
        (TokenType.IDENTIFIER, 'number'),
        (TokenType.OPERATOR, '+'),
        (TokenType.IDENTIFIER, 'SumOfFirstN'),
        (TokenType.PUNCTUATION, '('),
        (TokenType.IDENTIFIER, 'number'),
        (TokenType.OPERATOR, '-'),
        (TokenType.INTEGER, '1'),
        (TokenType.PUNCTUATION, ')'),
        (TokenType.KEYWORD, 'in'),
        (TokenType.IDENTIFIER, 'print'),
        (TokenType.PUNCTUATION, '('),
        (TokenType.IDENTIFIER, 'SumOfFirstN'),
        (TokenType.PUNCTUATION, '('),
        (TokenType.INTEGER, '100'),
        (TokenType.PUNCTUATION, ')'),
        (TokenType.PUNCTUATION, ')')
    ]
    assert tokens_to_type_value_list(tokens) == expected


def test_check_palindrome():
    code = """
    let CheckPalindrome number =
        number eq Reverse(number, 0) -> 'Palindrome' | 'Not a Palindrome'
        where rec Reverse(num, reversed) =
            num gr 0 -> Reverse(num / 10, (reversed * 10 + (num - (num / 10) * 10))) | reversed
    in
    Print(CheckPalindrome 1221)
    """
    tokens = tokenize(code)
    values = [t.get_value() for t in tokens]
    print(values)
    assert 'CheckPalindrome' in values
    assert 'Reverse' in values
    assert "'Palindrome'" in values
    assert "'Not a Palindrome'" in values


def test_find_greatest():
    code = """
    let FindGreatest num1 num2 num3 =
        (num1 > num2 & num1 > num3) -> num1
        | (num2 > num3) -> num2
        | num3
    in
    Print(FindGreatest 5 (-9) 8)
    """
    tokens = tokenize(code)
    values = [t.get_value() for t in tokens]
    assert 'FindGreatest' in values
    assert 'num1' in values
    assert '>' in values


def test_sum_list():
    code = """
    let Sum(A) = Psum (A,Order A ) 
    where rec Psum (T,N) = N eq 0 -> 0 
    | Psum(T,N-1)+T N 
    in Print ( Sum (1,2,3,4,5) ) 
    """
    tokens = tokenize(code)
    values = [t.get_value() for t in tokens]
    assert 'Sum' in values
    assert 'Psum' in values
    assert 'Order' in values
    assert 'eq' in values
    assert 'in' in values
