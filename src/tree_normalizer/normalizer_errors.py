class StandardizerError(Exception):
    """Base class for all standardizer-related errors."""
    pass


class ASTError(StandardizerError):
    """Base class for errors related to Abstract Syntax Tree operations."""
    pass


class ASTConstructionError(ASTError):
    """Exception raised when there's an error constructing an AST."""
    pass


class StandardizationError(StandardizerError):
    """Exception raised when there's an error during standardization process."""
    pass


class STError(StandardizerError):
    """Base class for errors related to Standardized Tree operations."""
    pass


class InvalidNodeTypeError(StandardizerError):
    """Exception raised when an operation is attempted on a node of invalid type."""
    
    def __init__(self, node_type, expected_types=None, message=None):
        if message is None:
            if expected_types:
                message = f"Expected node of type {expected_types}, but got {node_type}"
            else:
                message = f"Invalid node type: {node_type}"
        super().__init__(message)
        self.node_type = node_type
        self.expected_types = expected_types


class InvalidTreeStructureError(StandardizerError):
    """Exception raised when the tree structure is invalid for an operation."""
    pass