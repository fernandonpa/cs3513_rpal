import pytest
from src.lexer.lexer import tokenize
from src.parser.parser import Parser
from src.parser.node_types import NodeType

def parse_code(source_code):
    tokens = tokenize(source_code)
    parser = Parser(tokens)
    ast = parser.parse()
    return parser.convert_ast_to_string_ast()

def test_sum_of_first_n():
    source_code = """
    let rec SumOfFirstN (number) = 
        number eq 0 -> 0 | number + SumOfFirstN(number - 1)
    in
    print(SumOfFirstN(100))
    """
    output = parse_code(source_code)
    assert output[0].endswith("let")
    assert any("SUMOFFIRSTN" in line.upper() for line in output)
    assert any("number" in line.lower() for line in output)

def test_check_palindrome():
    source_code = """
    let CheckPalindrome number =
        number eq Reverse(number, 0) -> 'Palindrome' | 'Not a Palindrome'
        where rec Reverse(num, reversed) =
            num gr 0 -> Reverse(num / 10, (reversed * 10 + (num - (num / 10) * 10))) | reversed
    in
    Print(CheckPalindrome 1221)
    """
    output = parse_code(source_code)
    assert any("CHECKPALINDROME" in line.upper() for line in output)
    assert any("REVERSE" in line.upper() for line in output)
    assert any("PALINDROME" in line.upper() for line in output)


def test_find_greatest():
    source_code = """
    let FindGreatest num1 num2 num3 =
        (num1 > num2 & num1 > num3) -> num1
        | (num2 > num3) -> num2
        | num3
    in
    Print(FindGreatest 5 (-9) 8)
    """
    output = parse_code(source_code)
    assert "let" in [line.strip().lower() for line in output]
    assert any("FINDGREATEST" in line.upper() for line in output)
    assert any(">" in line or "gr" in line.lower() for line in output)

def test_sum_list():
    source_code = """
    let Sum(A) = Psum (A,Order A ) 
    where rec Psum (T,N) = N eq 0 -> 0 
    | Psum(T,N-1)+T N 
    in Print ( Sum (1,2,3,4,5) ) 
    """
    output = parse_code(source_code)
    assert any("SUM" in line.upper() for line in output)
    assert any("PSUM" in line.upper() for line in output)
    assert any("ORDER" in line.upper() for line in output)
    assert any("let" in line.lower() for line in output)

