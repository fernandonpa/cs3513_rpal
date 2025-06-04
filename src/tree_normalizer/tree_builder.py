"""
This module defines the AST class for managing the Abstract Syntax Tree (AST).
"""

class AST:
    """
    Represents an Abstract Syntax Tree (AST).

    Attributes:
        root (Node): The root node of the AST.
    """

    def __init__(self, root=None):
        """
        Initialize an AST instance.

        Args:
            root (Node): The root node of the AST.
        """
        self.root = root

    def set_root(self, root):
        """
        Set the root of the AST.

        Args:
            root (Node): The root node to set.
        """
        self.root = root

    def get_root(self):
        """
        Get the root of the AST.

        Returns:
            Node: The root node of the AST.
        """
        return self.root

    def standardize(self):
        """
        Standardize the AST by standardizing the root node.
        """
        if self.root and not self.root.is_standardized:
            self.root.standardize()

    def pre_order_traverse(self, node, depth=0):
        """
        Perform a pre-order traversal of the AST.

        Args:
            node (Node): The current node to traverse.
            depth (int): The current depth for indentation.
        """
        print("." * depth + str(node.get_data()))
        for child in node.get_children():
            self.pre_order_traverse(child, depth + 1)

    def print_ast(self):
        """
        Print the AST using pre-order traversal.
        """
        if self.root:
            self.pre_order_traverse(self.root)