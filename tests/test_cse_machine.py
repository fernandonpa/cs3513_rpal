import pytest
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))



from src.tree_normalizer.syntax_node import Node as StdNode, NodeFactory
from src.tree_normalizer.tree_builder import AST
from src.cse_machine.machine import CSEMachine
from cse_machine.nodes.factory import CSEFactory
from src.cse_machine.nodes import *
from src.cse_machine.error_handler import CSEMachineError

class MockAST:
    """Mock AST for testing the CSE machine directly"""
    def __init__(self, root):
        self.root = root
    
    def get_root(self):
        return self.root

def create_identifier_node(name, depth=0):
    """Create a simple identifier node"""
    return NodeFactory.create(f"<IDENTIFIER:{name}>", depth)

def create_integer_node(value, depth=0):
    """Create an integer node"""
    return NodeFactory.create(f"<INTEGER:{value}>", depth)

def create_string_node(value, depth=0):
    """Create a string node"""
    return NodeFactory.create(f"<STRING:'{value}'>", depth)

def create_boolean_node(value, depth=0):
    """Create a boolean node (true or false)"""
    return NodeFactory.create(f"<TRUE_VALUE:{value}>", depth)

def create_gamma_node(depth=0):
    """Create a gamma node"""
    return NodeFactory.create("gamma", depth)

def create_lambda_node(depth=0):
    """Create a lambda node"""
    return NodeFactory.create("lambda", depth)

def create_binary_op_node(op, depth=0):
    """Create a binary operation node"""
    return NodeFactory.create(op, depth)

def create_tau_node(depth=0):
    """Create a tau node"""
    return NodeFactory.create("tau", depth)

def create_conditional_node(depth=0):
    """Create a conditional node"""
    return NodeFactory.create("->", depth)

def create_ystar_node(depth=0):
    """Create a Y* node for recursion"""
    return NodeFactory.create("<Y*>", depth)

class TestCSEMachineComponents:
    """Tests for individual components of the CSE machine"""
    
    def test_symbol_creation(self):
        """Test creating and manipulating symbols"""
        sym = Symbol("test")
        assert sym.get_value() == "test"
        
        sym.set_value("modified")
        assert sym.get_value() == "modified"
        
        # Test specialized symbols
        int_sym = IntegerValue("42")
        assert int_sym.get_value() == "42"
        
        str_sym = StringValue("hello")
        assert str_sym.get_value() == "hello"
        
        bool_sym = BoolValue("true")
        assert bool_sym.get_value() == "true"

    def test_environment_lookup(self):
        """Test environment creation and variable lookup"""
        # Create environments
        e0 = Environment(0)
        e1 = Environment(1)
        e1.set_parent(e0)
        
        # Bind variables
        x_id = Identifier("x")
        y_id = Identifier("y")
        z_id = Identifier("z")
        
        e0.bindings[x_id] = IntegerValue("10")
        e1.bindings[y_id] = StringValue("hello")
        
        # Test lookup
        assert e1.lookup(x_id).get_value() == "10"  # Should look up in parent
        assert e1.lookup(y_id).get_value() == "hello"  # Should find in current env
        assert e1.lookup(z_id).get_value() == "z"  # Not found, returns id itself

    def test_binary_operations(self):
        """Test binary operations"""
        # Create a CSE Machine to test operations
        mock_control = []
        mock_value = []
        mock_env = [Environment(0)]
        machine = CSEMachine(mock_control, mock_value, mock_env)
        
        # Test addition
        op = BinaryOperator("+")
        left = IntegerValue("5")
        right = IntegerValue("3")
        result = machine._apply_binary_operation(op, left, right)
        assert result.get_value() == "8"
        
        # Test logical operations
        op = BinaryOperator("&")
        left = BoolValue("true")
        right = BoolValue("false")
        result = machine._apply_binary_operation(op, left, right)
        assert result.get_value() == "false"
        
        # Test comparison
        op = BinaryOperator("gr")
        left = IntegerValue("5")
        right = IntegerValue("3")
        result = machine._apply_binary_operation(op, left, right)
        assert result.get_value() == "true"
    
    def test_unary_operations(self):
        """Test unary operations"""
        # Create a CSE Machine to test operations
        mock_control = []
        mock_value = []
        mock_env = [Environment(0)]
        machine = CSEMachine(mock_control, mock_value, mock_env)
        
        # Test negation
        op = UnaryOperator("neg")
        operand = IntegerValue("5")
        result = machine._apply_unary_operation(op, operand)
        assert result.get_value() == "-5"
        
        # Test logical not
        op = UnaryOperator("not")
        operand = BoolValue("true")
        result = machine._apply_unary_operation(op, operand)
        assert result.get_value() == "false"

