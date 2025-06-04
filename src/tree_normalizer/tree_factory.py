"""
This module defines the ASTFactory class for building an Abstract Syntax Tree (AST) from raw data.
"""

from .syntax_node import Node
from .tree_builder import AST

class ASTFactory:
    """
    Factory class for building an Abstract Syntax Tree (AST) from raw data.
    """

    def __init__(self):
        """
        Initialize an ASTFactory instance.
        """
        pass

    def get_abstract_syntax_tree(self, data):
        """
        Build an Abstract Syntax Tree (AST) from raw data.

        Args:
            data (list[str]): The raw data representing the tree structure.

        Returns:
            AST: The constructed Abstract Syntax Tree.
        """
        root = self._create_node(data[0], 0)
        previous_node = root
        current_depth = 0

        for line in data[1:]:
            depth = line.count(".")
            node_data = line[depth:]
            current_node = self._create_node(node_data, depth)

            if depth > current_depth:
                previous_node.get_children().append(current_node)
                current_node.set_parent(previous_node)
            else:
                while previous_node.get_depth() != depth:
                    previous_node = previous_node.get_parent()
                previous_node.get_parent().get_children().append(current_node)
                current_node.set_parent(previous_node.get_parent())

            previous_node = current_node
            current_depth = depth

        return AST(root)

    def _create_node(self, data, depth):
        """
        Create a new node with the given data and depth.

        Args:
            data (str): The data for the node.
            depth (int): The depth of the node.

        Returns:
            Node: The created node.
        """
        node = Node()
        node.set_data(data)
        node.set_depth(depth)
        return node