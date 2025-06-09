import pytest
from src.cse_machine.machine import CSEMachine
from src.cse_machine.nodes.symbol import Symbol
from src.cse_machine.nodes.id import Id
from src.cse_machine.nodes.int import Int
from src.cse_machine.nodes.str import Str
from src.cse_machine.nodes.bool import Bool
from src.cse_machine.nodes.lmbda import Lambda
from src.cse_machine.nodes.gamma import Gamma
from src.cse_machine.nodes.e import E
from src.cse_machine.nodes.beta import Beta
from src.cse_machine.nodes.tau import Tau
from src.cse_machine.nodes.tup import Tup
from src.cse_machine.nodes.bop import Bop
from src.cse_machine.nodes.uop import Uop
from src.cse_machine.nodes.delta import Delta
from src.cse_machine.nodes.b import B
import tempfile
import os

class TestCSEMachine:
    """Test suite for CSEMachine class."""
    
    def test_init(self):
        """Test CSEMachine initialization."""
        control = [Int("5")]
        stack = []
        environment = [{}]
        
        machine = CSEMachine(control, stack, environment)
        
        assert machine.control == control
        assert machine.stack == stack
        assert machine.environment == environment
    
    def test_convert_string_to_bool_true(self):
        """Test conversion of string 'true' to boolean."""
        machine = CSEMachine([], [], [{}])
        result = machine.covert_string_to_bool("true")
        assert result is True
    
    def test_convert_string_to_bool_false(self):
        """Test conversion of string 'false' to boolean."""
        machine = CSEMachine([], [], [{}])
        result = machine.covert_string_to_bool("false")
        assert result is False
    
    def test_apply_unary_operation_neg(self):
        """Test unary negation operation."""
        machine = CSEMachine([], [], [{}])
        rator = Uop("neg")
        rand = Int("5")
        
        result = machine.apply_unary_operation(rator, rand)
        
        assert isinstance(result, Int)
        assert result.get_data() == "-5"
    
    def test_apply_unary_operation_not(self):
        """Test unary not operation."""
        machine = CSEMachine([], [], [{}])
        rator = Uop("not")
        rand = Bool("true")
        
        result = machine.apply_unary_operation(rator, rand)
        
        assert isinstance(result, Bool)
        assert result.get_data() == "false"
    
    def test_apply_binary_operation_addition(self):
        """Test binary addition operation."""
        machine = CSEMachine([], [], [{}])
        rator = Bop("+")
        rand1 = Int("3")
        rand2 = Int("5")
        
        result = machine.apply_binary_operation(rator, rand1, rand2)
        
        assert isinstance(result, Int)
        assert result.get_data() == "8"
    
    def test_apply_binary_operation_subtraction(self):
        """Test binary subtraction operation."""
        machine = CSEMachine([], [], [{}])
        rator = Bop("-")
        rand1 = Int("10")
        rand2 = Int("3")
        
        result = machine.apply_binary_operation(rator, rand1, rand2)
        
        assert isinstance(result, Int)
        assert result.get_data() == "7"
    
    def test_apply_binary_operation_multiplication(self):
        """Test binary multiplication operation."""
        machine = CSEMachine([], [], [{}])
        rator = Bop("*")
        rand1 = Int("4")
        rand2 = Int("6")
        
        result = machine.apply_binary_operation(rator, rand1, rand2)
        
        assert isinstance(result, Int)
        assert result.get_data() == "24"
    
    def test_apply_binary_operation_division(self):
        """Test binary division operation."""
        machine = CSEMachine([], [], [{}])
        rator = Bop("/")
        rand1 = Int("15")
        rand2 = Int("3")
        
        result = machine.apply_binary_operation(rator, rand1, rand2)
        
        assert isinstance(result, Int)
        assert result.get_data() == "5"
    
    def test_apply_binary_operation_power(self):
        """Test binary power operation."""
        machine = CSEMachine([], [], [{}])
        rator = Bop("**")
        rand1 = Int("2")
        rand2 = Int("3")
        
        result = machine.apply_binary_operation(rator, rand1, rand2)
        
        assert isinstance(result, Int)
        assert result.get_data() == "8"
    
    def test_apply_binary_operation_logical_and(self):
        """Test binary logical and operation."""
        machine = CSEMachine([], [], [{}])
        rator = Bop("&")
        rand1 = Bool("true")
        rand2 = Bool("false")
        
        result = machine.apply_binary_operation(rator, rand1, rand2)
        
        assert isinstance(result, Bool)
        assert result.get_data() == "false"
    
    def test_apply_binary_operation_logical_or(self):
        """Test binary logical or operation."""
        machine = CSEMachine([], [], [{}])
        rator = Bop("or")
        rand1 = Bool("true")
        rand2 = Bool("false")
        
        result = machine.apply_binary_operation(rator, rand1, rand2)
        
        assert isinstance(result, Bool)
        assert result.get_data() == "true"
    
    def test_apply_binary_operation_equality(self):
        """Test binary equality operation."""
        machine = CSEMachine([], [], [{}])
        rator = Bop("eq")
        rand1 = Int("5")
        rand2 = Int("5")
        
        result = machine.apply_binary_operation(rator, rand1, rand2)
        
        assert isinstance(result, Bool)
        assert result.get_data() == "true"
    
    def test_apply_binary_operation_not_equal(self):
        """Test binary not equal operation."""
        machine = CSEMachine([], [], [{}])
        rator = Bop("ne")
        rand1 = Int("5")
        rand2 = Int("3")
        
        result = machine.apply_binary_operation(rator, rand1, rand2)
        
        assert isinstance(result, Bool)
        assert result.get_data() == "true"
    
    def test_apply_binary_operation_less_than(self):
        """Test binary less than operation."""
        machine = CSEMachine([], [], [{}])
        rator = Bop("ls")
        rand1 = Int("3")
        rand2 = Int("5")
        
        result = machine.apply_binary_operation(rator, rand1, rand2)
        
        assert isinstance(result, Bool)
        assert result.get_data() == "true"
    
    def test_apply_binary_operation_greater_than(self):
        """Test binary greater than operation."""
        machine = CSEMachine([], [], [{}])
        rator = Bop("gr")
        rand1 = Int("7")
        rand2 = Int("3")
        
        result = machine.apply_binary_operation(rator, rand1, rand2)
        
        assert isinstance(result, Bool)
        assert result.get_data() == "true"
    
    
    def test_execute_simple_integer(self):
        """Test executing a simple integer value."""
        control = [Int("42")]
        stack = []
        environment = [{}]
        
        machine = CSEMachine(control, stack, environment)
        machine.execute()
        
        assert len(machine.stack) == 1
        assert isinstance(machine.stack[0], Int)
        assert machine.stack[0].get_data() == "42"
    
    def test_execute_simple_string(self):
        """Test executing a simple string value."""
        control = [Str("hello")]
        stack = []
        environment = [{}]
        
        machine = CSEMachine(control, stack, environment)
        machine.execute()
        
        assert len(machine.stack) == 1
        assert isinstance(machine.stack[0], Str)
        assert machine.stack[0].get_data() == "hello"
    
    def test_execute_simple_boolean(self):
        """Test executing a simple boolean value."""
        control = [Bool("true")]
        stack = []
        environment = [{}]
        
        machine = CSEMachine(control, stack, environment)
        machine.execute()
        
        assert len(machine.stack) == 1
        assert isinstance(machine.stack[0], Bool)
        assert machine.stack[0].get_data() == "true"
    
    def test_clear_file(self):
        """Test clearing a file."""
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test content")
            temp_path = f.name
        
        try:
            CSEMachine.clear_file(temp_path)
            
            with open(temp_path, 'r') as f:
                content = f.read()
                assert content == ""
        finally:
            os.unlink(temp_path)