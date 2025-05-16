class Symbol:
    """Base class for all symbols in the CSE machine."""
    
    def __init__(self, value):
        """Initialize a symbol with a value.
        
        Args:
            value: The value stored in the symbol
        """
        self.value = value

    def set_value(self, value):
        """Set the symbol's value.
        
        Args:
            value: The new value to store
        """
        self.value = value

    def get_value(self):
        """Get the symbol's value.
        
        Returns:
            The value stored in the symbol
        """
        return self.value


class Operand(Symbol):
    """Base class for all operands (values) in the CSE machine."""
    
    def __init__(self, value):
        """Initialize an operand with a value.
        
        Args:
            value: The value stored in the operand
        """
        super().__init__(value)

    def get_value(self):
        """Get the operand's value.
        
        Returns:
            The value stored in the operand
        """
        return super().get_value()


class Operator(Symbol):
    """Base class for all operators in the CSE machine."""
    
    def __init__(self, value):
        """Initialize an operator with a value.
        
        Args:
            value: The value stored in the operator
        """
        super().__init__(value)


class BoolValue(Operand):
    """Class for boolean values in the CSE machine."""
    
    def __init__(self, value):
        """Initialize a boolean value.
        
        Args:
            value: The boolean value as a string ('true' or 'false')
        """
        super().__init__(value)


class IntegerValue(Operand):
    """Class for integer values in the CSE machine."""
    
    def __init__(self, value):
        """Initialize an integer value.
        
        Args:
            value: The integer value as a string
        """
        super().__init__(value)


class StringValue(Operand):
    """Class for string values in the CSE machine."""
    
    def __init__(self, value):
        """Initialize a string value.
        
        Args:
            value: The string value
        """
        super().__init__(value)


class Identifier(Operand):
    """Class for identifiers in the CSE machine."""
    
    def __init__(self, value):
        """Initialize an identifier.
        
        Args:
            value: The identifier name
        """
        super().__init__(value)
    
    def get_value(self):
        """Get the identifier's value.
        
        Returns:
            The identifier name
        """
        return super().get_value()


class Tuple(Operand):
    """Class for tuples in the CSE machine."""
    
    def __init__(self):
        """Initialize an empty tuple."""
        super().__init__("tuple")
        self.elements = []


class DummyValue(Operand):
    """Class for the dummy value in the CSE machine."""
    
    def __init__(self):
        """Initialize a dummy value."""
        super().__init__("dummy")


class UnaryOperator(Operator):
    """Class for unary operators in the CSE machine."""
    
    def __init__(self, value):
        """Initialize a unary operator.
        
        Args:
            value: The operator symbol ('neg', 'not', etc.)
        """
        super().__init__(value)


class BinaryOperator(Operator):
    """Class for binary operators in the CSE machine."""
    
    def __init__(self, value):
        """Initialize a binary operator.
        
        Args:
            value: The operator symbol ('+', '*', 'eq', etc.)
        """
        super().__init__(value)


class Environment(Symbol):
    """Class for environment objects in the CSE machine."""
    
    def __init__(self, index):
        """Initialize an environment.
        
        Args:
            index: The environment index
        """
        super().__init__("env")
        self.index = index
        self.parent = None
        self.is_marked_for_deletion = False
        self.bindings = {}

    def set_parent(self, parent_env):
        """Set the parent environment.
        
        Args:
            parent_env: The parent environment object
        """
        self.parent = parent_env

    def get_parent(self):
        """Get the parent environment.
        
        Returns:
            The parent environment object
        """
        return self.parent

    def set_index(self, index):
        """Set the environment index.
        
        Args:
            index: The new index value
        """
        self.index = index

    def get_index(self):
        """Get the environment index.
        
        Returns:
            The environment index
        """
        return self.index

    def mark_for_deletion(self, flag=True):
        """Mark or unmark the environment for deletion.
        
        Args:
            flag: True to mark for deletion, False to unmark
        """
        self.is_marked_for_deletion = flag

    def is_deleted(self):
        """Check if the environment is marked for deletion.
        
        Returns:
            True if the environment is marked for deletion, False otherwise
        """
        return self.is_marked_for_deletion

    def lookup(self, identifier):
        """Look up an identifier in the environment or its parents.
        
        Args:
            identifier: The identifier to look up
            
        Returns:
            The value bound to the identifier, or a new Symbol if not found
        """
        for key in self.bindings:
            if key.get_value() == identifier.get_value():
                return self.bindings[key]
        
        # If not found and has parent, look in parent
        if self.parent is not None:
            return self.parent.lookup(identifier)
        
        # If not found and no parent, return a new symbol with the identifier
        return Symbol(identifier.get_value())


