import pytest
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from tree_normalizer.syntax_node import Node, NodeFactory, StandardizationError
from tree_normalizer.tree_builder import AST
from tree_normalizer.tree_factory import ASTFactory, ASTConstructionError
from tree_normalizer.normalizer import StandardizedTree
from tree_normalizer.normalizer_errors import InvalidTreeStructureError


class TestNode:
    """Tests for the Node class."""
    
    def test_create_node(self):
        """Test creating a node with basic properties."""
        node = Node("test", 1)
        assert node.get_data() == "test"
        assert node.get_depth() == 1
        assert node.get_parent() is None
        assert len(node.get_children()) == 0
        assert node.is_standardized is False
    
    def test_add_child(self):
        """Test adding a child to a node."""
        parent = Node("parent", 0)
        child = Node("child", 1)
        
        parent.add_child(child)
        
        assert len(parent.get_children()) == 1
        assert parent.get_children()[0] == child
        assert child.get_parent() == parent


class TestAST:
    """Tests for the AST class."""
    
    def test_create_empty_ast(self):
        """Test creating an empty AST."""
        ast = AST()
        assert ast.get_root() is None
    
    def test_create_ast_with_root(self):
        """Test creating an AST with a root node."""
        root = Node("root")
        ast = AST(root)
        assert ast.get_root() == root
    
    def test_set_root(self):
        """Test setting the root of an AST."""
        ast = AST()
        root = Node("root")
        ast.set_root(root)
        assert ast.get_root() == root
    
    def test_standardize_empty_ast(self):
        """Test standardizing an empty AST raises an error."""
        ast = AST()
        with pytest.raises(StandardizationError):
            ast.standardize()


class TestASTFactory:
    """Tests for the ASTFactory class."""
    
    def test_create_ast_from_data(self):
        """Test creating an AST from parsed data."""
        data = [
            "let",
            ".function_form",
            "..x",
            "..+",
            "...x",
            "...1",
            ".in",
            "..x"
        ]
        
        ast = ASTFactory.get_abstract_syntax_tree(data)
        
        assert ast.get_root() is not None
        assert ast.get_root().get_data() == "let"
        assert len(ast.get_root().get_children()) == 2
        assert ast.get_root().get_children()[0].get_data() == "function_form"
    
    def test_create_ast_from_empty_data(self):
        """Test creating an AST from empty data raises an error."""
        with pytest.raises(ASTConstructionError):
            ASTFactory.get_abstract_syntax_tree([])


