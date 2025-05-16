from .nodes import *
from .error_handler import CSEMachineError

class CSEMachine:
    """Implementation of the Control Structure Environment Machine for RPAL."""
    
    def __init__(self, control_stack, value_stack, env_stack):
        """Initialize the CSE machine with stacks.
        
        Args:
            control_stack: The initial control stack
            value_stack: The initial value stack
            env_stack: The initial environment stack
        """
        self.control_stack = control_stack
        self.value_stack = value_stack
        self.env_stack = env_stack
    
    def evaluate(self):
        """Evaluate the program by executing the CSE machine.
        
        Returns:
            None. The result is left on the value stack.
        """
        # Get the initial environment
        current_env = self.env_stack[0]
        # Counter for environment indices
        env_counter = 1
        
        # Continue until control stack is empty
        while self.control_stack:
            # Optional debugging:
            # self._write_control_stack_to_file("control_stack.txt")
            # self._write_value_stack_to_file("value_stack.txt")
            
            # Pop the next instruction from the control stack
            current_symbol = self.control_stack.pop()
            
            # Handle different types of symbols
            if isinstance(current_symbol, Identifier):
                # Look up identifier in current environment and push to value stack
                self.value_stack.insert(0, current_env.lookup(current_symbol))
                
            elif isinstance(current_symbol, Lambda):
                # Set lambda's environment and push to value stack
                current_symbol.set_environment(current_env.get_index())
                self.value_stack.insert(0, current_symbol)
                
            elif isinstance(current_symbol, Gamma):
                # Function application
                next_symbol = self.value_stack.pop(0)
                
                if isinstance(next_symbol, Lambda):
                    # Apply lambda to arguments
                    lambda_obj = next_symbol
                    
                    # Create new environment
                    new_env = Environment(env_counter)
                    env_counter += 1
                    
                    # Bind parameters to arguments
                    if len(lambda_obj.parameters) == 1:
                        # Single parameter
                        arg = self.value_stack.pop(0)
                        new_env.bindings[lambda_obj.parameters[0]] = arg
                    else:
                        # Multiple parameters (tuple)
                        tuple_arg = self.value_stack.pop(0)
                        for i, param in enumerate(lambda_obj.parameters):
                            new_env.bindings[param] = tuple_arg.elements[i]
                    
                    # Set parent environment
                    for env in self.env_stack:
                        if env.get_index() == lambda_obj.get_environment():
                            new_env.set_parent(env)
                            break
                    
                    # Update current environment
                    current_env = new_env
                    
                    # Update stacks
                    self.control_stack.append(new_env)
                    self.control_stack.append(lambda_obj.get_body())
                    self.value_stack.insert(0, new_env)
                    self.env_stack.append(new_env)
                
                elif isinstance(next_symbol, Tuple):
                    # Tuple selection (e.g., tup.3)
                    tuple_obj = next_symbol
                    index = int(self.value_stack.pop(0).get_value())
                    
                    # Get the element at the specified index (1-based)
                    self.value_stack.insert(0, tuple_obj.elements[index - 1])
                
                elif isinstance(next_symbol, Ystar):
                    # Handle recursion operator
                    lambda_obj = self.value_stack.pop(0)
                    eta_obj = Eta()
                    eta_obj.set_index(lambda_obj.get_index())
                    eta_obj.set_environment(lambda_obj.get_environment())
                    eta_obj.set_parameter(lambda_obj.parameters[0])
                    eta_obj.set_lambda(lambda_obj)
                    self.value_stack.insert(0, eta_obj)
                
                elif isinstance(next_symbol, Eta):
                    # Handle eta (recursive function)
                    eta_obj = next_symbol
                    lambda_obj = eta_obj.get_lambda()
                    
                    # Set up for recursive call
                    self.control_stack.append(Gamma())
                    self.control_stack.append(Gamma())
                    self.value_stack.insert(0, eta_obj)
                    self.value_stack.insert(0, lambda_obj)
                
                else:
                    # Built-in functions
                    if next_symbol.get_value() == "Print":
                        # Print function is a no-op in this implementation
                        # (result will be on the value stack at the end)
                        pass
                        
                    elif next_symbol.get_value() == "Stem":
                        # Get first character of string
                        s = self.value_stack.pop(0)
                        s.set_value(s.get_value()[0])
                        self.value_stack.insert(0, s)
                        
                    elif next_symbol.get_value() == "Stern":
                        # Get all but first character of string
                        s = self.value_stack.pop(0)
                        s.set_value(s.get_value()[1:])
                        self.value_stack.insert(0, s)
                        
                    elif next_symbol.get_value() == "Conc":
                        # Concatenate strings
                        s1 = self.value_stack.pop(0)
                        s2 = self.value_stack.pop(0)
                        s1.set_value(s1.get_value() + s2.get_value())
                        self.value_stack.insert(0, s1)
                        
                    elif next_symbol.get_value() == "Order":
                        # Get length of tuple
                        tuple_obj = self.value_stack.pop(0)
                        length = IntegerValue(str(len(tuple_obj.elements)))
                        self.value_stack.insert(0, length)
                        
                    elif next_symbol.get_value() == "Isinteger":
                        # Check if value is an integer
                        result = BoolValue("true" if isinstance(self.value_stack[0], IntegerValue) else "false")
                        self.value_stack.insert(0, result)
                        self.value_stack.pop(1)
                        
                    elif next_symbol.get_value() == "Isstring":
                        # Check if value is a string
                        result = BoolValue("true" if isinstance(self.value_stack[0], StringValue) else "false")
                        self.value_stack.insert(0, result)
                        self.value_stack.pop(1)
                        
                    elif next_symbol.get_value() == "Istuple":
                        # Check if value is a tuple
                        result = BoolValue("true" if isinstance(self.value_stack[0], Tuple) else "false")
                        self.value_stack.insert(0, result)
                        self.value_stack.pop(1)
                        
                    elif next_symbol.get_value() == "Isdummy":
                        # Check if value is dummy
                        result = BoolValue("true" if isinstance(self.value_stack[0], DummyValue) else "false")
                        self.value_stack.insert(0, result)
                        self.value_stack.pop(1)
                        
                    elif next_symbol.get_value() == "Istruthvalue":
                        # Check if value is a boolean
                        result = BoolValue("true" if isinstance(self.value_stack[0], BoolValue) else "false")
                        self.value_stack.insert(0, result)
                        self.value_stack.pop(1)
                        
                    elif next_symbol.get_value() == "Isfunction":
                        # Check if value is a function
                        result = BoolValue("true" if isinstance(self.value_stack[0], Lambda) else "false")
                        self.value_stack.insert(0, result)
                        self.value_stack.pop(1)
            
            elif isinstance(current_symbol, Environment):
                # Pop environment
                self.value_stack.pop(1)  # Remove environment from value stack
                self.env_stack[current_symbol.get_index()].mark_for_deletion()
                
                # Find the next active environment
                for i in range(len(self.env_stack) - 1, -1, -1):
                    if not self.env_stack[i].is_deleted():
                        current_env = self.env_stack[i]
                        break
            
            elif isinstance(current_symbol, UnaryOperator):
                # Apply unary operator
                operand = self.value_stack.pop(0)
                result = self._apply_unary_operation(current_symbol, operand)
                self.value_stack.insert(0, result)
                
            elif isinstance(current_symbol, BinaryOperator):
                # Apply binary operator
                operand1 = self.value_stack.pop(0)
                operand2 = self.value_stack.pop(0)
                result = self._apply_binary_operation(current_symbol, operand1, operand2)
                self.value_stack.insert(0, result)
                
            elif isinstance(current_symbol, Beta):
                # Conditional branching
                if self.value_stack[0].get_value() == "true":
                    # Condition is true, remove the false branch
                    self.control_stack.pop()
                else:
                    # Condition is false, remove the true branch
                    self.control_stack.pop(-2)
                
                # Remove the condition from the value stack
                self.value_stack.pop(0)
                
            elif isinstance(current_symbol, Tau):
                # Tuple construction
                tau = current_symbol
                tuple_obj = Tuple()
                
                # Pop elements from value stack and add to tuple
                for _ in range(tau.get_size()):
                    tuple_obj.elements.append(self.value_stack.pop(0))
                
                # Push tuple to value stack
                self.value_stack.insert(0, tuple_obj)
                
            elif isinstance(current_symbol, Delta):
                # Execute delta (instruction sequence)
                self.control_stack.extend(current_symbol.instructions)
                
            elif isinstance(current_symbol, ControlStructure):
                # Execute control structure
                self.control_stack.extend(current_symbol.instructions)
                
            else:
                # Push any other symbols to the value stack
                self.value_stack.insert(0, current_symbol)
    
    def _apply_unary_operation(self, operator, operand):
        """Apply a unary operator to an operand.
        
        Args:
            operator: A UnaryOperator object
            operand: The operand value
            
        Returns:
            The result of applying the operator to the operand
        """
        if operator.get_value() == "neg":
            # Negation
            value = int(operand.get_value())
            return IntegerValue(str(-value))
            
        elif operator.get_value() == "not":
            # Logical NOT
            value = self._convert_to_bool(operand.get_value())
            return BoolValue(str(not value).lower())
            
        else:
            # Unknown operator
            return ErrorSymbol(f"Unknown unary operator: {operator.get_value()}")
    
    def _apply_binary_operation(self, operator, operand1, operand2):
        """Apply a binary operator to two operands.
        
        Args:
            operator: A BinaryOperator object
            operand1: The first operand
            operand2: The second operand
            
        Returns:
            The result of applying the operator to the operands
        """
        op = operator.get_value()
        
        # Arithmetic operators
        if op == "+":
            val1 = int(operand1.get_value())
            val2 = int(operand2.get_value())
            return IntegerValue(str(val1 + val2))
            
        elif op == "-":
            val1 = int(operand1.get_value())
            val2 = int(operand2.get_value())
            return IntegerValue(str(val1 - val2))
            
        elif op == "*":
            val1 = int(operand1.get_value())
            val2 = int(operand2.get_value())
            return IntegerValue(str(val1 * val2))
            
        elif op == "/":
            val1 = int(operand1.get_value())
            val2 = int(operand2.get_value())
            if val2 == 0:
                return ErrorSymbol("Division by zero")
            return IntegerValue(str(val1 // val2))
            
        elif op == "**":
            val1 = int(operand1.get_value())
            val2 = int(operand2.get_value())
            return IntegerValue(str(val1 ** val2))
        
        # Logical operators
        elif op == "&":
            val1 = self._convert_to_bool(operand1.get_value())
            val2 = self._convert_to_bool(operand2.get_value())
            return BoolValue(str(val1 and val2).lower())
            
        elif op == "or":
            val1 = self._convert_to_bool(operand1.get_value())
            val2 = self._convert_to_bool(operand2.get_value())
            return BoolValue(str(val1 or val2).lower())
        
        # Comparison operators
        elif op == "eq":
            val1 = operand1.get_value()
            val2 = operand2.get_value()
            return BoolValue(str(val1 == val2).lower())
            
        elif op == "ne":
            val1 = operand1.get_value()
            val2 = operand2.get_value()
            return BoolValue(str(val1 != val2).lower())
            
        elif op == "ls":
            val1 = int(operand1.get_value())
            val2 = int(operand2.get_value())
            return BoolValue(str(val1 < val2).lower())
            
        elif op == "le":
            val1 = int(operand1.get_value())
            val2 = int(operand2.get_value())
            return BoolValue(str(val1 <= val2).lower())
            
        elif op == "gr":
            val1 = int(operand1.get_value())
            val2 = int(operand2.get_value())
            return BoolValue(str(val1 > val2).lower())
            
        elif op == "ge":
            val1 = int(operand1.get_value())
            val2 = int(operand2.get_value())
            return BoolValue(str(val1 >= val2).lower())
        
        # Tuple augmentation
        elif op == "aug":
            if isinstance(operand2, Tuple):
                # Add all elements from second tuple to first
                operand1.elements.extend(operand2.elements)
            else:
                # Add single element
                operand1.elements.append(operand2)
            return operand1
            
        else:
            # Unknown operator
            return ErrorSymbol(f"Unknown binary operator: {op}")
    
    def _convert_to_bool(self, value):
        """Convert a string value to a Python boolean.
        
        Args:
            value: A string value ('true' or 'false')
            
        Returns:
            True if value is 'true', False if value is 'false'
        """
        return value == "true"
    
    def _format_tuple(self, tuple_obj):
        """Format a tuple for display.
        
        Args:
            tuple_obj: A Tuple object
            
        Returns:
            A string representation of the tuple
        """
        result = "("
        for i, element in enumerate(tuple_obj.elements):
            if isinstance(element, Tuple):
                result += self._format_tuple(element)
            else:
                result += element.get_value()
            
            if i < len(tuple_obj.elements) - 1:
                result += ", "
        
        result += ")"
        return result
    
    def get_result(self):
        """Get the final result from the CSE machine.
        
        Returns:
            The formatted result value as a string
        """
        # Evaluate the program
        self.evaluate()
        
        # Check if there's a result on the value stack
        if not self.value_stack:
            return "Error: No result on value stack"
        
        # Format the result based on its type
        result = self.value_stack[0]
        
        if isinstance(result, Tuple):
            return self._format_tuple(result)
        else:
            return result.get_value()
    
    def _write_value_stack_to_file(self, file_path):
        """Write the value stack to a file for debugging purposes.
        
        Args:
            file_path: The path to the output file
        """
        with open(file_path, 'a') as file:
            for symbol in self.value_stack:
                file.write(symbol.get_value())
                if isinstance(symbol, (Lambda, Delta, Environment, Eta)):
                    file.write(str(symbol.get_index()))
                file.write(",")
            file.write("\n")
    
    def _write_control_stack_to_file(self, file_path):
        """Write the control stack to a file for debugging purposes.
        
        Args:
            file_path: The path to the output file
        """
        with open(file_path, 'a') as file:
            for symbol in self.control_stack:
                file.write(symbol.get_value())
                if isinstance(symbol, (Lambda, Delta, Environment, Eta)):
                    file.write(str(symbol.get_index()))
                file.write(",")
            file.write("\n")
    
    @staticmethod
    def clear_file(file_path):
        """Clear the contents of a file.
        
        Args:
            file_path: The path to the file to clear
        """
        open(file_path, 'w').close()