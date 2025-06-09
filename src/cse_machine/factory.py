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
from .machine import CSEMachine

class CSEMachineFactory:
    """Factory for creating CSE machine components from the AST.
    
    This class transforms an abstract syntax tree (AST) into the standardized
    control structure needed by the CSE machine. It handles the conversion of
    AST nodes into appropriate CSE machine symbols and creates the initial
    control, stack, and environment structures.
    
    The standardization process transforms the AST into a structure that
    can be directly executed by the CSE machine, handling scoping rules,
    environment creation, and function closures.
    
    Attributes:
        e0 (E): The base environment (environment 0)
        i (int): Counter for generating unique lambda indices
        j (int): Counter for generating unique delta indices
    """
    
    def __init__(self):
        """Initialize a new CSE machine factory.
        
        Creates a base environment (e0) and initializes counters for 
        generating unique indices for lambdas and deltas during the
        standardization process.
        """
        self.e0 = E(0)         # Create the base environment
        self.i = 1             # Lambda index counter (starts at 1)
        self.j = 0             # Delta index counter (starts at 0)

    def get_symbol(self, node):
        """Convert an AST node into a CSE machine symbol.
        
        This method maps AST nodes to their corresponding CSE machine symbols
        based on node type and data.
        
        Args:
            node: AST node to convert
            
        Returns:
            Symbol: The CSE machine symbol corresponding to the AST node
        """
        data = node.get_data()
        
        # Handle operators
        if data in ("not", "neg"):
            return Uop(data)  # Unary operator symbol
        elif data in ("+", "-", "*", "/", "**", "&", "or", "eq", "ne", "ls", "le", "gr", "ge", "aug"):
            return Bop(data)  # Binary operator symbol
        elif data == "gamma":
            return Gamma()  # Gamma symbol
        elif data == "tau":
            return Tau(len(node.get_children()))  # Tau symbol with the number of children
        elif data == "<Y*>":
            return Ystar()  # Y* symbol
        else:
            # Handle literals and identifiers
            if data.startswith("<IDENTIFIER:"):
                return Id(data[12:-1])  # Identifier symbol
            elif data.startswith("<INTEGER:"):
                return Int(data[9:-1])  # Integer symbol
            elif data.startswith("<STRING:"):
                return Str(data[9:-2])  # String symbol
            elif data.startswith("STRING:"):
                return Str(data[8:-2]) 
            elif data.startswith("<NIL"):
                return Tup()  # Empty tuple symbol
            elif data.startswith("<TRUE_VALUE:t"):
                return Bool("true")  # Boolean true symbol
            elif data.startswith("<TRUE_VALUE:f"):
                return Bool("false")  # Boolean false symbol
            elif data.startswith("<dummy>"):
                return Dummy()  # Dummy symbol
            else:
                print("Err node:", data)
                return Err()  # Error symbol for unrecognized nodes

    def get_b(self, node):
        """Create a B (base environment) node from an AST node.
        
        Args:
            node: AST node to convert
            
        Returns:
            B: A base environment node containing the symbols from the AST node
        """
        b = B()
        b.symbols = self.get_pre_order_traverse(node)
        return b

    def get_lambda(self, node):
        """Create a Lambda node from an AST node.
        
        This handles the conversion of lambda abstractions in the AST to
        Lambda nodes in the CSE machine, setting up parameter identifiers
        and the function body as a delta.
        
        Args:
            node: AST lambda node to convert
            
        Returns:
            Lambda: A lambda node representing the function abstraction
        """
        lambda_expr = Lambda(self.i)  # Create new lambda with unique index
        self.i += 1
        
        # Set the function body as a delta
        lambda_expr.set_delta(self.get_delta(node.get_children()[1]))
        
        # Handle parameter identifiers
        if node.get_children()[0].get_data() == ",":
            # Multiple parameters (comma-separated)
            for identifier in node.get_children()[0].get_children():
                lambda_expr.identifiers.append(Id(identifier.get_data()[12:-1]))
        else:
            # Single parameter
            lambda_expr.identifiers.append(Id(node.get_children()[0].get_data()[12:-1]))
        
        return lambda_expr

    def get_pre_order_traverse(self, node):
        """Convert an AST node and its children to CSE machine symbols.
        
        This performs a pre-order traversal of the AST, converting each node
        to its corresponding CSE machine symbol.
        
        Args:
            node: AST node to traverse
            
        Returns:
            list: List of CSE machine symbols corresponding to the AST
        """
        symbols = []
        
        if node.get_data() == "lambda":
            # Handle lambda expressions
            symbols.append(self.get_lambda(node))
            
        elif node.get_data() == "->":
            # Handle conditional expressions (if-then-else)
            symbols.append(self.get_delta(node.get_children()[1]))  # 'then' branch
            symbols.append(self.get_delta(node.get_children()[2]))  # 'else' branch
            symbols.append(Beta())  # Conditional selector
            symbols.append(self.get_b(node.get_children()[0]))  # Condition
            
        else:
            # Handle regular nodes
            symbols.append(self.get_symbol(node))
            for child in node.get_children():
                symbols.extend(self.get_pre_order_traverse(child))
                
        return symbols

    def get_delta(self, node):
        """Create a Delta node from an AST node.
        
        Delta nodes mark environment boundaries in the CSE machine and
        contain the code to execute within that environment.
        
        Args:
            node: AST node to convert
            
        Returns:
            Delta: A delta node containing the symbols from the AST node
        """
        delta = Delta(self.j)  # Create new delta with unique index
        self.j += 1
        delta.symbols = self.get_pre_order_traverse(node)
        return delta

    def get_control(self, ast):
        """Create the initial control structure for the CSE machine.
        
        The control structure contains the base environment and the
        standardized program represented as a delta.
        
        Args:
            ast: The abstract syntax tree to convert
            
        Returns:
            list: The initial control structure for the CSE machine
        """
        control = [self.e0, self.get_delta(ast.get_root())]
        return control

    def get_stack(self):
        """Create the initial stack for the CSE machine.
        
        The initial stack contains only the base environment.
        
        Returns:
            list: The initial stack for the CSE machine
        """
        return [self.e0]

    def get_environment(self):
        """Create the initial environment for the CSE machine.
        
        The initial environment contains only the base environment.
        
        Returns:
            list: The initial environment for the CSE machine
        """
        return [self.e0]

    def get_cse_machine(self, ast):
        """Create a complete CSE machine from an abstract syntax tree.
        
        This method standardizes the AST and creates a CSE machine with
        the appropriate control, stack, and environment structures.
        
        Args:
            ast: The abstract syntax tree to execute
            
        Returns:
            CSEMachine: A fully initialized CSE machine ready to execute the program
        """
        control = self.get_control(ast)
        stack = self.get_stack()
        environment = self.get_environment()
        return CSEMachine(control, stack, environment)