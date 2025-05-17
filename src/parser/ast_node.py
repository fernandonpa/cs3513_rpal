from .node_types import NodeType

class ASTNode:
    """
    Represents a node in the Abstract Syntax Tree (AST) for RPAL
    
    Attributes:
        node_type (NodeType): The type of the node
        value (str): The value associated with the node (if applicable)
        children (list): List of child nodes
        line (int): Source code line number where this node originates
        column (int): Source code column number where this node originates
    """
    
    def __init__(self, node_type, value=None, line=None, column=None):
        """
        Initialize a new AST node
        
        Args:
            node_type (NodeType): The type of this node
            value (str, optional): The value associated with this node
            line (int, optional): Source line number
            column (int, optional): Source column number
        """
        self.node_type = node_type
        self.value = value
        self.children = []
        self.line = line
        self.column = column
    
    def add_child(self, child):
        """Add a child node to this node"""
        self.children.append(child)
    
    def add_children(self, children):
        """Add multiple child nodes to this node"""
        self.children.extend(children)
    
    def child_count(self):
        """Return the number of child nodes"""
        return len(self.children)
    
    def __str__(self):
        """String representation of the node"""
        if self.value is not None:
            return f"{self.node_type.name}({self.value})"
        return f"{self.node_type.name}"
    
    def __repr__(self):
        """Formal string representation of the node"""
        return self.__str__()
    
    def to_structured_string(self, indent=0):
        """
        Convert the node to a structured string representation (for debugging)
        
        Args:
            indent (int): Current indentation level
            
        Returns:
            str: A formatted string representation of the AST
        """
        result = " " * indent
        result += self.__str__() + "\n"
        
        for child in self.children:
            result += child.to_structured_string(indent + 2)
            
        return result