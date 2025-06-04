
from .nodes.symbol import Symbol
from .nodes.rand import Rand
from .nodes.rator import Rator
from .nodes.b import B
from .nodes.beta import Beta
from .nodes.bool import Bool
from .nodes.delta import Delta
from .nodes.dummy import Dummy
from .nodes.e import E
from .nodes.bop import Bop
from .nodes.err import Err
from .nodes.eta import Eta
from .nodes.gamma import Gamma
from .nodes.id import Id
from .nodes.int import Int
from .nodes.lmbda import Lambda
from .nodes.tau import Tau
from .nodes.tup import Tup
from .nodes.uop import Uop
from .nodes.ystar import Ystar
from .nodes.str import Str


class CSEMachine:
    """CSE (Control-Stack-Environment) Machine for executing RPAL programs.
    
    This class implements the abstract machine that evaluates standardized RPAL programs.
    The CSE machine processes a control structure representing the program, maintains
    a stack for intermediate results, and manages environments for variable bindings.
    
    Attributes:
        control (list): The control structure representing the program to execute
        stack (list): Stack for storing intermediate computation results
        environment (list): List of environments for variable lookups
    """
    
    def __init__(self, control, stack, environment):
        """Initialize a new CSE Machine.
        
        Args:
            control (list): Initial control structure (standardized program)
            stack (list): Initial stack (typically empty)
            environment (list): Initial environment (typically contains base env)
        """
        self.control = control
        self.stack = stack
        self.environment = environment
    
    def execute(self):
        """Execute the RPAL program represented by the control structure.
        
        This method implements the core execution loop of the CSE machine,
        processing each node in the control structure according to the
        semantics of the RPAL language.
        """
        current_environment = self.environment[0]  # Start with base environment
        j = 1  # Environment index counter for new environments
        
        while self.control:
            
            current_symbol = self.control.pop()  # Get next node to process
            
            if isinstance(current_symbol, Id):
                # Handle identifier lookup - find the value in the environment
                self.stack.insert(0, current_environment.lookup(current_symbol))
                
            elif isinstance(current_symbol, Lambda):
                # Handle lambda expression - create function closure
                current_symbol.set_environment(current_environment.get_index())
                self.stack.insert(0, current_symbol)
                
            elif isinstance(current_symbol, Gamma):
                # Handle function application
                next_symbol = self.stack.pop(0)  # Get the function to apply
                
                if isinstance(next_symbol, Lambda):
                    # Apply lambda expression to arguments
                    lambda_expr = next_symbol
                    e = E(j)  # Create new environment
                    j += 1
                    
                    if len(lambda_expr.identifiers) == 1:
                        # Single parameter function
                        temp = self.stack.pop(0)
                        e.values[lambda_expr.identifiers[0]] = temp
                    else:
                        # Multiple parameters function (tuple pattern)
                        tup = self.stack.pop(0)
                        for i, id in enumerate(lambda_expr.identifiers):
                            e.values[id] = tup.symbols[i]
                            
                    # Set up environment chain and handle execution
                    for env in self.environment:
                        if env.get_index() == lambda_expr.get_environment():
                            e.set_parent(env)
                    current_environment = e
                    self.control.append(e)
                    self.control.append(lambda_expr.get_delta())
                    self.stack.insert(0, e)
                    self.environment.append(e)
                    
                elif isinstance(next_symbol, Tup):
                    # Handle tuple element access (e.g., T[n])
                    tup = next_symbol
                    i = int(self.stack.pop(0).get_data())
                    self.stack.insert(0, tup.symbols[i - 1])  # 1-indexed
                    
                elif isinstance(next_symbol, Ystar):
                    # Handle Y* fixed-point combinator for recursion
                    lambda_expr = self.stack.pop(0)
                    eta = Eta()
                    eta.set_index(lambda_expr.get_index())
                    eta.set_environment(lambda_expr.get_environment())
                    eta.set_identifier(lambda_expr.identifiers[0])
                    eta.set_lambda(lambda_expr)
                    self.stack.insert(0, eta)
                    
                elif isinstance(next_symbol, Eta):
                    # Handle recursive function call via Eta
                    eta = next_symbol
                    lambda_expr = eta.get_lambda()
                    self.control.append(Gamma())
                    self.control.append(Gamma())
                    self.stack.insert(0, eta)
                    self.stack.insert(0, lambda_expr)
                    
                else:
                    # Handle built-in functions
                    if next_symbol.get_data() == "Print":
                        # Print is handled by get_answer()
                        pass
                        
                    elif next_symbol.get_data() == "Stem":
                        # Get first character of string
                        s = self.stack.pop(0)
                        s.set_data(s.get_data()[0])
                        self.stack.insert(0, s)
                        
                    elif next_symbol.get_data() == "Stern":
                        # Get all but first character of string
                        s = self.stack.pop(0)
                        s.set_data(s.get_data()[1:])
                        self.stack.insert(0, s)
                        
                    elif next_symbol.get_data() == "Conc":
                        # Concatenate two strings
                        s1 = self.stack.pop(0)
                        s2 = self.stack.pop(0)
                        s1.set_data(s1.get_data() + s2.get_data())
                        self.stack.insert(0, s1)
                        
                    elif next_symbol.get_data() == "Order":
                        # Get tuple size
                        tup = self.stack.pop(0)
                        n = Int(str(len(tup.symbols)))
                        self.stack.insert(0, n)
                        
                    elif next_symbol.get_data() == "Isinteger":
                        # Check if value is an integer
                        if isinstance(self.stack[0], Int):
                            self.stack.insert(0, Bool("true"))
                        else:
                            self.stack.insert(0, Bool("false"))
                        self.stack.pop(1)
                        
                    elif next_symbol.get_data() == "Null":
                        # Check for null/empty value
                        pass
                        
                    elif next_symbol.get_data() == "Itos":
                        # Convert integer to string
                        pass
                        
                    elif next_symbol.get_data() == "Isstring":
                        # Check if value is a string
                        if isinstance(self.stack[0], Str):
                            self.stack.insert(0, Bool("true"))
                        else:
                            self.stack.insert(0, Bool("false"))
                        self.stack.pop(1)
                        
                    elif next_symbol.get_data() == "Istuple":
                        # Check if value is a tuple
                        if isinstance(self.stack[0], Tup):
                            self.stack.insert(0, Bool("true"))
                        else:
                            self.stack.insert(0, Bool("false"))
                        self.stack.pop(1)
                        
                    elif next_symbol.get_data() == "Isdummy":
                        # Check if value is dummy
                        if isinstance(self.stack[0], Dummy):
                            self.stack.insert(0, Bool("true"))
                        else:
                            self.stack.insert(0, Bool("false"))
                        self.stack.pop(1)
                        
                    elif next_symbol.get_data() == "Istruthvalue":
                        # Check if value is boolean
                        if isinstance(self.stack[0], Bool):
                            self.stack.insert(0, Bool("true"))
                        else:
                            self.stack.insert(0, Bool("false"))
                        self.stack.pop(1)
                        
                    elif next_symbol.get_data() == "Isfunction":
                        # Check if value is a function
                        if isinstance(self.stack[0], Lambda):
                            self.stack.insert(0, Bool("true"))
                        else:
                            self.stack.insert(0, Bool("false"))
                        self.stack.pop(1)
                        
            elif isinstance(current_symbol, E):
                # Handle environment termination
                self.stack.pop(1)  # Remove environment reference
                self.environment[current_symbol.get_index()].set_is_removed(True)
                
                # Find the nearest non-removed environment
                y = len(self.environment)
                while y > 0:
                    if not self.environment[y - 1].get_is_removed():
                        current_environment = self.environment[y - 1]
                        break
                    else:
                        y -= 1
                        
            elif isinstance(current_symbol, Rator):
                if isinstance(current_symbol, Uop):
                    # Handle unary operations (neg, not)
                    rator = current_symbol
                    rand = self.stack.pop(0)
                    self.stack.insert(0, self.apply_unary_operation(rator, rand))
                    
                if isinstance(current_symbol, Bop):
                    # Handle binary operations (+, -, *, /, etc.)
                    rator = current_symbol
                    rand1 = self.stack.pop(0)
                    rand2 = self.stack.pop(0)
                    self.stack.insert(0, self.apply_binary_operation(rator, rand1, rand2))
                    
            elif isinstance(current_symbol, Beta):
                # Handle conditional (if-then-else) processing
                # Determine which branch to take based on top of stack
                if (self.stack[0].get_data() == "true"):
                    self.control.pop()  # Skip the 'else' branch
                else:
                    self.control.pop(-2)  # Skip the 'then' branch
                self.stack.pop(0)  # Remove the condition value
                
            elif isinstance(current_symbol, Tau):
                # Handle tuple creation
                tau = current_symbol
                tup = Tup()
                for _ in range(tau.get_n()):
                    tup.symbols.append(self.stack.pop(0))
                self.stack.insert(0, tup)
                
            elif isinstance(current_symbol, Delta):
                # Handle delta nodes (code blocks)
                self.control.extend(current_symbol.symbols)
                
            elif isinstance(current_symbol, B):
                # Handle base environment nodes
                self.control.extend(current_symbol.symbols)
                
            else:
                # Handle all other symbols (literals, etc.)
                self.stack.insert(0, current_symbol)
    
    def write_stack_to_file(self, file_path):
        """Write the current stack contents to a file for debugging.
        
        Args:
            file_path (str): Path to the output file
        """
        with open(file_path, 'a') as file:
            for symbol in self.stack:
                file.write(symbol.get_data())
                if isinstance(symbol, (Lambda, Delta, E, Eta)):
                    file.write(str(symbol.get_index()))
                file.write(",")
            file.write("\n")

    def write_control_to_file(self, file_path):
        """Write the current control structure to a file for debugging.
        
        Args:
            file_path (str): Path to the output file
        """
        with open(file_path, 'a') as file:
            for symbol in self.control:
                file.write(symbol.get_data())
                if isinstance(symbol, (Lambda, Delta, E, Eta)):
                    file.write(str(symbol.get_index()))
                file.write(",")
            file.write("\n")
    
    @staticmethod
    def clear_file(file_path):
        """Clear the contents of a file.
        
        Args:
            file_path (str): Path to the file to clear
        """
        open(file_path, 'w').close()
    
    def print_environment(self):
        """Print the environment hierarchy for debugging.
        
        Displays each environment and its parent environment if it exists.
        """
        for symbol in self.environment:
            print(f"e{symbol.get_index()} --> ", end="")
            if symbol.get_index() != 0:
                print(f"e{symbol.get_parent().get_index()}")
            else:
                print()
                
    def covert_string_to_bool(self, data):
        """Convert a string boolean representation to a Python boolean.
        
        Args:
            data (str): String representation ("true" or "false")
            
        Returns:
            bool: Python boolean value (True or False)
        """
        if data == "true":
            return True
        elif data == "false":
            return False

    def apply_unary_operation(self, rator, rand):
        """Apply a unary operation to an operand.
        
        Args:
            rator (Uop): Unary operator node
            rand (Rand): Operand node
            
        Returns:
            Symbol: Result of the operation
        """
        if rator.get_data() == "neg":
            # Numeric negation
            val = int(rand.get_data())
            return Int(str(-1 * val))
            
        elif rator.get_data() == "not":
            # Logical negation
            val = self.covert_string_to_bool(rand.get_data())
            return Bool(str(not val).lower())
            
        else:
            # Unknown operation
            return Err()

    def apply_binary_operation(self, rator, rand1, rand2):
        """Apply a binary operation to two operands.
        
        Args:
            rator (Bop): Binary operator node
            rand1 (Rand): First operand node
            rand2 (Rand): Second operand node
            
        Returns:
            Symbol: Result of the operation
        """
        if rator.get_data() == "+":
            # Addition
            val1 = int(rand1.get_data())
            val2 = int(rand2.get_data())
            return Int(str(val1 + val2))
            
        elif rator.data == "-":
            # Subtraction
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Int(str(val1 - val2))
            
        elif rator.data == "*":
            # Multiplication
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Int(str(val1 * val2))
            
        elif rator.data == "/":
            # Division
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Int(str(int(val1 / val2)))
            
        elif rator.data == "**":
            # Exponentiation
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Int(str(val1 ** val2))
            
        elif rator.data == "&":
            # Logical AND
            val1 = self.covert_string_to_bool(rand1.data)
            val2 = self.covert_string_to_bool(rand2.data)
            return Bool(str(val1 and val2).lower())
            
        elif rator.data == "or":
            # Logical OR
            val1 = self.covert_string_to_bool(rand1.data)
            val2 = self.covert_string_to_bool(rand2.data)
            return Bool(str(val1 or val2).lower())
            
        elif rator.data == "eq":
            # Equality
            val1 = rand1.data
            val2 = rand2.data
            return Bool(str(val1 == val2).lower())
            
        elif rator.data == "ne":
            # Inequality
            val1 = rand1.data
            val2 = rand2.data
            return Bool(str(val1 != val2).lower())
            
        elif rator.data == "ls":
            # Less than
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Bool(str(val1 < val2).lower())
            
        elif rator.data == "le":
            # Less than or equal
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Bool((val1 <= val2))
            
        elif rator.data == "gr":
            # Greater than
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Bool(str(val1 > val2).lower())
            
        elif rator.data == "ge":
            # Greater than or equal
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Bool(str(val1 >= val2).lower())
            
        elif rator.data == "aug":
            # Tuple augmentation
            if isinstance(rand2, Tup):
                rand1.symbols.extend(rand2.symbols)
            else:
                rand1.symbols.append(rand2)
            return rand1
            
        else:
            # Unknown operation
            return Err()

    def get_tuple_value(self, tup):
        """Convert a tuple value to its string representation.
        
        Args:
            tup (Tup): Tuple to convert
            
        Returns:
            str: String representation of the tuple
        """
        temp = "("
        for symbol in tup.symbols:
            if isinstance(symbol, Tup):
                temp += self.get_tuple_value(symbol) + ", "
            else:
                temp += symbol.get_data() + ", "
        temp = temp[:-2] + ")"  # Remove last comma and space, add closing parenthesis
        return temp

    def get_answer(self):
        """Execute the program and return the final result.
        
        Returns:
            str: String representation of the program's result
        """
        self.execute()  # Run the program
        
        # Format the result
        if isinstance(self.stack[0], Tup):
            return self.get_tuple_value(self.stack[0])
        return self.stack[0].get_data()