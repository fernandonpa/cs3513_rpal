from enum import Enum

class NodeType(Enum):
    """Enumeration of node types for the RPAL Abstract Syntax Tree.
    
    This enum defines the different types of nodes that can appear in the AST
    during parsing of RPAL programs. Each type represents a specific language
    construct or operation.
    
    Attributes:
        let (int): Represents a let binding (let <id> = <expr> in <expr>)
        fcn_form (int): Function form or definition
        identifier (int): Variable or function name
        integer (int): Integer literal value
        string (int): String literal value
        where (int): Where expression (<expr> where <definitions>)
        gamma (int): Function application node (represents function calls)
        lambda_expr (int): Lambda abstraction (anonymous function)
        tau (int): Tuple construction operator
        rec (int): Recursive definition marker
        aug (int): Augmentation operation for extending environments
        conditional (int): If-then-else expression
        op_or (int): Logical OR operation
        op_and (int): Logical AND operation
        op_not (int): Logical NOT operation
        op_compare (int): Comparison operations (gr, ge, ls, le)
        op_plus (int): Addition operation
        op_minus (int): Subtraction operation
        op_neg (int): Unary negation
        op_mul (int): Multiplication operation
        op_div (int): Division operation
        op_pow (int): Exponentiation operation
        at (int): Pattern matching at-sign (@)
        true_value (int): Boolean true literal
        false_value (int): Boolean false literal
        nil (int): Nil value (similar to null)
        dummy (int): Placeholder node
        within (int): Within expression (similar to let/where)
        and_op (int): Multiple definitions separator
        equal (int): Equality test operation
        comma (int): Comma separator (for lists/tuples)
        empty_params (int): Empty parameter list marker
    """
    let = 1
    fcn_form = 2
    identifier = 3
    integer = 4
    string = 5
    where = 6
    gamma = 7
    lambda_expr = 8
    tau = 9
    rec = 10
    aug = 11
    conditional = 12
    op_or = 13
    op_and = 14
    op_not = 15
    op_compare = 16
    op_plus = 17
    op_minus = 18
    op_neg = 19
    op_mul = 20
    op_div = 21
    op_pow = 22
    at = 23
    true_value = 24
    false_value = 25
    nil = 26
    dummy = 27
    within = 28
    and_op = 29
    equal = 30
    comma = 31
    empty_params = 32