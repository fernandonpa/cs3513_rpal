from .nodes import (
    Symbol, E, Id, Lambda, Gamma, Delta, Eta, Ystar, Tup, Tau, 
    Beta, B, Rator, Uop, Bop, Int, Bool, Str, Dummy
)
from .operations import apply_unary_operation, apply_binary_operation
from .error_handler import handle_error, CSEError
from .utils import format_tuple, debug_print_control, debug_print_stack, debug_print_environment

class CSEMachine:
    """Control Structure Evaluator (CSE) Machine implementation"""
    
    def __init__(self, control, stack, environment):
        self.control = control    # Control stack
        self.stack = stack        # Value stack
        self.environment = environment  # Environment stack
        self.env_counter = len(environment)  # For creating new environments
        self.debug_mode = False
        self.debug_files = {
            'control': None,
            'stack': None,
            'environment': None
        }
    
    def enable_debug(self, control_file=None, stack_file=None, env_file=None):
        """Enable debug mode with optional file outputs"""
        self.debug_mode = True
        self.debug_files['control'] = control_file
        self.debug_files['stack'] = stack_file
        self.debug_files['environment'] = env_file
        
        # Clear debug files if provided
        for file_path in self.debug_files.values():
            if file_path:
                open(file_path, 'w').close()
    
    def _debug_output(self):
        """Output debug information if debug mode is enabled"""
        if not self.debug_mode:
            return
            
        control_info = debug_print_control(self.control)
        stack_info = debug_print_stack(self.stack)
        env_info = debug_print_environment(self.environment)
        
        print(control_info)
        print(stack_info)
        print(env_info)
        print('-' * 50)
        
        # Write to files if provided
        if self.debug_files['control']:
            with open(self.debug_files['control'], 'a') as f:
                f.write(f"{control_info}\n")
        
        if self.debug_files['stack']:
            with open(self.debug_files['stack'], 'a') as f:
                f.write(f"{stack_info}\n")
        
        if self.debug_files['environment']:
            with open(self.debug_files['environment'], 'a') as f:
                f.write(f"{env_info}\n\n")
    
    def execute(self):
        """Execute the CSE machine until completion"""
        current_env = self.environment[0]
        
        while self.control:
            self._debug_output()
            
            current_symbol = self.control.pop()
            
            try:
                self._process_symbol(current_symbol, current_env)
                
                # Update current environment if needed
                if len(self.environment) > 0:
                    # Find the first non-removed environment
                    for env in self.environment:
                        if not env.is_marked_removed():
                            current_env = env
                            break
            
            except Exception as e:
                handle_error(e)
                # Continue execution to try to recover
    
    def _process_symbol(self, symbol, current_env):
        """Process a single symbol from the control stack"""
        
        # Handle different symbol types
        if isinstance(symbol, Id):
            # Look up identifier in current environment
            value = current_env.lookup(symbol)
            self.stack.insert(0, value)
            
        elif isinstance(symbol, Lambda):
            # Lambda captures its creation environment
            symbol.set_environment_index(current_env.get_index())
            self.stack.insert(0, symbol)
            
        elif isinstance(symbol, Gamma):
            self._process_gamma()
            
        elif isinstance(symbol, E):
            # Environment marker - we're exiting an environment
            self.stack.pop(1)  # Remove environment entry below current result
            self.environment[symbol.get_index()].mark_removed()
            
        elif isinstance(symbol, Rator):
            self._process_operator(symbol)
            
        elif isinstance(symbol, Beta):
            self._process_beta()
            
        elif isinstance(symbol, Tau):
            self._process_tau(symbol)
            
        elif isinstance(symbol, Delta):
            # Add delta's symbols to control stack
            self.control.extend(symbol.symbols)
            
        elif isinstance(symbol, B):
            # Add B's symbols to control stack
            self.control.extend(symbol.symbols)
            
        else:
            # Other symbols (values) are pushed onto the stack
            self.stack.insert(0, symbol)
    
    def _process_gamma(self):
        """Process a gamma (function application) symbol"""
        func = self.stack.pop(0)
        
        if isinstance(func, Lambda):
            # Function application
            self._apply_lambda(func)
            
        elif isinstance(func, Tup):
            # Tuple indexing
            self._tuple_index(func)
            
        elif isinstance(func, Ystar):
            # Y* fixed-point operator (for recursion)
            self._process_ystar()
            
        elif isinstance(func, Eta):
            # Eta (recursive function) processing
            self._process_eta(func)
            
        else:
            # Built-in function handling
            self._process_builtin(func)
    
    def _apply_lambda(self, lambda_func):
        """Apply a lambda function to arguments on the stack"""
        # Create new environment
        new_env = E(self.env_counter)
        self.env_counter += 1
        
        # Bind parameters to arguments
        if len(lambda_func.identifiers) == 1:
            # Single parameter
            arg = self.stack.pop(0)
            new_env.bind(lambda_func.identifiers[0], arg)
        else:
            # Multiple parameters as a tuple
            tup = self.stack.pop(0)
            if not isinstance(tup, Tup) or len(tup.get_elements()) != len(lambda_func.identifiers):
                # Handle error: argument count mismatch
                print(f"Error: Expected {len(lambda_func.identifiers)} arguments but got {len(tup.get_elements()) if isinstance(tup, Tup) else 1}")
                self.stack.insert(0, Symbol("error"))
                return
                
            for i, param_id in enumerate(lambda_func.identifiers):
                new_env.bind(param_id, tup.get_elements()[i])
        
        # Link to parent environment
        for env in self.environment:
            if env.get_index() == lambda_func.get_environment_index():
                new_env.set_parent(env)
                break
        
        # Update control and environment stacks
        self.control.append(new_env)  # E marker for when this environment exits
        self.control.append(lambda_func.get_body())  # Lambda body to execute
        
        self.stack.insert(0, new_env)  # Put env on stack to track results
        self.environment.append(new_env)
    
    def _tuple_index(self, tup):
        """Process tuple indexing operation"""
        index = self.stack.pop(0)
        if not isinstance(index, Int):
            self.stack.insert(0, Symbol("error"))
            print("Error: Tuple index must be an integer")
            return
            
        index_val = int(index.get_data())
        
        if index_val < 1 or index_val > len(tup.get_elements()):
            self.stack.insert(0, Symbol("error"))
            print(f"Error: Tuple index {index_val} out of bounds (1-{len(tup.get_elements())})")
            return
            
        # Tuple indices in RPAL start at 1
        self.stack.insert(0, tup.get_elements()[index_val - 1])
    
    def _process_ystar(self):
        """Process Y* (fixed-point combinator) operation"""
        lambda_func = self.stack.pop(0)
        if not isinstance(lambda_func, Lambda):
            self.stack.insert(0, Symbol("error"))
            print("Error: Y* requires a lambda function")
            return
            
        # Create an eta closure for recursion
        eta = Eta()
        eta.set_index(lambda_func.get_index())
        eta.set_environment_index(lambda_func.get_environment_index())
        eta.set_identifier(lambda_func.identifiers[0]) if lambda_func.identifiers else None
        eta.set_lambda(lambda_func)
        
        self.stack.insert(0, eta)
    
    def _process_eta(self, eta):
        """Process an eta closure (for recursion)"""
        lambda_func = eta.get_lambda()
        
        # Set up recursive application
        self.control.append(Gamma())
        self.control.append(Gamma())
        self.stack.insert(0, eta)
        self.stack.insert(0, lambda_func)
    
    def _process_operator(self, operator):
        """Process an operator (unary or binary)"""
        if isinstance(operator, Uop):
            # Unary operator
            operand = self.stack.pop(0)
            result = apply_unary_operation(operator, operand)
            self.stack.insert(0, result)
        elif isinstance(operator, Bop):
            # Binary operator
            right = self.stack.pop(0)
            left = self.stack.pop(0)
            result = apply_binary_operation(operator, left, right)
            self.stack.insert(0, result)
    
    def _process_beta(self):
        """Process a beta (conditional) operation"""
        condition = self.stack.pop(0)
        
        # Check if condition is true
        is_true = False
        if isinstance(condition, Bool):
            is_true = condition.get_data() == "true"
        
        # Keep then-branch or else-branch based on condition
        if is_true:
            self.control.pop()  # Remove else-branch
        else:
            self.control.pop(-2)  # Remove then-branch
    
    def _process_tau(self, tau):
        """Process a tau (tuple construction) operation"""
        # Create a tuple with n elements from the stack
        tup = Tup()
        for _ in range(tau.get_size()):
            tup.add_element(self.stack.pop(0))
        self.stack.insert(0, tup)
    
    def _process_builtin(self, func):
        """Process built-in functions"""
        func_name = func.get_data()
        
        if func_name == "Print":
            # Simply return the value (result will be printed after execution)
            pass
            
        elif func_name == "Stem":
            # Get first character of a string
            s = self.stack.pop(0)
            if not isinstance(s, Str):
                self.stack.insert(0, Symbol("error"))
                print("Error: Stem requires a string")
                return
                
            if len(s.get_data()) > 0:
                s.set_data(s.get_data()[0])
            else:
                s.set_data("")
            self.stack.insert(0, s)
            
        elif func_name == "Stern":
            # Get all but first character of a string
            s = self.stack.pop(0)
            if not isinstance(s, Str):
                self.stack.insert(0, Symbol("error"))
                print("Error: Stern requires a string")
                return
                
            if len(s.get_data()) > 1:
                s.set_data(s.get_data()[1:])
            else:
                s.set_data("")
            self.stack.insert(0, s)
            
        elif func_name == "Conc":
            # Concatenate two strings
            s2 = self.stack.pop(0)
            s1 = self.stack.pop(0)
            if not isinstance(s1, Str) or not isinstance(s2, Str):
                self.stack.insert(0, Symbol("error"))
                print("Error: Conc requires two strings")
                return
                
            s1.set_data(s1.get_data() + s2.get_data())
            self.stack.insert(0, s1)
            
        elif func_name == "Order":
            # Get tuple size
            tup = self.stack.pop(0)
            if not isinstance(tup, Tup):
                self.stack.insert(0, Int(1))  # Non-tuples have order 1
                return
                
            self.stack.insert(0, Int(len(tup.get_elements())))
            
        elif func_name == "Isinteger":
            # Check if value is an integer
            val = self.stack.pop(0)
            self.stack.insert(0, Bool(isinstance(val, Int)))
            
        elif func_name == "Isstring":
            # Check if value is a string
            val = self.stack.pop(0)
            self.stack.insert(0, Bool(isinstance(val, Str)))
            
        elif func_name == "Istuple":
            # Check if value is a tuple
            val = self.stack.pop(0)
            self.stack.insert(0, Bool(isinstance(val, Tup)))
            
        elif func_name == "Isdummy":
            # Check if value is dummy
            val = self.stack.pop(0)
            self.stack.insert(0, Bool(isinstance(val, Dummy)))
            
        elif func_name == "Istruthvalue":
            # Check if value is a boolean
            val = self.stack.pop(0)
            self.stack.insert(0, Bool(isinstance(val, Bool)))
            
        elif func_name == "Isfunction":
            # Check if value is a function
            val = self.stack.pop(0)
            self.stack.insert(0, Bool(isinstance(val, Lambda)))
            
        else:
            # Unknown built-in function
            self.stack.insert(0, Symbol("error"))
            print(f"Error: Unknown built-in function: {func_name}")
    
    def get_result(self):
        """Get the final result after execution"""
        if not self.stack:
            return Symbol("error")
            
        result = self.stack[0]
        
        # Format tuples for display
        if isinstance(result, Tup):
            return format_tuple(result)
            
        return result.get_data()