class TestCSEFactory:
    """Tests for the CSE Factory"""
    
    def test_create_machine(self):
        """Test creating a CSE machine from an AST"""
        # Create a simple AST with just an integer node
        int_node = create_integer_node("42")
        ast = MockAST(int_node)
        
        # Create the machine
        factory = CSEFactory()
        machine = factory.create_cse_machine(ast)
        
        # Check machine structure
        assert isinstance(machine, CSEMachine)
        assert len(machine.control_stack) == 2
        assert isinstance(machine.control_stack[0], Environment)  # Global environment
        assert isinstance(machine.control_stack[1], Delta)  # Root delta
    
    def test_create_symbol(self):
        """Test creating symbols from AST nodes"""
        factory = CSEFactory()
        
        # Test identifier
        id_sym = factory.create_symbol(create_identifier_node("x"))
        assert isinstance(id_sym, Identifier)
        assert id_sym.get_value() == "x"
        
        # Test integer
        int_sym = factory.create_symbol(create_integer_node("42"))
        assert isinstance(int_sym, IntegerValue)
        assert int_sym.get_value() == "42"
        
        # Test operator
        op_sym = factory.create_symbol(create_binary_op_node("+"))
        assert isinstance(op_sym, BinaryOperator)
        assert op_sym.get_value() == "+"

