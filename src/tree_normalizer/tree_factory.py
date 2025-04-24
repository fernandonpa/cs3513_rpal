from typing import List
from .syntax_node import Node, NodeFactory
from .tree_builder import AST


class ASTFactory:
    """Factory class for creating Abstract Syntax Trees from parsed data."""
    
    @staticmethod
    def get_abstract_syntax_tree(data: List[str]) -> AST:
        """
        Create an AST from a list of strings representing nodes with depth.
        
        Args:
            data: List of strings where each string represents a node with its depth
                 (e.g., "...<ID:foo>" where dots represent depth)
                 
        Returns:
            An AST with the constructed tree
            
        Raises:
            ASTConstructionError: If there's an error in constructing the AST
        """
        if not data:
            raise ASTConstructionError("Cannot create AST from empty data")
            
        try:
            # Create the root node
            root = NodeFactory.create(data[0], 0)
            previous_node = root
            current_depth = 0
            
            for s in data[1:]:
                # Calculate depth based on leading dots
                i = 0
                d = 0
                while i < len(s) and s[i] == '.':
                    d += 1
                    i += 1
                
                # Create current node
                node_data = s[i:]
                current_node = NodeFactory.create(node_data, d)
                
                # Determine where to add this node in the tree
                if current_depth < d:
                    # This is a child of the previous node
                    previous_node.children.append(current_node)
                    current_node.set_parent(previous_node)
                else:
                    # Need to find the right parent
                    parent_node = previous_node
                    while parent_node.get_depth() != d - 1:
                        parent_node = parent_node.get_parent()
                        if parent_node is None:
                            raise ASTConstructionError(f"Invalid tree structure at node: {node_data}")
                    
                    parent_node.children.append(current_node)
                    current_node.set_parent(parent_node)
                
                previous_node = current_node
                current_depth = d
                
            return AST(root)
            
        except Exception as e:
            if isinstance(e, ASTConstructionError):
                raise
            raise ASTConstructionError(f"Error constructing AST: {str(e)}")


class ASTConstructionError(Exception):
    """Exception raised for errors during AST construction."""
    pass