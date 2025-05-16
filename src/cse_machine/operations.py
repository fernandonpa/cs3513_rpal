from .nodes import Int, Bool, Str, Tup, Symbol, Err
from .error_handler import TypeMismatchError, UndefinedOperationError, DivisionByZeroError, handle_error

def apply_unary_operation(operator, operand):
    """Apply a unary operation to an operand"""
    op_name = operator.get_data()
    
    try:
        if op_name == "neg":
            if not isinstance(operand, Int):
                raise TypeMismatchError("neg", "Int", type(operand).__name__)
            return Int(-int(operand.get_data()))
        
        elif op_name == "not":
            if not isinstance(operand, Bool):
                raise TypeMismatchError("not", "Bool", type(operand).__name__)
            return Bool(not operand.get_value())
        
        else:
            raise UndefinedOperationError(op_name)
    
    except Exception as e:
        return handle_error(e)

def apply_binary_operation(operator, left, right):
    """Apply a binary operation to two operands"""
    op_name = operator.get_data()
    
    try:
        # Arithmetic operations
        if op_name in ("+", "-", "*", "/", "**"):
            if not isinstance(left, Int) or not isinstance(right, Int):
                raise TypeMismatchError(op_name, "Int, Int", f"{type(left).__name__}, {type(right).__name__}")
            
            left_val = int(left.get_data())
            right_val = int(right.get_data())
            
            if op_name == "+":
                return Int(left_val + right_val)
            elif op_name == "-":
                return Int(left_val - right_val)
            elif op_name == "*":
                return Int(left_val * right_val)
            elif op_name == "/":
                if right_val == 0:
                    raise DivisionByZeroError()
                return Int(left_val // right_val)  # Integer division
            elif op_name == "**":
                return Int(left_val ** right_val)
        
        # Logical operations
        elif op_name in ("&", "or"):
            if not isinstance(left, Bool) or not isinstance(right, Bool):
                raise TypeMismatchError(op_name, "Bool, Bool", f"{type(left).__name__}, {type(right).__name__}")
            
            left_val = left.get_value()
            right_val = right.get_value()
            
            if op_name == "&":
                return Bool(left_val and right_val)
            elif op_name == "or":
                return Bool(left_val or right_val)
        
        # Comparison operations
        elif op_name in ("eq", "ne"):
            # These can compare any types
            left_val = left.get_data()
            right_val = right.get_data()
            
            if op_name == "eq":
                return Bool(left_val == right_val)
            elif op_name == "ne":
                return Bool(left_val != right_val)
            
        elif op_name in ("ls", "le", "gr", "ge"):
            # These require numeric operands
            if not isinstance(left, Int) or not isinstance(right, Int):
                raise TypeMismatchError(op_name, "Int, Int", f"{type(left).__name__}, {type(right).__name__}")
            
            left_val = int(left.get_data())
            right_val = int(right.get_data())
            
            if op_name == "ls":
                return Bool(left_val < right_val)
            elif op_name == "le":
                return Bool(left_val <= right_val)
            elif op_name == "gr":
                return Bool(left_val > right_val)
            elif op_name == "ge":
                return Bool(left_val >= right_val)
        
        # Tuple augmentation
        elif op_name == "aug":
            if not isinstance(left, Tup):
                # Convert left to a tuple with a single element
                new_tup = Tup()
                new_tup.add_element(left)
                left = new_tup
            
            # Make a copy of the tuple to avoid modifying the original
            result = Tup()
            for element in left.get_elements():
                result.add_element(element)
            
            result.add_element(right)
            return result
        
        else:
            raise UndefinedOperationError(op_name)
            
    except Exception as e:
        return handle_error(e)