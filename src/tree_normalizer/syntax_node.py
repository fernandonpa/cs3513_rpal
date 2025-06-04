"""
This module defines the Node class for representing nodes in the syntax tree and the NodeFactory for creating nodes.
"""

from .normalizer_errors import NormalizerError
from enum import Enum


class NodeFactory:
    """
    Factory class for creating nodes in the syntax tree.
    """

    @staticmethod
    def get_node(data, depth):
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

    @staticmethod
    def get_node_with_parent(data, depth, parent, children, is_standardized):
        """
        Create a new node with the given data, depth, parent, and children.

        Args:
            data (str): The data for the node.
            depth (int): The depth of the node.
            parent (Node): The parent node.
            children (list[Node]): The child nodes.
            is_standardized (bool): Whether the node is standardized.

        Returns:
            Node: The created node.
        """
        node = Node()
        node.set_data(data)
        node.set_depth(depth)
        node.set_parent(parent)
        node.children = children
        node.is_standardized = is_standardized
        return node

class Node:
    """
    Represents a node in the syntax tree.

    Attributes:
        data (str): The data stored in the node.
        depth (int): The depth of the node in the tree.
        parent (Node): The parent node.
        children (list[Node]): The child nodes.
        is_standardized (bool): Whether the node has been standardized.
    """

    def __init__(self):
        """
        Initialize a Node instance.
        """
        self.data = None
        self.depth = 0
        self.parent = None
        self.children = []
        self.is_standardized = False

    def set_data(self, data):
        """
        Set the data of the node.

        Args:
            data (str): The data to set.
        """
        self.data = data

    def get_data(self):
        """
        Get the data of the node.

        Returns:
            str: The data of the node.
        """
        return self.data

    def set_depth(self, depth):
        """
        Set the depth of the node.

        Args:
            depth (int): The depth to set.
        """
        self.depth = depth

    def get_depth(self):
        """
        Get the depth of the node.

        Returns:
            int: The depth of the node.
        """
        return self.depth

    def set_parent(self, parent):
        """
        Set the parent of the node.

        Args:
            parent (Node): The parent node.
        """
        self.parent = parent

    def get_parent(self):
        """
        Get the parent of the node.

        Returns:
            Node: The parent node.
        """
        return self.parent

    def get_children(self):
        """
        Get the children of the node.

        Returns:
            list[Node]: The child nodes.
        """
        return self.children

    def get_degree(self):
        """
        Get the degree (number of children) of the node.

        Returns:
            int: The number of children.
        """
        return len(self.children)

    def standardize(self):
        """
        Standardize the node and its children.

        Raises:
            NormalizerError: If an error occurs during standardization.
        """
        if not self.is_standardized:
            for child in self.children:
                child.standardize()

            try:
                if self.data == "let":
                    self._standardize_let()
                elif self.data == "where":
                    self._standardize_where()
                elif self.data == "function_form":
                    self._standardize_function_form()
                elif self.data == "lambda":
                    self._standardize_lambda()
                elif self.data == "within":
                    self._standardize_within()
                elif self.data == "@":
                    self._standardize_at()
                elif self.data == "and":
                    self._standardize_and()
                elif self.data == "rec":
                    self._standardize_rec()
            except Exception as e:
                raise NormalizerError(f"Error during standardization of node '{self.data}': {str(e)}")

            self.is_standardized = True

    def _standardize_let(self):
        """
        Standardize a 'let' node.

        Transformation:
            LET              GAMMA
          /     \           /     \
        EQUAL   P   ->   LAMBDA   E
        /   \             /    \
       X     E           X      P
        """
        temp1 = self.children[0].children[1]
        temp1.set_parent(self)
        temp1.set_depth(self.depth + 1)
        temp2 = self.children[1]
        temp2.set_parent(self.children[0])
        temp2.set_depth(self.depth + 2)
        self.children[1] = temp1
        self.children[0].set_data("lambda")
        self.children[0].children[1] = temp2
        self.set_data("gamma")

    def _standardize_where(self):
        """
        Standardize a 'where' node.

        Transformation:
            WHERE               LET
           /   \             /     \
          P    EQUAL   ->  EQUAL   P
               /   \       /   \
              X     E     X     E
        """
        temp = self.children[0]
        self.children[0] = self.children[1]
        self.children[1] = temp
        self.set_data("let")
        self.standardize()

    def _standardize_function_form(self):
        """
        Standardize a 'function_form' node.

        Transformation:
            FCN_FORM                EQUAL
           /   |   \              /    \
          P    V+   E    ->      P     +LAMBDA
                                    /     \
                                   V     .E
        """
        Ex = self.children[-1]
        current_lambda = NodeFactory.get_node_with_parent("lambda", self.depth + 1, self, [], True)
        self.children.insert(1, current_lambda)

        i = 2
        while self.children[i] != Ex:
            V = self.children[i]
            self.children.pop(i)
            V.set_depth(current_lambda.depth + 1)
            V.set_parent(current_lambda)
            current_lambda.children.append(V)

            if len(self.children) > 3:
                current_lambda = NodeFactory.get_node_with_parent("lambda", current_lambda.depth + 1, current_lambda, [], True)
                current_lambda.get_parent().children.append(current_lambda)

        current_lambda.children.append(Ex)
        self.children.pop(2)
        self.set_data("=")

    def _standardize_lambda(self):
        """
        Standardize a 'lambda' node.

        Transformation:
            LAMBDA        LAMBDA
             /   \   ->   /    \
            V++   E      V     .E
        """
        if len(self.children) > 2:
            Ey = self.children[-1]
            current_lambda = NodeFactory.get_node_with_parent("lambda", self.depth + 1, self, [], True)
            self.children.insert(1, current_lambda)

            i = 2
            while self.children[i] != Ey:
                V = self.children[i]
                self.children.pop(i)
                V.set_depth(current_lambda.depth + 1)
                V.set_parent(current_lambda)
                current_lambda.children.append(V)

                if len(self.children) > 3:
                    current_lambda = NodeFactory.get_node_with_parent("lambda", current_lambda.depth + 1, current_lambda, [], True)
                    current_lambda.get_parent().children.append(current_lambda)

            current_lambda.children.append(Ey)
            self.children.pop(2)

    def _standardize_within(self):
        """
        Standardize a 'within' node.

        Transformation:
            WITHIN                  EQUAL
           /      \                /     \
         EQUAL   EQUAL    ->      X2     GAMMA
        /    \   /    \                  /    \
       X1    E1 X2    E2               LAMBDA  E1
                                        /    \
                                       X1    E2
        """
        X1 = self.children[0].children[0]
        X2 = self.children[1].children[0]
        E1 = self.children[0].children[1]
        E2 = self.children[1].children[1]
        gamma = NodeFactory.get_node_with_parent("gamma", self.depth + 1, self, [], True)
        lambda_ = NodeFactory.get_node_with_parent("lambda", self.depth + 2, gamma, [], True)
        X1.set_depth(X1.get_depth() + 1)
        X1.set_parent(lambda_)
        X2.set_depth(X1.get_depth() - 1)
        X2.set_parent(self)
        E1.set_depth(E1.get_depth())
        E1.set_parent(gamma)
        E2.set_depth(E2.get_depth() + 1)
        E2.set_parent(lambda_)
        lambda_.children.append(X1)
        lambda_.children.append(E2)
        gamma.children.append(lambda_)
        gamma.children.append(E1)
        self.children.clear()
        self.children.append(X2)
        self.children.append(gamma)
        self.set_data("=")

    def _standardize_at(self):
        """
        Standardize an '@' node.

        Transformation:
            AT              GAMMA
          / | \    ->       /    \
         E1 N E2          GAMMA   E2
                          /    \
                         N     E1
        """
        gamma1 = NodeFactory.get_node_with_parent("gamma", self.depth + 1, self, [], True)
        e1 = self.children[0]
        e1.set_depth(e1.get_depth() + 1)
        e1.set_parent(gamma1)
        n = self.children[1]
        n.set_depth(n.get_depth() + 1)
        n.set_parent(gamma1)
        gamma1.children.append(n)
        gamma1.children.append(e1)
        self.children.pop(0)
        self.children.pop(0)
        self.children.insert(0, gamma1)
        self.set_data("gamma")

    def _standardize_and(self):
        """
        Standardize an 'and' node.

        Transformation:
            SIMULTDEF            EQUAL
                |               /     \
              EQUAL++  ->     COMMA   TAU
              /   \             |      |
             X     E           X++    E++
        """
        comma = NodeFactory.get_node_with_parent(",", self.depth + 1, self, [], True)
        tau = NodeFactory.get_node_with_parent("tau", self.depth + 1, self, [], True)

        for equal in self.children:
            equal.children[0].set_parent(comma)
            equal.children[1].set_parent(tau)
            comma.children.append(equal.children[0])
            tau.children.append(equal.children[1])

        self.children.clear()
        self.children.append(comma)
        self.children.append(tau)
        self.set_data("=")

    def _standardize_rec(self):
        """
        Standardize a 'rec' node.

        Transformation:
            REC                 EQUAL
             |                 /     \
           EQUAL     ->       X     GAMMA
          /     \                   /    \
         X       E                YSTAR  LAMBDA
                                    /     \
                                   X      E
        """
        X = self.children[0].children[0]
        E = self.children[0].children[1]
        F = NodeFactory.get_node_with_parent(X.get_data(), self.depth + 1, self, X.children, True)
        G = NodeFactory.get_node_with_parent("gamma", self.depth + 1, self, [], True)
        Y = NodeFactory.get_node_with_parent("<Y*>", self.depth + 2, G, [], True)
        L = NodeFactory.get_node_with_parent("lambda", self.depth + 2, G, [], True)

        X.set_depth(L.depth + 1)
        X.set_parent(L)
        E.set_depth(L.depth + 1)
        E.set_parent(L)
        L.children.append(X)
        L.children.append(E)
        G.children.append(Y)
        G.children.append(L)
        self.children.clear()
        self.children.append(F)
        self.children.append(G)
        self.set_data("=")