class TestStandardization:
    """Tests for standardization transformations."""
    
    def test_standardize_let(self):
        """Test standardizing a let expression."""
        # Create an AST for: let x = 1 in x
        root = Node("let")
        equal = Node("=")
        x1 = Node("x")
        one = Node("1")
        x2 = Node("x")
        
        root.add_child(equal)
        equal.add_child(x1)
        equal.add_child(one)
        root.add_child(x2)
        
        ast = AST(root)
        ast.standardize()
        
        # Result should be gamma with lambda and 1
        assert ast.get_root().get_data() == "gamma"
        assert len(ast.get_root().get_children()) == 2
        assert ast.get_root().get_children()[0].get_data() == "lambda"
        assert ast.get_root().get_children()[1].get_data() == "1"
    
    def test_standardize_where(self):
        """Test standardizing a where expression."""
        # Create an AST for: x where x = 1
        root = Node("where")
        x1 = Node("x")
        equal = Node("=")
        x2 = Node("x")
        one = Node("1")
        
        root.add_child(x1)
        root.add_child(equal)
        equal.add_child(x2)
        equal.add_child(one)
        
        ast = AST(root)
        ast.standardize()
        
        # Result should be gamma with lambda and 1 (same as let)
        assert ast.get_root().get_data() == "gamma"
        assert len(ast.get_root().get_children()) == 2
        assert ast.get_root().get_children()[0].get_data() == "lambda"
        assert ast.get_root().get_children()[1].get_data() == "1"
    
    def test_standardize_function_form(self):
        """Test standardizing a function form."""
        # Create an AST for: f x y = x + y
        root = Node("function_form")
        f = Node("f")
        x = Node("x")
        y = Node("y")
        plus = Node("+")
        x2 = Node("x")
        y2 = Node("y")
        
        root.add_child(f)
        root.add_child(x)
        root.add_child(y)
        root.add_child(plus)
        plus.add_child(x2)
        plus.add_child(y2)
        
        ast = AST(root)
        ast.standardize()
        
        # Result should be f = lambda x . lambda y . x + y
        assert ast.get_root().get_data() == "="
        assert len(ast.get_root().get_children()) == 2
        assert ast.get_root().get_children()[0].get_data() == "f"
        assert ast.get_root().get_children()[1].get_data() == "lambda"
        
        lambda1 = ast.get_root().get_children()[1]
        assert len(lambda1.get_children()) == 2
        assert lambda1.get_children()[0].get_data() == "x"
        assert lambda1.get_children()[1].get_data() == "lambda"
        
        lambda2 = lambda1.get_children()[1]
        assert len(lambda2.get_children()) == 2
        assert lambda2.get_children()[0].get_data() == "y"
        assert lambda2.get_children()[1].get_data() == "+"
    
    def test_standardize_lambda_multiple_params(self):
        """Test standardizing a lambda with multiple parameters."""
        # Create an AST for: lambda x y.x+y
        root = Node("lambda")
        x = Node("x")
        y = Node("y")
        plus = Node("+")
        x2 = Node("x")
        y2 = Node("y")
        
        root.add_child(x)
        root.add_child(y)
        root.add_child(plus)
        plus.add_child(x2)
        plus.add_child(y2)
        
        ast = AST(root)
        ast.standardize()
        
        # Result should be lambda x . lambda y . x + y
        assert ast.get_root().get_data() == "lambda"
        assert len(ast.get_root().get_children()) == 2
        assert ast.get_root().get_children()[0].get_data() == "x"
        assert ast.get_root().get_children()[1].get_data() == "lambda"
        
        lambda2 = ast.get_root().get_children()[1]
        assert len(lambda2.get_children()) == 2
        assert lambda2.get_children()[0].get_data() == "y"
        assert lambda2.get_children()[1].get_data() == "+"
    
    def test_standardize_within(self):
        """Test standardizing a within expression."""
        # Create an AST for: (x = 1) within (y = x + 2)
        root = Node("within")
        equal1 = Node("=")
        x = Node("x")
        one = Node("1")
        equal2 = Node("=")
        y = Node("y")
        plus = Node("+")
        x2 = Node("x")
        two = Node("2")
        
        root.add_child(equal1)
        equal1.add_child(x)
        equal1.add_child(one)
        root.add_child(equal2)
        equal2.add_child(y)
        equal2.add_child(plus)
        plus.add_child(x2)
        plus.add_child(two)
        
        ast = AST(root)
        ast.standardize()
        
        # Result should be y = gamma with lambda x.x+2 and 1
        assert ast.get_root().get_data() == "="
        assert len(ast.get_root().get_children()) == 2
        assert ast.get_root().get_children()[0].get_data() == "y"
        assert ast.get_root().get_children()[1].get_data() == "gamma"
        
        gamma = ast.get_root().get_children()[1]
        assert len(gamma.get_children()) == 2
        assert gamma.get_children()[0].get_data() == "lambda"
        assert gamma.get_children()[1].get_data() == "1"
        
        lambda1 = gamma.get_children()[0]
        assert len(lambda1.get_children()) == 2
        assert lambda1.get_children()[0].get_data() == "x"
        assert lambda1.get_children()[1].get_data() == "+"
    
    def test_standardize_at(self):
        """Test standardizing an @ (at) expression."""
        # Create an AST for: E1 @ N E2
        root = Node("@")
        e1 = Node("E1")
        n = Node("N")
        e2 = Node("E2")
        
        root.add_child(e1)
        root.add_child(n)
        root.add_child(e2)
        
        ast = AST(root)
        ast.standardize()
        
        # Result should be gamma with gamma(N, E1) and E2
        assert ast.get_root().get_data() == "gamma"
        assert len(ast.get_root().get_children()) == 2
        assert ast.get_root().get_children()[0].get_data() == "gamma"
        assert ast.get_root().get_children()[1].get_data() == "E2"
        
        inner_gamma = ast.get_root().get_children()[0]
        assert len(inner_gamma.get_children()) == 2
        assert inner_gamma.get_children()[0].get_data() == "N"
        assert inner_gamma.get_children()[1].get_data() == "E1"
    
    def test_standardize_and(self):
        """Test standardizing an 'and' expression."""
        # Create an AST for: and(x=1, y=2)
        root = Node("and")
        equal1 = Node("=")
        x = Node("x")
        one = Node("1")
        equal2 = Node("=")
        y = Node("y")
        two = Node("2")
        
        root.add_child(equal1)
        equal1.add_child(x)
        equal1.add_child(one)
        root.add_child(equal2)
        equal2.add_child(y)
        equal2.add_child(two)
        
        ast = AST(root)
        ast.standardize()
        
        # Result should be = with comma(x,y) and tau(1,2)
        assert ast.get_root().get_data() == "="
        assert len(ast.get_root().get_children()) == 2
        assert ast.get_root().get_children()[0].get_data() == ","
        assert ast.get_root().get_children()[1].get_data() == "tau"
        
        comma = ast.get_root().get_children()[0]
        assert len(comma.get_children()) == 2
        assert comma.get_children()[0].get_data() == "x"
        assert comma.get_children()[1].get_data() == "y"
        
        tau = ast.get_root().get_children()[1]
        assert len(tau.get_children()) == 2
        assert tau.get_children()[0].get_data() == "1"
        assert tau.get_children()[1].get_data() == "2"
    
    def test_standardize_rec(self):
        """Test standardizing a rec expression."""
        # Create an AST for: rec f = lambda x.f(x-1)
        root = Node("rec")
        equal = Node("=")
        f = Node("f")
        lambda_node = Node("lambda")
        x = Node("x")
        app = Node("gamma")
        f2 = Node("f")
        minus = Node("-")
        x2 = Node("x")
        one = Node("1")
        
        root.add_child(equal)
        equal.add_child(f)
        equal.add_child(lambda_node)
        lambda_node.add_child(x)
        lambda_node.add_child(app)
        app.add_child(f2)
        app.add_child(minus)
        minus.add_child(x2)
        minus.add_child(one)
        
        ast = AST(root)
        ast.standardize()
        
        # Result should be f = gamma(Y*, lambda f.lambda x.f(x-1))
        assert ast.get_root().get_data() == "="
        assert len(ast.get_root().get_children()) == 2
        assert ast.get_root().get_children()[0].get_data() == "f"
        assert ast.get_root().get_children()[1].get_data() == "gamma"
        
        gamma = ast.get_root().get_children()[1]
        assert len(gamma.get_children()) == 2
        assert gamma.get_children()[0].get_data() == "<Y*>"
        assert gamma.get_children()[1].get_data() == "lambda"


