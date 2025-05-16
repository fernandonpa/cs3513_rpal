from .nodes import *
from .machine import CSEMachine

class CSEFactory:
    """Factory class for creating CSE machine components."""
    
    def __init__(self):
        """Initialize the CSE factory."""
        # Create the initial environment
        self.initial_env = Environment(0)
        # Counters for unique indices
        self.lambda_counter = 1
        self.delta_counter = 0
    
    def create_symbol(self, node):
        """Create a symbol from a node in the standardized tree.
        
        Args:
            node: A node from the standardized tree
            
        Returns:
            The corresponding symbol for the CSE machine
        """
        data = node.get_data()
        
        # Handle unary operators
        if data in ("not", "neg"):
            return UnaryOperator(data)
            
        # Handle binary operators
        elif data in ("+", "-", "*", "/", "**", "&", "or", "eq", "ne", "ls", "le", "gr", "ge", "aug"):
            return BinaryOperator(data)
            
        # Handle special symbols
        elif data == "gamma":
            return Gamma()
        elif data == "tau":
            return Tau(len(node.get_children()))
        elif data == "<Y*>":
            return Ystar()
            
        # Handle literals and identifiers
        else:
            if data.startswith("<IDENTIFIER:"):
                return Identifier(data[12:-1])
            elif data.startswith("<INTEGER:"):
                return IntegerValue(data[9:-1])
            elif data.startswith("<STRING:"):
                return StringValue(data[9:-2])
            elif data.startswith("<NIL"):
                return Tuple()
            elif data.startswith("<TRUE_VALUE:t"):
                return BoolValue("true")
            elif data.startswith("<TRUE_VALUE:f"):
                return BoolValue("false")
            elif data.startswith("<dummy>"):
                return DummyValue()
            else:
                # For unrecognized nodes, log the error and return ErrorSymbol
                print(f"Error: Unrecognized node: {data}")
                return ErrorSymbol(f"Unrecognized: {data}")
    
    def create_control_structure(self, node):
        """Create a control structure (B) from a node.
        
        Args:
            node: A node representing a condition
            
        Returns:
            A ControlStructure object with instructions
        """
        control = ControlStructure()
        control.instructions = self.traverse_tree_preorder(node)
        return control
    
    def create_lambda(self, node):
        """Create a lambda from a node.
        
        Args:
            node: A lambda node from the standardized tree
            
        Returns:
            A Lambda object
        """
        lambda_obj = Lambda(self.lambda_counter)
        self.lambda_counter += 1
        
        # Set the body (delta)
        lambda_obj.set_body(self.create_delta(node.get_children()[1]))
        
        # Handle parameters (can be a single identifier or a comma-separated list)
        param_node = node.get_children()[0]
        
        if param_node.get_data() == ",":
            # Multiple parameters
            for identifier in param_node.get_children():
                lambda_obj.parameters.append(Identifier(identifier.get_data()[12:-1]))
        else:
            # Single parameter
            lambda_obj.parameters.append(Identifier(param_node.get_data()[12:-1]))
            
        return lambda_obj
    
    def traverse_tree_preorder(self, node):
        """Traverse a tree in pre-order and convert nodes to symbols.
        
        Args:
            node: The root node to traverse
            
        Returns:
            A list of symbols in pre-order traversal order
        """
        symbols = []
        
        # Handle lambda nodes specially
        if node.get_data() == "lambda":
            symbols.append(self.create_lambda(node))
        
        # Handle conditionals specially
        elif node.get_data() == "->":
            # Add the true and false branches as deltas
            symbols.append(self.create_delta(node.get_children()[1]))
            symbols.append(self.create_delta(node.get_children()[2]))
            # Add beta for conditional branching
            symbols.append(Beta())
            # Add control structure for the condition
            symbols.append(self.create_control_structure(node.get_children()[0]))
        
        # Handle all other nodes
        else:
            # Add the current node as a symbol
            symbols.append(self.create_symbol(node))
            
            # Recursively add all children
            for child in node.get_children():
                symbols.extend(self.traverse_tree_preorder(child))
                
        return symbols
    
    def create_delta(self, node):
        """Create a delta (instruction sequence) from a node.
        
        Args:
            node: A node from the standardized tree
            
        Returns:
            A Delta object containing instructions
        """
        delta = Delta(self.delta_counter)
        self.delta_counter += 1
        
        # Set the instructions by traversing the subtree
        delta.instructions = self.traverse_tree_preorder(node)
        
        return delta
    
    def create_control_stack(self, ast):
        """Create the initial control stack for the CSE machine.
        
        Args:
            ast: The abstract syntax tree (standardized)
            
        Returns:
            A list containing the initial environment and delta
        """
        return [self.initial_env, self.create_delta(ast.get_root())]
    
    def create_value_stack(self):
        """Create the initial value stack for the CSE machine.
        
        Returns:
            A list containing the initial environment
        """
        return [self.initial_env]
    
    def create_environment_stack(self):
        """Create the initial environment stack for the CSE machine.
        
        Returns:
            A list containing the initial environment
        """
        return [self.initial_env]
    
    def create_cse_machine(self, ast):
        """Create a complete CSE machine from a standardized tree.
        
        Args:
            ast: The abstract syntax tree (standardized)
            
        Returns:
            A CSEMachine initialized with control, value, and environment stacks
        """
        control_stack = self.create_control_stack(ast)
        value_stack = self.create_value_stack()
        env_stack = self.create_environment_stack()
        
        return CSEMachine(control_stack, value_stack, env_stack)