class Delta(Symbol):
    """Class for delta objects (instruction sequences) in the CSE machine."""
    
    def __init__(self, index):
        """Initialize a delta with an index.
        
        Args:
            index: The delta index
        """
        super().__init__("delta")
        self.index = index
        self.instructions = []

    def set_index(self, index):
        """Set the delta index.
        
        Args:
            index: The new index value
        """
        self.index = index

    def get_index(self):
        """Get the delta index.
        
        Returns:
            The delta index
        """
        return self.index


class ControlStructure(Symbol):
    """Class for control structures in the CSE machine."""
    
    def __init__(self):
        """Initialize a control structure."""
        super().__init__("control")
        self.instructions = []


class Lambda(Symbol):
    """Class for lambda (function) objects in the CSE machine."""
    
    def __init__(self, index):
        """Initialize a lambda with an index.
        
        Args:
            index: The lambda index
        """
        super().__init__("lambda")
        self.index = index
        self.environment = None
        self.parameters = []
        self.body = None

    def set_environment(self, env):
        """Set the lambda's environment.
        
        Args:
            env: The environment index
        """
        self.environment = env

    def get_environment(self):
        """Get the lambda's environment.
        
        Returns:
            The environment index
        """
        return self.environment

    def set_body(self, body):
        """Set the lambda's body.
        
        Args:
            body: The delta object representing the lambda's body
        """
        self.body = body

    def get_body(self):
        """Get the lambda's body.
        
        Returns:
            The delta object representing the lambda's body
        """
        return self.body
        
    def get_index(self):
        """Get the lambda index.
        
        Returns:
            The lambda index
        """
        return self.index


class Eta(Symbol):
    """Class for eta (recursive function) objects in the CSE machine."""
    
    def __init__(self):
        """Initialize an eta object."""
        super().__init__("eta")
        self.index = None
        self.environment = None
        self.parameter = None
        self.lambda_func = None

    def set_index(self, index):
        """Set the eta index.
        
        Args:
            index: The new index value
        """
        self.index = index

    def get_index(self):
        """Get the eta index.
        
        Returns:
            The eta index
        """
        return self.index

    def set_environment(self, env):
        """Set the eta's environment.
        
        Args:
            env: The environment index
        """
        self.environment = env

    def get_environment(self):
        """Get the eta's environment.
        
        Returns:
            The environment index
        """
        return self.environment

    def set_parameter(self, parameter):
        """Set the eta's parameter.
        
        Args:
            parameter: The parameter identifier
        """
        self.parameter = parameter

    def set_lambda(self, lambda_func):
        """Set the eta's lambda function.
        
        Args:
            lambda_func: The lambda function object
        """
        self.lambda_func = lambda_func

    def get_lambda(self):
        """Get the eta's lambda function.
        
        Returns:
            The lambda function object
        """
        return self.lambda_func


class Gamma(Symbol):
    """Class for gamma (function application) objects in the CSE machine."""
    
    def __init__(self):
        """Initialize a gamma object."""
        super().__init__("gamma")


class Beta(Symbol):
    """Class for beta (conditional) objects in the CSE machine."""
    
    def __init__(self):
        """Initialize a beta object."""
        super().__init__("beta")


class Tau(Symbol):
    """Class for tau (tuple construction) objects in the CSE machine."""
    
    def __init__(self, size):
        """Initialize a tau object with a size.
        
        Args:
            size: The number of elements in the tuple
        """
        super().__init__("tau")
        self.size = size

    def set_size(self, size):
        """Set the tau size.
        
        Args:
            size: The new size value
        """
        self.size = size

    def get_size(self):
        """Get the tau size.
        
        Returns:
            The tau size
        """
        return self.size


class Ystar(Symbol):
    """Class for Y* (recursion) objects in the CSE machine."""
    
    def __init__(self):
        """Initialize a Y* object."""
        super().__init__("<Y*>")


class ErrorSymbol(Symbol):
    """Class for error symbols in the CSE machine."""
    
    def __init__(self, message=""):
        """Initialize an error symbol with an optional message.
        
        Args:
            message: The error message
        """
        super().__init__("")
        self.message = message