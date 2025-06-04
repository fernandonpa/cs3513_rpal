"""
This module provides the main functionality for normalizing an Abstract Syntax Tree (AST).
"""

from .tree_factory import ASTFactory
from .normalizer_errors import NormalizerError

def normalize_tree(data):
    """
    Normalize the tree represented by the given data.

    Args:
        data (list[str]): The raw data representing the tree structure.

    Returns:
        AST: The normalized Abstract Syntax Tree.

    Raises:
        NormalizerError: If an error occurs during normalization.
    """
    try:
        factory = ASTFactory()
        ast = factory.get_abstract_syntax_tree(data)
        ast.standardize()
        return ast
    except Exception as e:
        raise NormalizerError(f"Error during tree normalization: {str(e)}")