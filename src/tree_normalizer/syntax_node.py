from abc import ABC, abstractmethod
from typing import List, Optional, Union


class Node:
    """Base class for all AST and ST nodes."""
    
    def __init__(self, data: str, depth: int = 0, parent=None):
        self.data = data
        self.depth = depth
        self.parent = parent
        self.children: List['Node'] = []
        self.is_standardized = False
        
    def __str__(self) -> str:
        """String representation of the node."""
        return self.data
    
    def set_data(self, data: str) -> None:
        """Set the data for this node."""
        self.data = data
        
    def get_data(self) -> str:
        """Get the data for this node."""
        return self.data
    
    def get_degree(self) -> int:
        """Get the number of children."""
        return len(self.children)
    
    def get_children(self) -> List['Node']:
        """Get the children of this node."""
        return self.children
    
    def set_depth(self, depth: int) -> None:
        """Set the depth of this node."""
        self.depth = depth
        
    def get_depth(self) -> int:
        """Get the depth of this node."""
        return self.depth
    
    def set_parent(self, parent: Optional['Node']) -> None:
        """Set the parent of this node."""
        self.parent = parent
        
    def get_parent(self) -> Optional['Node']:
        """Get the parent of this node."""
        return self.parent
    
    def add_child(self, child: 'Node') -> None:
        """Add a child to this node."""
        child.set_parent(self)
        self.children.append(child)
    
    def standardize(self) -> None:
        """Standardize this node and its children according to RPAL transformation rules."""
        if not self.is_standardized:
            # First standardize all children
            for child in self.children:
                child.standardize()
            
            # Then apply specific transformation rules based on node type
            self._apply_transformation()
            
            self.is_standardized = True
    
    def _apply_transformation(self) -> None:
        """Apply specific transformation rules based on node type."""
        if self.data == "let":
            self._transform_let()
        elif self.data == "where":
            self._transform_where()
        elif self.data == "function_form":
            self._transform_function_form()
        elif self.data == "lambda":
            self._transform_lambda()
        elif self.data == "within":
            self._transform_within()
        elif self.data == "@":
            self._transform_at()
        elif self.data == "and":
            self._transform_and()
        elif self.data == "rec":
            self._transform_rec()

    def _transform_let(self) -> None:
        """
        Standardize LET node:
              LET              GAMMA
            /     \           /     \
           EQUAL   P   ->   LAMBDA   E
          /   \             /    \
         X     E           X      P 
        """
        if len(self.children) != 2 or self.children[0].get_data() != "=":
            raise StandardizationError("LET transformation requires exactly 2 children with first child as EQUAL")
        
        # Extract components
        equal_node = self.children[0]
        P = self.children[1]
        
        if len(equal_node.children) != 2:
            raise StandardizationError("EQUAL node in LET must have exactly 2 children")
            
        X = equal_node.children[0]
        E = equal_node.children[1]
        
        # Create new lambda node
        equal_node.set_data("lambda")
        
        # Move P to be a child of the lambda
        P.set_parent(equal_node)
        P.set_depth(self.depth + 2)
        equal_node.children[1] = P
        
        # Move E to be a child of the top-level gamma
        E.set_parent(self)
        E.set_depth(self.depth + 1)
        self.children[1] = E
        
        # Change self to gamma
        self.set_data("gamma")

    def _transform_where(self) -> None:
        """
        Standardize WHERE node:
              WHERE               LET
              /   \             /     \
             P    EQUAL   ->  EQUAL   P
                  /   \       /   \
                 X     E     X     E
        """
        if len(self.children) != 2:
            raise StandardizationError("WHERE transformation requires exactly 2 children")
            
        # Swap children
        temp = self.children[0]
        self.children[0] = self.children[1]
        self.children[1] = temp
        
        # Change node type and re-standardize
        self.set_data("let")
        self.is_standardized = False
        self.standardize()

    def _transform_function_form(self) -> None:
        """
        Standardize FUNCTION_FORM node:
              FCN_FORM                EQUAL
              /   |   \              /    \
             P    V+   E    ->      P     +LAMBDA
                                           /     \
                                          V     .E
        """
        if len(self.children) < 2:
            raise StandardizationError("FUNCTION_FORM requires at least 2 children")
            
        # Extract components
        P = self.children[0]  # The function name
        E = self.children[-1]  # The function body
        
        # Create first lambda node
        current_lambda = NodeFactory.create("lambda", self.depth + 1, self)
        self.children.insert(1, current_lambda)
        
        # Process all variables (parameters)
        i = 2
        while i < len(self.children) and self.children[i] != E:
            V = self.children[i]
            self.children.pop(i)
            V.set_depth(current_lambda.depth + 1)
            V.set_parent(current_lambda)
            current_lambda.children.append(V)
            
            # Create nested lambda for multiple parameters
            if i < len(self.children) - 1:
                next_lambda = NodeFactory.create("lambda", current_lambda.depth + 1, current_lambda)
                current_lambda.children.append(next_lambda)
                current_lambda = next_lambda
        
        # Add the body to the innermost lambda
        current_lambda.children.append(E)
        E.set_parent(current_lambda)
        E.set_depth(current_lambda.depth + 1)
        
        # Remove the body from direct children
        if E in self.children:
            self.children.remove(E)
        
        # Change node type
        self.set_data("=")

    def _transform_lambda(self) -> None:
        """
        Standardize LAMBDA node with multiple parameters:
            LAMBDA        LAMBDA
             /   \   ->   /    \
            V++   E      V     .E
        """
        if len(self.children) <= 2:
            # Single parameter lambda already in standard form
            return
            
        # Extract components
        E = self.children[-1]  # Last child is body
        
        # Create first nested lambda
        current_lambda = NodeFactory.create("lambda", self.depth + 1, self)
        self.children.insert(1, current_lambda)
        
        # Process all variables except the first one
        i = 2
        while i < len(self.children) and self.children[i] != E:
            V = self.children[i]
            self.children.pop(i)
            V.set_depth(current_lambda.depth + 1)
            V.set_parent(current_lambda)
            current_lambda.children.append(V)
            
            # Create nested lambda for multiple parameters
            if i < len(self.children) - 1:
                next_lambda = NodeFactory.create("lambda", current_lambda.depth + 1, current_lambda)
                current_lambda.children.append(next_lambda)
                current_lambda = next_lambda
        
        # Add the body to the innermost lambda
        current_lambda.children.append(E)
        E.set_parent(current_lambda)
        E.set_depth(current_lambda.depth + 1)
        
        # Remove the body from direct children
        if E in self.children:
            self.children.remove(E)

    def _transform_within(self) -> None:
        """
        Standardize WITHIN node:
                  WITHIN                  EQUAL
                 /      \                /     \
               EQUAL   EQUAL    ->      X2     GAMMA
              /    \   /    \                  /    \
             X1    E1 X2    E2               LAMBDA  E1
                                             /    \
                                            X1    E2
        """
        if len(self.children) != 2 or self.children[0].get_data() != "=" or self.children[1].get_data() != "=":
            raise StandardizationError("WITHIN transformation requires exactly 2 EQUAL children")
            
        # Extract components
        X1 = self.children[0].children[0]
        E1 = self.children[0].children[1]
        X2 = self.children[1].children[0]
        E2 = self.children[1].children[1]
        
        # Create gamma and lambda nodes
        gamma = NodeFactory.create("gamma", self.depth + 1, self)
        lambda_node = NodeFactory.create("lambda", gamma.depth + 1, gamma)
        
        # Set up hierarchy
        X1.set_depth(lambda_node.depth + 1)
        X1.set_parent(lambda_node)
        lambda_node.children.append(X1)
        
        E2.set_depth(lambda_node.depth + 1)
        E2.set_parent(lambda_node)
        lambda_node.children.append(E2)
        
        gamma.children.append(lambda_node)
        
        E1.set_depth(gamma.depth + 1)
        E1.set_parent(gamma)
        gamma.children.append(E1)
        
        X2.set_depth(self.depth + 1)
        X2.set_parent(self)
        
        # Clear existing children and add new structure
        self.children.clear()
        self.children.append(X2)
        self.children.append(gamma)
        
        # Change node type
        self.set_data("=")

    def _transform_at(self) -> None:
        """
        Standardize AT node:
                AT              GAMMA
              / | \    ->       /    \
             E1 N E2          GAMMA   E2
                              /    \
                             N     E1
        """
        if len(self.children) != 3:
            raise StandardizationError("AT transformation requires exactly 3 children")
            
        # Extract components
        E1 = self.children[0]
        N = self.children[1]
        E2 = self.children[2]
        
        # Create inner gamma node
        gamma_inner = NodeFactory.create("gamma", self.depth + 1, self)
        
        # Set up inner gamma
        N.set_depth(gamma_inner.depth + 1)
        N.set_parent(gamma_inner)
        gamma_inner.children.append(N)
        
        E1.set_depth(gamma_inner.depth + 1)
        E1.set_parent(gamma_inner)
        gamma_inner.children.append(E1)
        
        # Clear and rebuild children
        self.children.clear()
        self.children.append(gamma_inner)
        
        E2.set_depth(self.depth + 1)
        E2.set_parent(self)
        self.children.append(E2)
        
        # Change node type
        self.set_data("gamma")

    def _transform_and(self) -> None:
        """
        Standardize AND node:
                SIMULTDEF            EQUAL
                    |               /     \
                  EQUAL++  ->     COMMA   TAU
                  /   \             |      |
                 X     E           X++    E++
        """
        if not self.children or any(child.get_data() != "=" for child in self.children):
            raise StandardizationError("AND transformation requires EQUAL children")
            
        # Create comma and tau nodes
        comma = NodeFactory.create(",", self.depth + 1, self)
        tau = NodeFactory.create("tau", self.depth + 1, self)
        
        # Distribute children from equal nodes to comma and tau
        for equal in self.children:
            if len(equal.children) != 2:
                raise StandardizationError("Each EQUAL in AND must have exactly 2 children")
                
            X = equal.children[0]
            E = equal.children[1]
            
            X.set_parent(comma)
            X.set_depth(comma.depth + 1)
            comma.children.append(X)
            
            E.set_parent(tau)
            E.set_depth(tau.depth + 1)
            tau.children.append(E)
        
        # Clear existing children and add new structure
        self.children.clear()
        self.children.append(comma)
        self.children.append(tau)
        
        # Change node type
        self.set_data("=")

    def _transform_rec(self) -> None:
        """
        Standardize REC node:
               REC                 EQUAL
                |                 /     \
              EQUAL     ->       X     GAMMA
             /     \                   /    \
            X       E                YSTAR  LAMBDA
                                           /     \
                                          X      E
        """
        if len(self.children) != 1 or self.children[0].get_data() != "=":
            raise StandardizationError("REC transformation requires exactly 1 EQUAL child")
            
        # Extract components
        equal = self.children[0]
        if len(equal.children) != 2:
            raise StandardizationError("EQUAL in REC must have exactly 2 children")
            
        X = equal.children[0]
        E = equal.children[1]
        
        # Create nodes for the transformation
        F = NodeFactory.create(X.get_data(), self.depth + 1, self)
        G = NodeFactory.create("gamma", self.depth + 1, self)
        Y = NodeFactory.create("<Y*>", G.depth + 1, G)
        L = NodeFactory.create("lambda", G.depth + 1, G)
        
        # Set up lambda node
        X_copy = NodeFactory.create(X.get_data(), L.depth + 1, L)
        L.children.append(X_copy)
        
        E.set_depth(L.depth + 1)
        E.set_parent(L)
        L.children.append(E)
        
        # Set up gamma node
        G.children.append(Y)
        G.children.append(L)
        
        # Clear existing children and add new structure
        self.children.clear()
        self.children.append(F)
        self.children.append(G)
        
        # Change node type
        self.set_data("=")


class NodeFactory:
    """Factory class for creating different types of nodes."""
    
    @staticmethod
    def create(data: str, depth: int = 0, parent=None) -> Node:
        """Create a new node with the given data, depth, and parent."""
        node = Node(data, depth, parent)
        return node


class StandardizationError(Exception):
    """Exception raised for errors during standardization process."""
    pass