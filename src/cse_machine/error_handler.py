class CSEError(Exception):
    """Base exception for CSE machine errors"""
    pass

class TypeMismatchError(CSEError):
    """Raised when an operation receives operands of incorrect types"""
    def __init__(self, operation, expected, received):
        self.operation = operation
        self.expected = expected
        self.received = received
        message = f"Type mismatch in {operation}: expected {expected}, got {received}"
        super().__init__(message)

class UndefinedOperationError(CSEError):
    """Raised when an undefined operation is attempted"""
    def __init__(self, operation):
        self.operation = operation
        message = f"Undefined operation: {operation}"
        super().__init__(message)

class DivisionByZeroError(CSEError):
    """Raised when a division by zero is attempted"""
    def __init__(self):
        super().__init__("Division by zero")

class UnboundIdentifierError(CSEError):
    """Raised when an unbound identifier is referenced"""
    def __init__(self, identifier):
        self.identifier = identifier
        message = f"Unbound identifier: {identifier}"
        super().__init__(message)

class IndexOutOfBoundsError(CSEError):
    """Raised when a tuple index is out of bounds"""
    def __init__(self, index, size):
        self.index = index
        self.size = size
        message = f"Index {index} out of bounds for tuple of size {size}"
        super().__init__(message)

def handle_error(error, recovery_value=None):
    """Handle CSE errors with appropriate recovery or propagation"""
    from .nodes import Err
    print(f"CSE Error: {error}")
    if recovery_value is not None:
        return recovery_value
    return Err()