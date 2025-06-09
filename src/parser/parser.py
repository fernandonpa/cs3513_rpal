from enum import Enum
from ..lexer.lexer import TokenType, MyToken
from .node_types import NodeType
from .ast_node import Node


class Parser:
    """Parser for the RPAL language.
    
    This class implements a recursive-descent parser that converts a stream of tokens
    into an Abstract Syntax Tree (AST) according to the RPAL language grammar. The parser
    follows the standard RPAL grammar rules, handling expressions, definitions, and
    various language constructs.
    
    Attributes:
        tokens (list): List of MyToken objects to be parsed
        ast (list): A stack used to build the AST during parsing
        string_ast (list): Holds a string representation of the AST for debugging
    """
    
    def __init__(self, tokens):
        """Initialize a new parser with a token stream.
        
        Args:
            tokens (list): A list of MyToken objects from the lexical analysis phase
        """
        self.tokens = tokens  # Store the token stream to be parsed
        self.ast = []  # Stack to build the Abstract Syntax Tree
        self.string_ast = []  # For string representation of AST

    def parse(self):
        """Parse the token stream into an Abstract Syntax Tree.
        
        Starts the parsing process from the root of the grammar (E production).
        
        Returns:
            list: The constructed AST if parsing is successful
            None: If parsing fails
        """
        self.tokens.append(MyToken(TokenType.END_OF_TOKENS, ""))  # Add an End Of Tokens marker
        self.E()  # Start parsing from the entry point
        
        # Check if we've consumed all tokens (except the end marker)
        if self.tokens[0].type == TokenType.END_OF_TOKENS:
            return self.ast
        else:
            # Parsing failed - some tokens weren't processed
            print("Parsing Unsuccessful!...........")
            print("REMAINIG UNPARSED TOKENS:")
            for token in self.tokens:
                print("<" + str(token.type) + ", " + token.value + ">")
            return None

    def convert_ast_to_string_ast(self):
        """Convert the AST into a readable string representation.
        
        This method transforms the abstract syntax tree into a flattened string
        representation with dots indicating the nesting level, primarily for
        debugging and visualization purposes.
        
        Returns:
            list: String representation of the AST with proper indentation
        """
        dots = ""  # Tracks nesting level with dots
        stack = []  # Stack for processing nodes

        # Process all nodes in the AST
        while self.ast:
            if not stack:
                # Start of processing - check if current node has children
                if self.ast[-1].no_of_children == 0:
                    # Leaf node - add to string representation directly
                    self.add_strings(dots, self.ast.pop())
                else:
                    # Non-leaf node - push to stack for further processing
                    node = self.ast.pop()
                    stack.append(node)
            else:
                # Continue processing with stack
                if self.ast[-1].no_of_children > 0:
                    # Move node to stack and increase nesting level
                    node = self.ast.pop()
                    stack.append(node)
                    dots += "."  # Increase indentation
                else:
                    # Process leaf node
                    stack.append(self.ast.pop())
                    dots += "."
                    # Process all leaf nodes at current level
                    while stack[-1].no_of_children == 0:
                        self.add_strings(dots, stack.pop())
                        if not stack:
                            break
                        dots = dots[:-1]  # Decrease indentation
                        node = stack.pop()
                        node.no_of_children -= 1  # Decrement child count
                        stack.append(node)  # Put back on stack

        # Reverse the list to get correct order
        self.string_ast.reverse()
        return self.string_ast

    def add_strings(self, dots, node):
        """Add a node to the string representation of the AST.
        
        Args:
            dots (str): The indentation level represented by dots
            node (Node): The AST node to convert to string
        """
        # Special formatting for nodes with values
        if node.type in [NodeType.identifier, NodeType.integer, NodeType.string, NodeType.true_value,
                         NodeType.false_value, NodeType.nil, NodeType.dummy]:
            self.string_ast.append(dots + "<" + node.type.name.upper() + ":" + node.value + ">")
        elif node.type == NodeType.fcn_form:
            # Special case for function form
            self.string_ast.append(dots + "function_form")
        else:
            # Standard case
            self.string_ast.append(dots + node.value)

    # ======= RECURSIVE DESCENT PARSER IMPLEMENTATION =======
    # Each method below implements a production rule from the RPAL grammar
                
    def E(self):
        """Parse an Expression (E).
        
        Grammar rule:
        E -> 'let' D 'in' E => 'let'
          -> 'fn' Vb+ '.' E => 'lambda'
          -> Ew
        """
        if self.tokens:  # Ensure tokens list is not empty
            token = self.tokens[0]
            if hasattr(token, 'type') and hasattr(token, 'value'):  # Check if token has type and value attributes
                if token.type == TokenType.KEYWORD and token.value in ["let", "fn"]:
                    if token.value == "let":
                        # Handle let expression: let D in E
                        self.tokens.pop(0)  # Remove "let"
                        self.D()  # Parse definition
                        if self.tokens[0].value != "in":
                            print("Parse error at E : 'in' Expected")
                        self.tokens.pop(0)  # Remove "in"
                        self.E()  # Parse expression
                        self.ast.append(Node(NodeType.let, "let", 2))  # Create let node with 2 children (D and E)
                    else:
                        # Handle lambda expression: fn Vb+ . E
                        self.tokens.pop(0)  # Remove "fn"
                        n = 0  # Count parameters
                        while self.tokens and (self.tokens[0].type == TokenType.IDENTIFIER or self.tokens[0].value == "("):
                            self.Vb()  # Parse parameter
                            n += 1
                        if self.tokens and self.tokens[0].value != ".":
                            print("Parse error at E : '.' Expected")
                        if self.tokens:
                            self.tokens.pop(0)  # Remove "."
                            self.E()  # Parse body expression
                            # Create lambda node with n+1 children (n parameters and 1 body)
                            self.ast.append(Node(NodeType.lambda_expr, "lambda", n + 1))
                else:
                    # Default case: expression with where clause
                    self.Ew()
            else:
                print("Invalid token format.")
        else:
            print("Tokens list is empty.")


    def Ew(self):
        """Parse an expression with optional where clause (Ew).
        
        Grammar rule:
        Ew -> T 'where' Dr => 'where'
           -> T
        """
        self.T()  # Parse tuple expression
        if self.tokens and self.tokens[0].value == "where":
            # Handle where expression
            self.tokens.pop(0)  # Remove "where"
            self.Da()  # Parse definitions
            self.ast.append(Node(NodeType.where, "where", 2))  # Create where node with 2 children

    def T(self):
        """Parse a tuple expression (T).
        
        Grammar rule:
        T -> Ta ( ',' Ta )+ => 'tau'
          -> Ta
        """
        self.Ta()  # Parse first element
        n = 1  # Count tuple elements
        while self.tokens and self.tokens[0].value == ",":
            self.tokens.pop(0)  # Remove comma
            self.Ta()  # Parse next element
            n += 1
        if n > 1:
            # Create tuple node if we have multiple elements
            self.ast.append(Node(NodeType.tau, "tau", n))

    def Ta(self):
        """Parse an augmentation expression (Ta).
        
        Grammar rule (converted from left recursion):
        Ta -> Tc ('aug' Tc)*
        
        Original rule:
        Ta -> Ta 'aug' Tc => 'aug'
           -> Tc
        """
        self.Tc()  # Parse conditional expression
        while self.tokens and self.tokens[0].value == "aug":
            self.tokens.pop(0)  # Remove "aug"
            self.Tc()  # Parse next part
            self.ast.append(Node(NodeType.aug, "aug", 2))  # Create aug node

    def Tc(self):
        """Parse a conditional expression (Tc).
        
        Grammar rule:
        Tc -> B '->' Tc '|' Tc => '->'
           -> B
        """
        self.B()  # Parse boolean expression
        if self.tokens and self.tokens[0].value == "->":
            # Handle conditional expression (if-then-else)
            self.tokens.pop(0)  # Remove '->'
            self.Tc()  # Parse 'then' branch
            if not self.tokens or self.tokens[0].value != "|":
                print("Parse error at Tc: conditional '|' expected")
                return
            self.tokens.pop(0)  # Remove '|'
            self.Tc()  # Parse 'else' branch
            # Create conditional node with 3 children (condition, then, else)
            self.ast.append(Node(NodeType.conditional, "->", 3))

    def B(self):
        """Parse a boolean expression with 'or' (B).
        
        Grammar rule (converted from left recursion):
        B -> Bt ('or' Bt)*
        
        Original rule:
        B -> B 'or' Bt => 'or'
          -> Bt
        """
        self.Bt()  # Parse boolean term
        while self.tokens and self.tokens[0].value == "or":
            self.tokens.pop(0)  # Remove 'or'
            self.Bt()  # Parse next term
            self.ast.append(Node(NodeType.op_or, "or", 2))  # Create or node

    def Bt(self):
        """Parse a boolean term with '&' (Bt).
        
        Grammar rule (converted from left recursion):
        Bt -> Bs ('&' Bs)*
        
        Original rule:
        Bt -> Bt '&' Bs => '&'
           -> Bs
        """
        self.Bs()  # Parse boolean simple expression
        while self.tokens and self.tokens[0].value == "&":
            self.tokens.pop(0)  # Remove '&'
            self.Bs()  # Parse next simple expression
            self.ast.append(Node(NodeType.op_and, "&", 2))  # Create and node

    def Bs(self):
        """Parse a simple boolean expression with 'not' (Bs).
        
        Grammar rule:
        Bs -> 'not' Bp => 'not'
           -> Bp
        """
        if self.tokens and self.tokens[0].value == "not":
            # Handle not expression
            self.tokens.pop(0)  # Remove 'not'
            self.Bp()  # Parse boolean primary
            self.ast.append(Node(NodeType.op_not, "not", 1))  # Create not node with 1 child
        else:
            self.Bp()  # Parse boolean primary

    def Bp(self):
        """Parse a boolean primary expression with comparisons (Bp).
        
        Grammar rule:
        Bp -> A ('gr' | '>' ) A => 'gr'
           -> A ('ge' | '>=') A => 'ge'
           -> A ('ls' | '<' ) A => 'ls'
           -> A ('le' | '<=') A => 'le'
           -> A 'eq' A => 'eq'
           -> A 'ne' A => 'ne'
           -> A
        """
        self.A()  # Parse arithmetic expression
        if self.tokens:
            token = self.tokens[0]
            # Check for comparison operators
            if token.value in [">", ">=", "<", "<=", "gr", "ge", "ls", "le", "eq", "ne"]:
                self.tokens.pop(0)  # Remove operator
                self.A()  # Parse right-hand side
                
                # Create appropriate comparison node
                if token.value == ">":
                    self.ast.append(Node(NodeType.op_compare, "gr", 2))
                elif token.value == ">=":
                    self.ast.append(Node(NodeType.op_compare, "ge", 2))
                elif token.value == "<":
                    self.ast.append(Node(NodeType.op_compare, "ls", 2))
                elif token.value == "<=":
                    self.ast.append(Node(NodeType.op_compare, "le", 2))
                else:
                    self.ast.append(Node(NodeType.op_compare, token.value, 2))

    def A(self):
        """Parse an arithmetic expression with +/- (A).
        
        Grammar rule (with unary operators):
        A -> A '+' At => '+'
          -> A '-' At => '-'
          -> '+' At
          -> '-'At =>'neg'
          -> At
        """
        # Handle unary operators
        if self.tokens and self.tokens[0].value == "+":
            self.tokens.pop(0)  # Remove unary plus (no effect)
            self.At()
        elif self.tokens and self.tokens[0].value == "-":
            self.tokens.pop(0)  # Remove unary minus
            self.At()
            self.ast.append(Node(NodeType.op_neg, "neg", 1))  # Create negation node
        else:
            self.At()  # Parse arithmetic term

        # Handle binary +/- operators (left-associative)
        while self.tokens and self.tokens[0].value in {"+", "-"}:
            current_token = self.tokens[0]  # Save operator
            self.tokens.pop(0)  # Remove operator
            self.At()  # Parse next term
            
            # Create appropriate node
            if current_token.value == "+":
                self.ast.append(Node(NodeType.op_plus, "+", 2))
            else:
                self.ast.append(Node(NodeType.op_minus, "-", 2))

    def At(self):
        """Parse an arithmetic term with */÷ (At).
        
        Grammar rule (converted from left recursion):
        At -> Af ('*' Af | '/' Af)*
        
        Original rule:
        At -> At '*' Af => '*'
           -> At '/' Af => '/'
           -> Af
        """
        self.Af()  # Parse arithmetic factor
        
        # Handle multiplication and division (left-associative)
        while self.tokens and self.tokens[0].value in {"*", "/"}:
            current_token = self.tokens[0]  # Save operator
            self.tokens.pop(0)  # Remove operator
            self.Af()  # Parse next factor
            
            # Create appropriate node
            if current_token.value == "*":
                self.ast.append(Node(NodeType.op_mul, "*", 2))
            else:
                self.ast.append(Node(NodeType.op_div, "/", 2))

    def Af(self):
        """Parse an arithmetic factor with ** (Af).
        
        Grammar rule (converted from right recursion):
        Af -> Ap ('**' Af)?
        
        Original rule:
        Af -> Ap '**' Af => '**'
           -> Ap
        """
        self.Ap()  # Parse arithmetic primary
        
        # Handle exponentiation (right-associative)
        if self.tokens and self.tokens[0].value == "**":
            self.tokens.pop(0)  # Remove power operator
            self.Af()  # Parse exponent (recursive for right-associativity)
            self.ast.append(Node(NodeType.op_pow, "**", 2))  # Create power node

    def Ap(self):
        """Parse an arithmetic primary with @ (pattern matching) (Ap).
        
        Grammar rule (converted from left recursion):
        Ap -> R ('@' '<IDENTIFIER>' R)*
        
        Original rule:
        Ap -> Ap '@' '<IDENTIFIER>' R => '@'
           -> R
        """
        self.R()  # Parse rator/rand
        
        # Handle pattern matching expressions
        while self.tokens and self.tokens[0].value == "@":
            self.tokens.pop(0)  # Remove @ operator
            
            if not self.tokens or self.tokens[0].type != TokenType.IDENTIFIER:
                print("Parsing error at Ap: IDENTIFIER EXPECTED")
                return
            
            # Add identifier node
            self.ast.append(Node(NodeType.identifier, self.tokens[0].value, 0))
            self.tokens.pop(0)  # Remove IDENTIFIER
            
            self.R()  # Parse right part
            # Create @ node with 3 children (expr, id, expr)
            self.ast.append(Node(NodeType.at, "@", 3))

    def R(self):
        """Parse a rator/rand expression (function application) (R).
        
        Grammar rule (converted from left recursion):
        R -> Rn (Rn)*
        
        Original rule:
        R -> R Rn => 'gamma'
          -> Rn
        
        Note: Each function application creates a 'gamma' node.
        """
        self.Rn()  # Parse first rand
        
        # Handle function application (left-associative)
        while (self.tokens and 
               (self.tokens[0].type in [TokenType.IDENTIFIER, TokenType.INTEGER, TokenType.STRING] or
                self.tokens[0].value in ["true", "false", "nil", "dummy"] or
                self.tokens[0].value == "(")):
            
            self.Rn()  # Parse argument
            # Create gamma node (function application) with 2 children (function, arg)
            self.ast.append(Node(NodeType.gamma, "gamma", 2))

    def Rn(self):
        """Parse a rand (function argument or atom) (Rn).
        
        Grammar rule:
        Rn -> '<IDENTIFIER>'
           -> '<INTEGER>'
           -> '<STRING>'
           -> 'true' => 'true'
           -> 'false' => 'false'
           -> 'nil' => 'nil'
           -> '(' E ')'
           -> 'dummy' => 'dummy'
        """
        token_type = self.tokens[0].type
        token_value = self.tokens[0].value
        
        if token_type == TokenType.IDENTIFIER:
            # Handle identifier
            self.ast.append(Node(NodeType.identifier, token_value, 0))
            self.tokens.pop(0)
        elif token_type == TokenType.INTEGER:
            # Handle integer literal
            self.ast.append(Node(NodeType.integer, token_value, 0))
            self.tokens.pop(0)
        elif token_type == TokenType.STRING:
            # Handle string literal
            self.ast.append(Node(NodeType.string, token_value, 0))
            self.tokens.pop(0)
        elif token_type == TokenType.KEYWORD:
            # Handle keywords (true, false, nil, dummy)
            if token_value == "true":
                self.ast.append(Node(NodeType.true_value, token_value, 0))
                self.tokens.pop(0)
            elif token_value == "false":
                self.ast.append(Node(NodeType.false_value, token_value, 0))
                self.tokens.pop(0)
            elif token_value == "nil":
                self.ast.append(Node(NodeType.nil, token_value, 0))
                self.tokens.pop(0)
            elif token_value == "dummy":
                self.ast.append(Node(NodeType.dummy, token_value, 0))
                self.tokens.pop(0)
            else:
                print("Parse Error at Rn: Unexpected KEYWORD")
        elif token_type == TokenType.PUNCTUATION:
            if token_value == "(":
                # Handle parenthesized expression
                self.tokens.pop(0)  # Remove '('
                self.E()  # Parse inner expression
                
                if self.tokens[0].value != ")":
                    print("Parsing error at Rn: Expected a matching ')'")
                self.tokens.pop(0)  # Remove ')'
            else:
                print("Parsing error at Rn: Unexpected PUNCTUATION")
        else:
            print(token_type, token_value)
            print("Parsing error at Rn: Expected a Rn, but got different")

    def D(self):
        """Parse a definition (D).
        
        Grammar rule:
        D -> Da 'within' D => 'within'
          -> Da
        """
        self.Da()  # Parse definition and
        if self.tokens and self.tokens[0].value == "within":
            # Handle within expression
            self.tokens.pop(0)  # Remove 'within'
            self.D()  # Parse inner definition
            self.ast.append(Node(NodeType.within, "within", 2))  # Create within node

    def Da(self):
        """Parse a definition and (Da).
        
        Grammar rule:
        Da -> Dr ( 'and' Dr )+ => 'and'
           -> Dr
        """
        self.Dr()  # Parse definition rec
        n = 1  # Count definitions
        while self.tokens and self.tokens[0].value == "and":
            self.tokens.pop(0)  # Remove 'and'
            self.Dr()  # Parse next definition
            n += 1
        if n > 1:
            # Create and node if we have multiple definitions
            self.ast.append(Node(NodeType.and_op, "and", n))

    def Dr(self):
        """Parse a recursive definition (Dr).
        
        Grammar rule:
        Dr -> 'rec' Db => 'rec'
          -> Db
        """
        is_rec = False
        if self.tokens and self.tokens[0].value == "rec":
            # Check for recursive definition
            self.tokens.pop(0)  # Remove 'rec'
            is_rec = True
        self.Db()  # Parse definition body
        if is_rec:
            # Create rec node if it's a recursive definition
            self.ast.append(Node(NodeType.rec, "rec", 1))

    def Db(self):
        """Parse a definition body (Db).
        
        Grammar rule:
        Db -> Vl '=' E => '='
          -> '<IDENTIFIER>' Vb+ '=' E => 'fcn_form'
          -> '(' D ')'
        """
        if self.tokens[0].type == TokenType.PUNCTUATION and self.tokens[0].value == "(":
            # Handle parenthesized definition
            self.tokens.pop(0)  # Remove '('
            self.D()  # Parse inner definition
            if self.tokens[0].value != ")":
                print("Parsing error at Db #1")
            self.tokens.pop(0)  # Remove ')'
        elif self.tokens[0].type == TokenType.IDENTIFIER:
            # Look ahead to determine if this is a function definition
            # We need to check if there are parameters before the '=' sign
            
            i = 1
            param_count = 0
            
            # Count consecutive identifiers (parameters) before '='
            while (i < len(self.tokens) and 
                   (self.tokens[i].type == TokenType.IDENTIFIER or 
                    (self.tokens[i].type == TokenType.PUNCTUATION and self.tokens[i].value == "("))):
                if self.tokens[i].type == TokenType.IDENTIFIER:
                    param_count += 1
                    i += 1
                elif self.tokens[i].value == "(":
                    # Skip balanced parentheses for grouped parameters
                    paren_count = 1
                    i += 1
                    while i < len(self.tokens) and paren_count > 0:
                        if self.tokens[i].value == "(":
                            paren_count += 1
                        elif self.tokens[i].value == ")":
                            paren_count -= 1
                        i += 1
                    param_count += 1
            
            # Check if we found an '=' after the parameters
            has_equals = i < len(self.tokens) and self.tokens[i].value == "="
            
            if param_count > 0 and has_equals:
                # This is a function definition (fcn_form)
                self.ast.append(Node(NodeType.identifier, self.tokens[0].value, 0))
                self.tokens.pop(0)  # Remove function name

                n = 1  # Count children (1 for function name)
                
                # Parse all parameters
                while (self.tokens and 
                       (self.tokens[0].type == TokenType.IDENTIFIER or 
                        (self.tokens[0].type == TokenType.PUNCTUATION and self.tokens[0].value == "("))):
                    self.Vb()  # Parse parameter
                    n += 1
                
                if not self.tokens or self.tokens[0].value != "=":
                    print("Parsing error at Db #2: Expected '=' in function definition")
                    return
                    
                self.tokens.pop(0)  # Remove '='
                self.E()  # Parse function body
                n += 1  # Add one for the body

                # Create fcn_form node
                self.ast.append(Node(NodeType.fcn_form, "fcn_form", n))
                
            elif len(self.tokens) > 1 and self.tokens[1].value == "=":
                # Handle simple variable definition (no parameters)
                self.ast.append(Node(NodeType.identifier, self.tokens[0].value, 0))
                self.tokens.pop(0)  # Remove identifier
                self.tokens.pop(0)  # Remove '='
                self.E()  # Parse expression
                self.ast.append(Node(NodeType.equal, "=", 2))  # Create equals node
                
            elif len(self.tokens) > 1 and self.tokens[1].value == ",":
                # Handle multi-variable definition
                self.Vl()  # Parse variable list
                if not self.tokens or self.tokens[0].value != "=":
                    print("Parsing error at Db: Expected '=' after variable list")
                    return
                self.tokens.pop(0)  # Remove '='
                self.E()  # Parse expression
                self.ast.append(Node(NodeType.equal, "=", 2))  # Create equals node
            else:
                print(f"Parsing error at Db: Unexpected token pattern. Token 1: {self.tokens[0].value}, Token 2: {self.tokens[1].value if len(self.tokens) > 1 else 'EOF'}")
        else:
            print(f"Parsing error at Db: Expected identifier or '(', got {self.tokens[0].type} with value '{self.tokens[0].value}'")

    def Vb(self):
        """Parse a variable binding (Vb).
        
        Grammar rule:
        Vb -> '<IDENTIFIER>'
           -> '(' Vl ')'
           -> '(' ')' => '()'
        """
        if self.tokens[0].type == TokenType.PUNCTUATION and self.tokens[0].value == "(":
            # Handle parenthesized variable binding or empty parameter list
            self.tokens.pop(0)  # Remove '('
            isVl = False  # Flag to track if we found a variable list

            if self.tokens[0].type == TokenType.IDENTIFIER:
                # Parse variable list
                self.Vl()
                isVl = True
            
            if self.tokens[0].value != ")":
                print("Parse error unmatch )")
            self.tokens.pop(0)  # Remove ')'
            
            if not isVl:
                # Empty parameter list
                self.ast.append(Node(NodeType.empty_params, "()", 0))
        elif self.tokens[0].type == TokenType.IDENTIFIER:
            # Handle simple identifier
            self.ast.append(Node(NodeType.identifier, self.tokens[0].value, 0))
            self.tokens.pop(0)  # Remove identifier

    def Vl(self):
        """Parse a variable list (Vl).
        
        Grammar rule:
        Vl -> '<IDENTIFIER>' (',' '<IDENTIFIER>')* => ','?
        """
        n = 0  # Count identifiers
        while True:
            if n > 0:
                if not self.tokens or self.tokens[0].value != ",":
                    break
                self.tokens.pop(0)  # Remove comma
            if not self.tokens or self.tokens[0].type != TokenType.IDENTIFIER:
                if n == 0:  # If we haven't found any identifiers yet
                    print("Parse error: an identifier was expected")
                break
            
            # Add identifier node
            self.ast.append(Node(NodeType.identifier, self.tokens[0].value, 0))
            self.tokens.pop(0)  # Remove identifier
            n += 1
            
            if not self.tokens or self.tokens[0].value != ",":
                break  # No more identifiers
        
        if n > 1:
            # Create comma node if we have multiple identifiers
            self.ast.append(Node(NodeType.comma, ",", n))