class TestStandardizedTree:
    """Tests for the StandardizedTree class."""
    
    def test_create_st_from_ast(self):
        """Test creating a StandardizedTree from an AST."""
        # Create a simple AST: let x = 1 in x
        root = Node("let")
        equal = Node("=")
        x1 = Node("x")
        one = Node("1")
        x2 = Node("x")
        
        root.add_child(equal)
        equal.add_child(x1)
        equal.add_child(one)
        root.add_child(x2)
        
        ast = AST(root)
        st = StandardizedTree(ast)
        
        # Check that the root is now a gamma node
        assert st.get_root() is not None
        assert st.get_root().get_data() == "gamma"
        assert st.get_root().is_standardized
    
    def test_validate_valid_st(self):
        """Test validating a valid standardized tree."""
        # Create a valid ST: gamma(lambda x.x, 1)
        root = Node("gamma")
        lambda_node = Node("lambda")
        x1 = Node("x")
        x2 = Node("x")
        one = Node("1")
        
        root.add_child(lambda_node)
        lambda_node.add_child(x1)
        lambda_node.add_child(x2)
        root.add_child(one)
        
        # Mark all nodes as standardized
        root.is_standardized = True
        lambda_node.is_standardized = True
        x1.is_standardized = True
        x2.is_standardized = True
        one.is_standardized = True
        
        st = StandardizedTree()
        st.root = root
        
        assert st.validate()
    
    def test_validate_invalid_st(self):
        """Test validating an invalid standardized tree."""
        # Create an invalid ST: let x = 1 in x (unstandardized)
        root = Node("let")
        equal = Node("=")
        x1 = Node("x")
        one = Node("1")
        x2 = Node("x")
        
        root.add_child(equal)
        equal.add_child(x1)
        equal.add_child(one)
        root.add_child(x2)
        
        # Mark all nodes as standardized
        root.is_standardized = True
        equal.is_standardized = True
        x1.is_standardized = True
        one.is_standardized = True
        x2.is_standardized = True
        
        st = StandardizedTree()
        st.root = root
        
        assert not st.validate()


# Sample test for the full standardization process
def test_full_standardization_process():
    """Test the complete process of AST creation and standardization."""
    # Create a sample AST from parsed data
    data = [
        "let",
        ".function_form",
        "..Sum",
        "..A",
        "..where",
        "...gamma",
        "....Psum",
        "....tau",
        ".....A",
        ".....gamma",
        "......Order",
        "......A",
        "...rec",
        "....function_form",
        ".....Psum",
        ".....,",
        "......T",
        "......N",
        ".....->",
        "......eq",
        ".......N",
        ".......0",
        "......0",
        "......+",
        ".......gamma",
        "........Psum",
        "........tau",
        ".........T",
        ".........-",
        "..........N",
        "..........1",
        ".......gamma",
        "........T",
        "........N",
        ".gamma",
        "..Print",
        "..gamma",
        "...Sum",
        "...tau",
        "....1",
        "....2",
        "....3",
        "....4",
        "....5"
    ]
    
    ast = ASTFactory.get_abstract_syntax_tree(data)
    
    # Create a StandardizedTree from the AST
    st = StandardizedTree(ast)
    
    # Validate the standardized tree
    assert st.validate()
    
    # Verify some key aspects of the standardized form
    assert st.get_root() is not None
    assert st.get_root().is_standardized
    
    # Specific transformations that should have occurred:
    # 1. 'let' should become 'gamma'
    # 2. 'where' should become standardized
    # 3. 'rec' should become standardized with Y* combinator
    
    # The root should be a gamma node
    assert st.get_root().get_data() == "gamma"