from typing import List, Optional, Dict, Any
from .syntax_node import Node
from .tree_builder import AST
from .normalizer_errors import StandardizationError, STError


class StandardizedTree:
    """
    Represents a Standardized Tree (ST) for RPAL language.
    The ST is derived from an AST through standardization transformations.
    """
    
    def __init__(self, ast: Optional[AST] = None):
        """
        Initialize a StandardizedTree with an optional AST.
        If an AST is provided, it will be standardized.
        
        Args:
            ast: Optional AST to standardize
        """
        self.root: Optional[Node] = None
        
        if ast:
            self.from_ast(ast)
    
    def from_ast(self, ast: AST) -> None:
        """
        Convert an AST to a Standardized Tree.
        
        Args:
            ast: The AST to standardize
            
        Raises:
            StandardizationError: If standardization fails
        """
        if not ast.get_root():
            raise StandardizationError("Cannot standardize empty AST")
        
        # Create a deep copy of the AST to avoid modifying the original
        self.root = self._deep_copy_node(ast.get_root())
        
        # Standardize the copied tree
        if self.root:
            self.root.standardize()
    
    def _deep_copy_node(self, node: Optional[Node]) -> Optional[Node]:
        """Create a deep copy of a node and its subtree."""
        if node is None:
            return None
            
        # Create a new node with the same data and depth
        new_node = Node(node.get_data(), node.get_depth())
        
        # Copy children recursively
        for child in node.get_children():
            new_child = self._deep_copy_node(child)
            if new_child:
                new_child.set_parent(new_node)
                new_node.children.append(new_child)
                
        return new_node
    
    def get_root(self) -> Optional[Node]:
        """Get the root node of the standardized tree."""
        return self.root
    
    def print_st(self) -> None:
        """Print the standardized tree with proper indentation."""
        if not self.root:
            print("Empty Standardized Tree")
            return
            
        self._print_node(self.root, 0)
    
    def _print_node(self, node: Node, level: int) -> None:
        """Print a node and its subtree with indentation based on level."""
        print("." * level + str(node.get_data()))
        
        for child in node.get_children():
            self._print_node(child, level + 1)
    
    def to_string(self) -> str:
        """Convert the standardized tree to a string representation."""
        if not self.root:
            return "Empty Standardized Tree"
            
        result = []
        self._node_to_string(self.root, 0, result)
        return "\n".join(result)
    
    def _node_to_string(self, node: Node, level: int, result: List[str]) -> None:
        """Convert a node and its subtree to string representation with indentation."""
        result.append("." * level + str(node.get_data()))
        
        for child in node.get_children():
            self._node_to_string(child, level + 1, result)
    
    def validate(self) -> bool:
        """
        Validate that the tree is properly standardized.
        
        Returns:
            True if the tree is a valid standardized tree, False otherwise
        """
        if not self.root:
            return True
            
        return self._validate_node(self.root)
    
    def _validate_node(self, node: Node) -> bool:
        """
        Validate that a node and its subtree conform to standardized form.
        
        Args:
            node: The node to validate
            
        Returns:
            True if the node and its subtree are valid, False otherwise
        """
        # Check that certain constructs are not present in standardized tree
        if node.get_data() in ["let", "where", "within", "rec", "and", "@"]:
            return False
            
        # Check for function_form with more than 2 children
        if node.get_data() == "function_form" and len(node.get_children()) > 2:
            return False
            
        # Check for lambda with more than 2 children
        if node.get_data() == "lambda" and len(node.get_children()) > 2:
            return False
            
        # Recursively validate children
        for child in node.get_children():
            if not self._validate_node(child):
                return False
                
        return True