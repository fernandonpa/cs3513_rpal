class Node:
    """Represents a node in the Abstract Syntax Tree (AST) for RPAL.
    
    The AST is a tree representation of the syntactic structure of RPAL source code.
    Each node represents a construct in the source code, with its type indicating
    the construct's category (e.g., function declaration, variable reference, etc.).
    
    Attributes:
        type (str): The type or category of this AST node (e.g., 'let', 'lambda', 'apply').
        value (str): The value associated with this node, if applicable.
        no_of_children (int): The number of child nodes this node has.
    """
    
    def __init__(self, node_type, value, children):
        """Initialize a new AST node.
        
        Args:
            node_type (str): The type or category of this AST node.
            value (str): The value associated with this node (may be None if not applicable).
            children (int): The number of child nodes this node should have.
        """
        self.type = node_type          # Stores the node's syntactic category (e.g., 'let', 'identifier')
        self.value = value             # Stores any associated value (e.g., variable name for identifiers)
        self.no_of_children = children # Tracks how many child nodes are expected for this construct