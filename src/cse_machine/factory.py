from .nodes import (
    Symbol, Uop, Bop, Gamma, Tau, Ystar, Id, Int, Str, Tup, 
    Bool, Dummy, Err, E, Lambda, Delta, Beta, B
)

class CSEMachineFactory:
    """Factory for creating CSE Machine instances from AST nodes"""
    
    def __init__(self):
        self.env_counter = 0
        self.lambda_counter = 1  # Starting from 1 as per original code
        self.delta_counter = 0
        self.global_env = E(self.env_counter)
    
    def create_machine_from_ast(self, ast):
        """Create a complete CSE machine from an Abstract Syntax Tree"""
        from .machine import CSEMachine
        
        control = self._build_control(ast)
        stack = [self.global_env]  # Start with the global environment
        environment = [self.global_env]
        
        return CSEMachine(control, stack, environment)
    
    def _build_control(self, ast):
        """Build the initial control stack from the AST"""
        control = [self.global_env]
        root_delta = self._build_delta(ast.get_root())
        control.append(root_delta)
        return control
    
    def _build_delta(self, node):
        """Build a delta node from an AST node"""
        delta = Delta(self.delta_counter)
        self.delta_counter += 1
        delta.symbols = self._process_node(node)
        return delta
    
    def _process_node(self, node):
        """Process an AST node and return a list of symbols"""
        symbols = []
        
        if node.get_data() == "lambda":
            # Handle lambda expression
            lambda_expr = self._build_lambda(node)
            symbols.append(lambda_expr)
        
        elif node.get_data() == "->":
            # Handle conditional expression
            delta_then = self._build_delta(node.get_children()[1])
            delta_else = self._build_delta(node.get_children()[2])
            beta = Beta()
            b = B()
            b.symbols = self._process_node(node.get_children()[0])
            
            symbols.append(delta_then)
            symbols.append(delta_else)
            symbols.append(beta)
            symbols.append(b)
        
        else:
            # Handle other node types
            node_symbol = self._create_symbol_from_node(node)
            symbols.append(node_symbol)
            
            # Process children recursively
            for child in node.get_children():
                symbols.extend(self._process_node(child))
        
        return symbols
    
    def _build_lambda(self, node):
        """Build a lambda node from an AST node"""
        lambda_expr = Lambda(self.lambda_counter)
        self.lambda_counter += 1
        
        # Get the parameter identifiers
        param_node = node.get_children()[0]
        if param_node.get_data() == ",":
            # Multiple parameters
            for param in param_node.get_children():
                param_id = param.get_data()
                if param_id.startswith("<IDENTIFIER:"):
                    id_name = param_id[12:-1]  # Extract identifier name
                    lambda_expr.identifiers.append(Id(id_name))
        else:
            # Single parameter
            param_id = param_node.get_data()
            if param_id.startswith("<IDENTIFIER:"):
                id_name = param_id[12:-1]  # Extract identifier name
                lambda_expr.identifiers.append(Id(id_name))
        
        # Set the body
        lambda_expr.set_body(self._build_delta(node.get_children()[1]))
        
        return lambda_expr
    
    def _create_symbol_from_node(self, node):
        """Create a symbol from an AST node's data"""
        data = node.get_data()
        
        # Operators
        if data in ("not", "neg"):
            return Uop(data)
        
        elif data in ("+", "-", "*", "/", "**", "&", "or", "eq", "ne", "ls", "le", "gr", "ge", "aug"):
            return Bop(data)
        
        elif data == "gamma":
            return Gamma()
        
        elif data == "tau":
            return Tau(len(node.get_children()))
        
        elif data == "<Y*>":
            return Ystar()
        
        # Values and identifiers
        elif data.startswith("<IDENTIFIER:"):
            return Id(data[12:-1])  # Extract identifier name
        
        elif data.startswith("<INTEGER:"):
            return Int(data[9:-1])  # Extract integer value
        
        elif data.startswith("<STRING:"):
            return Str(data[9:-2])  # Extract string value
        
        elif data.startswith("<NIL"):
            return Tup()  # Empty tuple
        
        elif data.startswith("<TRUE_VALUE:t"):
            return Bool(True)
        
        elif data.startswith("<TRUE_VALUE:f"):
            return Bool(False)
        
        elif data.startswith("<dummy>"):
            return Dummy()
        
        else:
            print(f"Warning: Unrecognized node type: {data}")
            return Symbol(data)  # Fallback