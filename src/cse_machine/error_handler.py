class CSEMachineError(Exception):
    """Base exception class for CSE machine errors."""
    
    def __init__(self, message="CSE Machine Error"):
        """Initialize a CSE machine error.
        
        Args:
            message: The error message
        """
        self.message = message
        super().__init__(self.message)


class OperationError(CSEMachineError):
    """Exception raised for errors during operation execution."""
    
    def __init__(self, operation, message=None):
        """Initialize an operation error.
        
        Args:
            operation: The operation that caused the error
            message: Optional specific error message
        """
        if message is None:
            message = f"Error executing operation: {operation}"
        super().__init__(message)
        self.operation = operation


class TypeMismatchError(CSEMachineError):
    """Exception raised for type mismatches in operations."""
    
    def __init__(self, expected_type, actual_type, operation=None):
        """Initialize a type mismatch error.
        
        Args:
            expected_type: The expected type
            actual_type: The actual type
            operation: Optional operation that caused the error
        """
        message = f"Type mismatch: expected {expected_type}, got {actual_type}"
        if operation:
            message += f" in operation {operation}"
        super().__init__(message)
        self.expected_type = expected_type
        self.actual_type = actual_type
        self.operation = operation


class UndefinedSymbolError(CSEMachineError):
    """Exception raised for undefined symbols."""
    
    def __init__(self, symbol_name):
        """Initialize an undefined symbol error.
        
        Args:
            symbol_name: The name of the undefined symbol
        """
        super().__init__(f"Undefined symbol: {symbol_name}")
        self.symbol_name = symbol_name


class InvalidArgumentError(CSEMachineError):
    """Exception raised for invalid arguments to functions."""
    
    def __init__(self, function_name, expected, actual=None):
        """Initialize an invalid argument error.
        
        Args:
            function_name: The name of the function
            expected: Description of the expected arguments
            actual: Optional description of the actual arguments
        """
        message = f"Invalid argument to {function_name}: expected {expected}"
        if actual:
            message += f", got {actual}"
        super().__init__(message)
        self.function_name = function_name
        self.expected = expected
        self.actual = actual


class DivisionByZeroError(CSEMachineError):
    """Exception raised for division by zero."""
    
    def __init__(self):
        """Initialize a division by zero error."""
        super().__init__("Division by zero")


class StackUnderflowError(CSEMachineError):
    """Exception raised when trying to pop from an empty stack."""
    
    def __init__(self, stack_name):
        """Initialize a stack underflow error.
        
        Args:
            stack_name: The name of the stack (control, value, or environment)
        """
        super().__init__(f"Stack underflow: {stack_name} stack is empty")
        self.stack_name = stack_name


class RecursionDepthExceededError(CSEMachineError):
    """Exception raised when recursion depth is exceeded."""
    
    def __init__(self, depth_limit):
        """Initialize a recursion depth exceeded error.
        
        Args:
            depth_limit: The maximum recursion depth
        """
        super().__init__(f"Recursion depth limit exceeded: {depth_limit}")
        self.depth_limit = depth_limit