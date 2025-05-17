import pytest
import os
import sys
from typing import List

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from src.lexer.tokenizer import Tokenizer
from src.parser.parser import Parser
from src.parser.node_types import NodeType
from src.parser.parser_error import ParserError

def parse_code(code):
    """Helper function to parse RPAL code"""
    tokenizer = Tokenizer(code)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    return parser.parse()

def test_simple_let_expression():
    ast = parse_code("let x = 5 in x")
    
    # Check that it's a LET node with two children
    assert ast.node_type == NodeType.LET
    assert ast.value == "let"
    assert len(ast.children) == 2
    
    # Check the definition part (should be an EQUAL node)
    def_node = ast.children[0]
    assert def_node.node_type == NodeType.EQUAL
    assert len(def_node.children) == 2
    
    # Check the variable part of the definition
    var_node = def_node.children[0]
    assert var_node.node_type == NodeType.IDENTIFIER
    assert var_node.value == "x"
    
    # Check the value part of the definition
    val_node = def_node.children[1]
    assert val_node.node_type == NodeType.INTEGER
    assert val_node.value == "5"
    
    # Check the body part of the let expression
    body_node = ast.children[1]
    assert body_node.node_type == NodeType.IDENTIFIER
    assert body_node.value == "x"

def test_function_definition():
    ast = parse_code("let f x y = x + y in f 1 2")
    
    # Check that it's a LET node
    assert ast.node_type == NodeType.LET
    
    # The first child should be the function definition
    fcn_def = ast.children[0]
    assert fcn_def.node_type == NodeType.FCN_FORM
    assert len(fcn_def.children) == 4  # function name, 2 params, body
    
    # Check function name
    fcn_name = fcn_def.children[0]
    assert fcn_name.node_type == NodeType.IDENTIFIER
    assert fcn_name.value == "f"
    
    # Check parameters
    param1 = fcn_def.children[1]
    assert param1.node_type == NodeType.IDENTIFIER
    assert param1.value == "x"
    
    param2 = fcn_def.children[2]
    assert param2.node_type == NodeType.IDENTIFIER
    assert param2.value == "y"
    
    # Function body should be an addition operation
    fcn_body = fcn_def.children[3]
    assert fcn_body.node_type == NodeType.PLUS
    
    # Check the application in the let body
    application = ast.children[1]
    assert application.node_type == NodeType.GAMMA
    
    # Should be applying f to 1
    fcn_app = application.children[0]
    assert fcn_app.node_type == NodeType.GAMMA
    
    # The function being applied should be f
    f_node = fcn_app.children[0]
    assert f_node.node_type == NodeType.IDENTIFIER
    assert f_node.value == "f"

def test_tuple_creation():
    ast = parse_code("(1, 2, 3)")
    
    # Should create a TAU node with 3 children
    assert ast.node_type == NodeType.TAU
    assert len(ast.children) == 3
    
    for i, child in enumerate(ast.children):
        assert child.node_type == NodeType.INTEGER
        assert child.value == str(i + 1)

def test_conditional():
    ast = parse_code("x > 0 -> 'positive' | 'non-positive'")
    
    # Should be a conditional node
    assert ast.node_type == NodeType.CONDITIONAL
    assert len(ast.children) == 3
    
    # Check condition
    condition = ast.children[0]
    assert condition.node_type == NodeType.GT
    
    # Check true branch
    true_branch = ast.children[1]
    assert true_branch.node_type == NodeType.STRING
    assert true_branch.value == "positive"
    
    # Check false branch
    false_branch = ast.children[2]
    assert false_branch.node_type == NodeType.STRING
    assert false_branch.value == "non-positive"

def test_where_expression():
    ast = parse_code("x + y where x = 1 and y = 2")
    
    # Should be a WHERE node
    assert ast.node_type == NodeType.WHERE
    assert len(ast.children) == 2
    
    # Check expression
    expr = ast.children[0]
    assert expr.node_type == NodeType.PLUS
    
    # Check definition part
    defs = ast.children[1]
    assert defs.node_type == NodeType.AND
    assert len(defs.children) == 2

def test_parser_error():
    with pytest.raises(ParserError):
        parse_code("let x = in x")  # Missing expression after =
        
    with pytest.raises(ParserError):
        parse_code("x + ")  # Missing right operand

if __name__ == "__main__":
    test_simple_let_expression()
    test_function_definition()
    test_tuple_creation()
    test_conditional()
    test_where_expression()
    test_parser_error()
    print("All parser tests passed!")