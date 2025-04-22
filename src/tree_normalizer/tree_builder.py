from typing import Optional, List, Tuple
from .syntax_node import Node, StandardizationError

class AST:
    """Abstract Syntax Tree implementation for RPAL language."""
    
    def __init__(self, root: Optional[Node] = None):
        """Initialize an AST with an optional root node."""
        self.root = root
    
    def set_root(self, root: Node) -> None:
        """Set the root node of the AST."""
        self.root = root
    
    def get_root(self) -> Optional[Node]:
        """Get the root node of the AST."""
        return self.root
    
    def standardize(self) -> None:
        """Convert the AST to a Standardized Tree (ST)."""
        if not self.root:
            raise StandardizationError("Cannot standardize an empty AST.")
        
        if not self.root.is_standardized:
            self.root.standardize()
    
    def pre_order_traverse(self, node: Node, level: int = 0) -> List[Tuple[int, str]]:
        """
        Perform a pre-order traversal of the tree starting from the given node.
        
        Args:
            node: The starting node for traversal
            level: The indentation level
            
        Returns:
            A list of tuples containing (level, node_data) for each node
        """
        result = [(level, str(node.get_data()))]
        
        for child in node.get_children():
            result.extend(self.pre_order_traverse(child, level + 1))
            
        return result
    
    def print_ast(self) -> None:
        """Print the AST in a pre-order traversal format with proper indentation."""
        if not self.root:
            print("Empty AST")
            return
            
        traversal = self.pre_order_traverse(self.root)
        for level, data in traversal:
            print("." * level + data)
    
    def to_string(self) -> str:
        """Convert the AST to a string representation."""
        if not self.root:
            return "Empty AST"
            
        traversal = self.pre_order_traverse(self.root)
        return "\n".join(["." * level + data for level, data in traversal])