class TestCSEMachineExecution:
    """Tests for CSE Machine execution"""
    
    def evaluate_ast(self, ast):
        """Helper method to evaluate an AST and get the result"""
        factory = CSEFactory()
        machine = factory.create_cse_machine(ast)
        return machine.get_result()
    
    def test_simple_value_evaluation(self):
        """Test evaluating simple literals"""
        # Integer
        int_node = create_integer_node("42")
        ast = MockAST(int_node)
        result = self.evaluate_ast(ast)
        assert result == "42"
        
        # String
        str_node = create_string_node("hello")
        ast = MockAST(str_node)
        result = self.evaluate_ast(ast)
        assert result == "hello"
        
        # Boolean
        bool_node = create_boolean_node("true")
        ast = MockAST(bool_node)
        result = self.evaluate_ast(ast)
        assert result == "true"
    
    def test_arithmetic_operations(self):
        """Test arithmetic operations"""
        # Addition: 3 + 4
        add_node = create_binary_op_node("+")
        left = create_integer_node("3", 1)
        right = create_integer_node("4", 1)
        add_node.children = [left, right]
        left.set_parent(add_node)
        right.set_parent(add_node)
        
        ast = MockAST(add_node)
        assert self.evaluate_ast(ast) == "7"
        
        # Subtraction: 10 - 4
        sub_node = create_binary_op_node("-")
        left = create_integer_node("10", 1)
        right = create_integer_node("4", 1)
        sub_node.children = [left, right]
        left.set_parent(sub_node)
        right.set_parent(sub_node)
        
        ast = MockAST(sub_node)
        assert self.evaluate_ast(ast) == "6"
        
        # Multiplication: 5 * 6
        mul_node = create_binary_op_node("*")
        left = create_integer_node("5", 1)
        right = create_integer_node("6", 1)
        mul_node.children = [left, right]
        left.set_parent(mul_node)
        right.set_parent(mul_node)
        
        ast = MockAST(mul_node)
        assert self.evaluate_ast(ast) == "30"
    
    def test_comparison_operations(self):
        """Test comparison operations"""
        # Equality (true): 5 eq 5
        eq_node = create_binary_op_node("eq")
        left = create_integer_node("5", 1)
        right = create_integer_node("5", 1)
        eq_node.children = [left, right]
        left.set_parent(eq_node)
        right.set_parent(eq_node)
        
        ast = MockAST(eq_node)
        assert self.evaluate_ast(ast) == "true"
        
        # Less than: 5 ls 10
        ls_node = create_binary_op_node("ls")
        left = create_integer_node("5", 1)
        right = create_integer_node("10", 1)
        ls_node.children = [left, right]
        left.set_parent(ls_node)
        right.set_parent(ls_node)
        
        ast = MockAST(ls_node)
        assert self.evaluate_ast(ast) == "true"
        
        # Greater than: 15 gr 10
        gr_node = create_binary_op_node("gr")
        left = create_integer_node("15", 1)
        right = create_integer_node("10", 1)
        gr_node.children = [left, right]
        left.set_parent(gr_node)
        right.set_parent(gr_node)
        
        ast = MockAST(gr_node)
        assert self.evaluate_ast(ast) == "true"
    
    def test_logical_operations(self):
        """Test logical operations"""
        # And (true): true & true
        and_node = create_binary_op_node("&")
        left = create_boolean_node("true", 1)
        right = create_boolean_node("true", 1)
        and_node.children = [left, right]
        left.set_parent(and_node)
        right.set_parent(and_node)
        
        ast = MockAST(and_node)
        assert self.evaluate_ast(ast) == "true"
        
        # And (false): true & false
        and_node = create_binary_op_node("&")
        left = create_boolean_node("true", 1)
        right = create_boolean_node("false", 1)
        and_node.children = [left, right]
        left.set_parent(and_node)
        right.set_parent(and_node)
        
        ast = MockAST(and_node)
        assert self.evaluate_ast(ast) == "false"
        
        # Or (true): false or true
        or_node = create_binary_op_node("or")
        left = create_boolean_node("false", 1)
        right = create_boolean_node("true", 1)
        or_node.children = [left, right]
        left.set_parent(or_node)
        right.set_parent(or_node)
        
        ast = MockAST(or_node)
        assert self.evaluate_ast(ast) == "true"
        
        # Not: not true
        not_node = create_binary_op_node("not")
        child = create_boolean_node("true", 1)
        not_node.children = [child]
        child.set_parent(not_node)
        
        ast = MockAST(not_node)
        assert self.evaluate_ast(ast) == "false"
    
    def test_lambda_and_application(self):
        """Test lambda creation and application"""
        # Create a lambda that adds 1 to its argument
        # lambda x. x + 1
        lambda_node = create_lambda_node()
        x_node = create_identifier_node("x", 1)
        
        # x + 1 expression
        plus_node = create_binary_op_node("+", 1)
        x_ref = create_identifier_node("x", 2)
        one_node = create_integer_node("1", 2)
        
        # Build the tree structure
        lambda_node.children = [x_node, plus_node]
        plus_node.children = [x_ref, one_node]
        
        x_node.set_parent(lambda_node)
        plus_node.set_parent(lambda_node)
        x_ref.set_parent(plus_node)
        one_node.set_parent(plus_node)
        
        # Apply the lambda to 5: (lambda x. x + 1) 5
        gamma_node = create_gamma_node()
        five_node = create_integer_node("5", 1)
        
        gamma_node.children = [lambda_node, five_node]
        lambda_node.set_parent(gamma_node)
        five_node.set_parent(gamma_node)
        
        ast = MockAST(gamma_node)
        assert self.evaluate_ast(ast) == "6"
    
    def test_conditionals(self):
        """Test conditional expressions"""
        # if true then 1 else 2
        cond_node = create_conditional_node()
        condition = create_boolean_node("true", 1)
        then_branch = create_integer_node("1", 1)
        else_branch = create_integer_node("2", 1)
        
        cond_node.children = [condition, then_branch, else_branch]
        condition.set_parent(cond_node)
        then_branch.set_parent(cond_node)
        else_branch.set_parent(cond_node)
        
        ast = MockAST(cond_node)
        assert self.evaluate_ast(ast) == "1"
        
        # if false then 1 else 2
        cond_node = create_conditional_node()
        condition = create_boolean_node("false", 1)
        then_branch = create_integer_node("1", 1)
        else_branch = create_integer_node("2", 1)
        
        cond_node.children = [condition, then_branch, else_branch]
        condition.set_parent(cond_node)
        then_branch.set_parent(cond_node)
        else_branch.set_parent(cond_node)
        
        ast = MockAST(cond_node)
        assert self.evaluate_ast(ast) == "2"
    
    def test_tuples(self):
        """Test tuple creation and access"""
        # Create a tuple (1, 2, 3)
        tau_node = create_tau_node()
        one_node = create_integer_node("1", 1)
        two_node = create_integer_node("2", 1)
        three_node = create_integer_node("3", 1)
        
        tau_node.children = [one_node, two_node, three_node]
        one_node.set_parent(tau_node)
        two_node.set_parent(tau_node)
        three_node.set_parent(tau_node)
        
        ast = MockAST(tau_node)
        assert self.evaluate_ast(ast) == "(1, 2, 3)"
        
        # Test aug operation: (1, 2, 3) aug 4
        aug_node = create_binary_op_node("aug")
        tau_clone = create_tau_node(1)
        one_clone = create_integer_node("1", 2)
        two_clone = create_integer_node("2", 2)
        three_clone = create_integer_node("3", 2)
        four_node = create_integer_node("4", 1)
        
        tau_clone.children = [one_clone, two_clone, three_clone]
        one_clone.set_parent(tau_clone)
        two_clone.set_parent(tau_clone)
        three_clone.set_parent(tau_clone)
        
        aug_node.children = [tau_clone, four_node]
        tau_clone.set_parent(aug_node)
        four_node.set_parent(aug_node)
        
        ast = MockAST(aug_node)
        assert self.evaluate_ast(ast) == "(1, 2, 3, 4)"
    
    def test_built_in_functions(self):
        """Test built-in functions"""
        # Order: find the length of a tuple
        # Order (1, 2, 3)
        gamma_node = create_gamma_node()
        order_id = create_identifier_node("Order", 1)
        
        tau_node = create_tau_node(1)
        one_node = create_integer_node("1", 2)
        two_node = create_integer_node("2", 2)
        three_node = create_integer_node("3", 2)
        
        tau_node.children = [one_node, two_node, three_node]
        one_node.set_parent(tau_node)
        two_node.set_parent(tau_node)
        three_node.set_parent(tau_node)
        
        gamma_node.children = [order_id, tau_node]
        order_id.set_parent(gamma_node)
        tau_node.set_parent(gamma_node)
        
        ast = MockAST(gamma_node)
        assert self.evaluate_ast(ast) == "3"

if __name__ == "__main__":
    pytest.main(["-v", "test_cse_machine.py"])