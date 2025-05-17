from ..lexer.token_types import TokenType
from .ast_node import ASTNode
from .node_types import NodeType, COMPARISON_OPS
from .parser_error import UnexpectedTokenError, SyntaxError, MissingTokenError

class Parser:
    """
    Recursive-descent parser for the RPAL language
    
    This parser follows the RPAL grammar to build an abstract syntax tree (AST)
    from a sequence of tokens provided by the lexer.
    """
    
    def __init__(self, tokens):
        """
        Initialize the parser with a list of tokens
        
        Args:
            tokens (list): List of Token objects from the lexer
        """
        self.tokens = tokens
        self.current_pos = 0
        self.ast_root = None
    
    def parse(self):
        """
        Parse the token stream and build an abstract syntax tree
        
        Returns:
            ASTNode: Root node of the abstract syntax tree
            
        Raises:
            ParserError: If syntax errors are encountered during parsing
        """
        self.ast_root = self.parse_expression()
        
        # Check that we've consumed all tokens
        if not self.is_at_end():
            token = self.peek()
            raise SyntaxError("Unexpected tokens at end of input", 
                              token.line, token.column)
        
        return self.ast_root
    
    # Helper methods for token handling
    
    def is_at_end(self):
        """Check if we've reached the end of the token stream"""
        return self.current_pos >= len(self.tokens) or self.tokens[self.current_pos].type == TokenType.EOF
    
    def peek(self):
        """Return current token without consuming it"""
        if self.is_at_end():
            return None
        return self.tokens[self.current_pos]
    
    def previous(self):
        """Return the previously consumed token"""
        return self.tokens[self.current_pos - 1]
    
    def advance(self):
        """Consume and return the current token"""
        if not self.is_at_end():
            self.current_pos += 1
        return self.previous()
    
    def check(self, token_type=None, token_value=None):
        """
        Check if current token matches the type/value without consuming it
        
        Args:
            token_type: TokenType to check against (optional)
            token_value: Token value to check against (optional)
            
        Returns:
            bool: True if token matches, False otherwise
        """
        if self.is_at_end():
            return False
            
        token = self.peek()
        
        type_match = token_type is None or token.type == token_type
        value_match = token_value is None or token.value == token_value
        
        return type_match and value_match
    
    def match(self, token_type=None, token_value=None):
        """
        Check if current token matches and consume it if it does
        
        Args:
            token_type: TokenType to match (optional)
            token_value: Token value to match (optional)
            
        Returns:
            bool: True if token matched and was consumed, False otherwise
        """
        if self.check(token_type, token_value):
            self.advance()
            return True
        return False
    
    def consume(self, token_type=None, token_value=None, error_message=None):
        """
        Consume current token if it matches or raise an error
        
        Args:
            token_type: Expected TokenType (optional)
            token_value: Expected token value (optional)
            error_message: Custom error message (optional)
            
        Returns:
            Token: The consumed token
            
        Raises:
            UnexpectedTokenError: If token doesn't match expectations
        """
        if self.check(token_type, token_value):
            return self.advance()
        
        token = self.peek()
        
        if error_message is None:
            expected = token_type.name if token_type else f"'{token_value}'"
            error_message = f"Expected {expected}"
        
        raise UnexpectedTokenError(
            error_message, 
            f"{token.type.name}('{token.value}')" if token else "EOF",
            token.line if token else None, 
            token.column if token else None
        )
    
    # Recursive descent parsing methods following RPAL grammar
    
    def parse_expression(self):
        """
        Parse an expression (E in the grammar)
        
        E -> 'let' D 'in' E => 'let'
          -> 'fn' Vb+ '.' E => 'lambda'
          -> Ew
        """
        # Check for 'let' expression
        if self.match(token_value="let"):
            let_token = self.previous()
            definition = self.parse_definition()
            
            self.consume(token_value="in", error_message="Expected 'in' after definition in let-expression")
            body = self.parse_expression()
            
            # Create LET node
            let_node = ASTNode(NodeType.LET, "let", let_token.line, let_token.column)
            let_node.add_child(definition)
            let_node.add_child(body)
            return let_node
        
        # Check for function expression
        elif self.match(token_value="fn"):
            fn_token = self.previous()
            params = []
            
            # Parse one or more variable bindings
            first_vb = self.parse_variable_binding()
            params.append(first_vb)
            
            while not self.check(token_value="."):
                params.append(self.parse_variable_binding())
            
            # Consume the dot
            self.consume(token_value=".", error_message="Expected '.' after parameters in function expression")
            
            # Parse the function body
            body = self.parse_expression()
            
            # Create lambda node
            lambda_node = ASTNode(NodeType.LAMBDA, "lambda", fn_token.line, fn_token.column)
            for param in params:
                lambda_node.add_child(param)
            lambda_node.add_child(body)
            return lambda_node
        
        # Otherwise parse where expression
        else:
            return self.parse_where_expression()
    
    def parse_where_expression(self):
        """
        Parse a where expression (Ew in the grammar)
        
        Ew -> T 'where' Dr => 'where'
           -> T
        """
        term = self.parse_tuple_expression()
        
        if self.match(token_value="where"):
            where_token = self.previous()
            definition = self.parse_rec_definition()
            
            # Create WHERE node
            where_node = ASTNode(NodeType.WHERE, "where", where_token.line, where_token.column)
            where_node.add_child(term)
            where_node.add_child(definition)
            return where_node
        
        return term
    
    def parse_tuple_expression(self):
        """
        Parse a tuple expression (T in the grammar)
        
        T -> Ta (',' Ta)+ => 'tau'
          -> Ta
        """
        terms = [self.parse_augmented_expression()]
        
        # Check for comma-separated terms
        while self.match(token_value=","):
            terms.append(self.parse_augmented_expression())
        
        # If we found a tuple, create a TAU node
        if len(terms) > 1:
            tau_node = ASTNode(NodeType.TAU, "tau", terms[0].line, terms[0].column)
            tau_node.add_children(terms)
            return tau_node
        
        # Otherwise return the single term
        return terms[0]
    
    def parse_augmented_expression(self):
        """
        Parse an augmented expression (Ta in the grammar)
        
        Ta -> Tc ('aug' Tc)* => 'aug'
        """
        left = self.parse_conditional_expression()
        
        # Check for augmentation
        while self.match(token_value="aug"):
            aug_token = self.previous()
            right = self.parse_conditional_expression()
            
            # Create AUG node
            aug_node = ASTNode(NodeType.AUG, "aug", aug_token.line, aug_token.column)
            aug_node.add_child(left)
            aug_node.add_child(right)
            left = aug_node
        
        return left
    
    def parse_conditional_expression(self):
        """
        Parse a conditional expression (Tc in the grammar)
        
        Tc -> B '->' Tc '|' Tc => '->'
           -> B
        """
        condition = self.parse_boolean_expression()
        
        # Check for conditional operator
        if self.match(token_value="->"):
            arrow_token = self.previous()
            true_branch = self.parse_conditional_expression()
            
            self.consume(token_value="|", error_message="Expected '|' in conditional expression")
            
            false_branch = self.parse_conditional_expression()
            
            # Create CONDITIONAL node
            cond_node = ASTNode(
                NodeType.CONDITIONAL, "->", arrow_token.line, arrow_token.column
            )
            cond_node.add_child(condition)
            cond_node.add_child(true_branch)
            cond_node.add_child(false_branch)
            return cond_node
        
        return condition
    
    def parse_boolean_expression(self):
        """
        Parse a boolean expression (B in the grammar)
        
        B -> Bt ('or' Bt)* => 'or'
        """
        left = self.parse_boolean_term()
        
        # Check for OR operators
        while self.match(token_value="or"):
            or_token = self.previous()
            right = self.parse_boolean_term()
            
            # Create OR node
            or_node = ASTNode(NodeType.OR, "or", or_token.line, or_token.column)
            or_node.add_child(left)
            or_node.add_child(right)
            left = or_node
        
        return left
    
    def parse_boolean_term(self):
        """
        Parse a boolean term (Bt in the grammar)
        
        Bt -> Bs ('&' Bs)* => '&'
        """
        left = self.parse_boolean_factor()
        
        # Check for AND operators
        while self.match(token_value="&"):
            and_token = self.previous()
            right = self.parse_boolean_factor()
            
            # Create AND_OP node
            and_node = ASTNode(NodeType.AND_OP, "&", and_token.line, and_token.column)
            and_node.add_child(left)
            and_node.add_child(right)
            left = and_node
        
        return left
    
    def parse_boolean_factor(self):
        """
        Parse a boolean factor (Bs in the grammar)
        
        Bs -> 'not' Bp => 'not'
           -> Bp
        """
        if self.match(token_value="not"):
            not_token = self.previous()
            expr = self.parse_boolean_primary()
            
            # Create NOT node
            not_node = ASTNode(NodeType.NOT, "not", not_token.line, not_token.column)
            not_node.add_child(expr)
            return not_node
        
        return self.parse_boolean_primary()
    
    def parse_boolean_primary(self):
        """
        Parse a boolean primary (Bp in the grammar)
        
        Bp -> A ('gr'|'>'|'ge'|'>='|'ls'|'<'|'le'|'<='|'eq'|'ne') A
           -> A
        """
        left = self.parse_arithmetic_expression()
        
        # Check for comparison operators
        comp_ops = ['gr', '>', 'ge', '>=', 'ls', '<', 'le', '<=', 'eq', 'ne']
        for op in comp_ops:
            if self.match(token_value=op):
                op_token = self.previous()
                right = self.parse_arithmetic_expression()
                
                # Map the operator to its node type
                node_type = COMPARISON_OPS.get(op)
                
                # Create comparison node
                comp_node = ASTNode(node_type, op, op_token.line, op_token.column)
                comp_node.add_child(left)
                comp_node.add_child(right)
                return comp_node
        
        return left
    
    def parse_arithmetic_expression(self):
        """
        Parse an arithmetic expression (A in the grammar)
        
        A -> '+' At
          -> '-' At => 'neg'
          -> At ('+' At)* => '+'
          -> At ('-' At)* => '-'
        """
        # Handle unary plus
        if self.match(token_value="+"):
            # Unary plus just returns the term
            return self.parse_arithmetic_term()
        
        # Handle unary minus (negation)
        elif self.match(token_value="-"):
            neg_token = self.previous()
            term = self.parse_arithmetic_term()
            
            # Create NEGATE node
            neg_node = ASTNode(NodeType.NEGATE, "neg", neg_token.line, neg_token.column)
            neg_node.add_child(term)
            return neg_node
        
        # Handle regular additive expressions
        left = self.parse_arithmetic_term()
        
        while True:
            if self.match(token_value="+"):
                op_token = self.previous()
                right = self.parse_arithmetic_term()
                
                # Create PLUS node
                plus_node = ASTNode(NodeType.PLUS, "+", op_token.line, op_token.column)
                plus_node.add_child(left)
                plus_node.add_child(right)
                left = plus_node
                
            elif self.match(token_value="-"):
                op_token = self.previous()
                right = self.parse_arithmetic_term()
                
                # Create MINUS node
                minus_node = ASTNode(NodeType.MINUS, "-", op_token.line, op_token.column)
                minus_node.add_child(left)
                minus_node.add_child(right)
                left = minus_node
                
            else:
                break
        
        return left
    
    def parse_arithmetic_term(self):
        """
        Parse an arithmetic term (At in the grammar)
        
        At -> Af ('*' Af)* => '*'
           -> Af ('/' Af)* => '/'
        """
        left = self.parse_arithmetic_factor()
        
        while True:
            if self.match(token_value="*"):
                op_token = self.previous()
                right = self.parse_arithmetic_factor()
                
                # Create TIMES node
                times_node = ASTNode(NodeType.TIMES, "*", op_token.line, op_token.column)
                times_node.add_child(left)
                times_node.add_child(right)
                left = times_node
                
            elif self.match(token_value="/"):
                op_token = self.previous()
                right = self.parse_arithmetic_factor()
                
                # Create DIVIDE node
                div_node = ASTNode(NodeType.DIVIDE, "/", op_token.line, op_token.column)
                div_node.add_child(left)
                div_node.add_child(right)
                left = div_node
                
            else:
                break
        
        return left
    
    def parse_arithmetic_factor(self):
        """
        Parse an arithmetic factor (Af in the grammar)
        
        Af -> Ap ('**' Af)* => '**'
        """
        left = self.parse_atom_with_primaries()
        
        if self.match(token_value="**"):
            op_token = self.previous()
            right = self.parse_arithmetic_factor()  # Notice the recursion to handle right-associativity
            
            # Create POWER node
            pow_node = ASTNode(NodeType.POWER, "**", op_token.line, op_token.column)
            pow_node.add_child(left)
            pow_node.add_child(right)
            return pow_node
        
        return left
    
    def parse_atom_with_primaries(self):
        """
        Parse an atom with primaries (Ap in the grammar)
        
        Ap -> R ('@' <IDENTIFIER> R)* => '@'
        """
        left = self.parse_rator_rand()
        
        while self.match(token_value="@"):
            at_token = self.previous()
            
            # Expect an identifier
            self.consume(TokenType.IDENTIFIER, error_message="Expected identifier after '@'")
            id_token = self.previous()
            id_node = ASTNode(NodeType.IDENTIFIER, id_token.value, 
                             id_token.line, id_token.column)
            
            right = self.parse_rator_rand()
            
            # Create AT node
            at_node = ASTNode(NodeType.AT, "@", at_token.line, at_token.column)
            at_node.add_child(left)
            at_node.add_child(id_node)
            at_node.add_child(right)
            left = at_node
        
        return left
    
    def parse_rator_rand(self):
        """
        Parse a rator-rand expression (R in the grammar)
        
        R -> Rn (Rn)* => 'gamma'
        """
        left = self.parse_rand()
        
        # This is a bit different from other rules - we need to check if the next token
        # could start a Rn. This requires lookahead.
        while (self.check(TokenType.IDENTIFIER) or 
               self.check(TokenType.INTEGER) or 
               self.check(TokenType.STRING) or 
               self.check(token_value="(") or
               self.check(token_value="true") or
               self.check(token_value="false") or
               self.check(token_value="nil") or
               self.check(token_value="dummy")):
            
            right = self.parse_rand()
            
            # Create GAMMA node (function application)
            gamma_node = ASTNode(NodeType.GAMMA, "gamma", left.line, left.column)
            gamma_node.add_child(left)
            gamma_node.add_child(right)
            left = gamma_node
        
        return left
    
    def parse_rand(self):
        """
        Parse a rand expression (Rn in the grammar)
        
        Rn -> <IDENTIFIER>
           -> <INTEGER>
           -> <STRING>
           -> 'true' => 'true'
           -> 'false' => 'false'
           -> 'nil' => 'nil'
           -> '(' E ')'
           -> 'dummy' => 'dummy'
        """
        # Handle identifiers
        if self.match(TokenType.IDENTIFIER):
            token = self.previous()
            return ASTNode(NodeType.IDENTIFIER, token.value, token.line, token.column)
        
        # Handle integers
        elif self.match(TokenType.INTEGER):
            token = self.previous()
            return ASTNode(NodeType.INTEGER, token.value, token.line, token.column)
        
        # Handle strings
        elif self.match(TokenType.STRING):
            token = self.previous()
            return ASTNode(NodeType.STRING, token.value, token.line, token.column)
        
        # Handle true
        elif self.match(token_value="true"):
            token = self.previous()
            return ASTNode(NodeType.TRUE, "true", token.line, token.column)
        
        # Handle false
        elif self.match(token_value="false"):
            token = self.previous()
            return ASTNode(NodeType.FALSE, "false", token.line, token.column)
        
        # Handle nil
        elif self.match(token_value="nil"):
            token = self.previous()
            return ASTNode(NodeType.NIL, "nil", token.line, token.column)
        
        # Handle dummy
        elif self.match(token_value="dummy"):
            token = self.previous()
            return ASTNode(NodeType.DUMMY, "dummy", token.line, token.column)
        
        # Handle parenthesized expressions
        elif self.match(token_value="("):
            open_token = self.previous()
            expr = self.parse_expression()
            self.consume(token_value=")", error_message="Expected ')' after expression")
            return expr
        
        # Error if none of the above
        else:
            token = self.peek()
            raise SyntaxError("Expected a rand expression", 
                             token.line if token else None, 
                             token.column if token else None)
    
    def parse_definition(self):
        """
        Parse a definition (D in the grammar)
        
        D -> Da 'within' D => 'within'
          -> Da
        """
        left = self.parse_and_definition()
        
        if self.match(token_value="within"):
            within_token = self.previous()
            right = self.parse_definition()
            
            # Create WITHIN node
            within_node = ASTNode(NodeType.WITHIN, "within", within_token.line, within_token.column)
            within_node.add_child(left)
            within_node.add_child(right)
            return within_node
        
        return left
    
    def parse_and_definition(self):
        """
        Parse an and-definition (Da in the grammar)
        
        Da -> Dr ('and' Dr)+ => 'and'
           -> Dr
        """
        defs = [self.parse_rec_definition()]
        
        while self.match(token_value="and"):
            defs.append(self.parse_rec_definition())
        
        if len(defs) > 1:
            # Create AND node for multiple definitions
            and_node = ASTNode(NodeType.AND, "and", defs[0].line, defs[0].column)
            and_node.add_children(defs)
            return and_node
        
        return defs[0]
    
    def parse_rec_definition(self):
        """
        Parse a recursive definition (Dr in the grammar)
        
        Dr -> 'rec' Db => 'rec'
           -> Db
        """
        if self.match(token_value="rec"):
            rec_token = self.previous()
            db = self.parse_basic_definition()
            
            # Create REC node
            rec_node = ASTNode(NodeType.REC, "rec", rec_token.line, rec_token.column)
            rec_node.add_child(db)
            return rec_node
        
        return self.parse_basic_definition()
    
    def parse_basic_definition(self):
        """
        Parse a basic definition (Db in the grammar)
        
        Db -> Vl '=' E => '='
           -> <IDENTIFIER> Vb+ '=' E => 'fcn_form'
           -> '(' D ')'
        """
        # Handle parenthesized definition
        if self.match(token_value="("):
            def_node = self.parse_definition()
            self.consume(token_value=")", error_message="Expected ')' after definition")
            return def_node
        
        # Handle identifier cases
        elif self.check(TokenType.IDENTIFIER):
            # Try to parse as function form first (lookahead required)
            saved_pos = self.current_pos
            id_token = self.advance()
            id_node = ASTNode(NodeType.IDENTIFIER, id_token.value, 
                             id_token.line, id_token.column)
            
            # Check if we have parameters
            if (self.check(TokenType.IDENTIFIER) or self.check(token_value="(")):
                # We have a function form
                params = [id_node]
                
                # Parse parameters
                while (self.check(TokenType.IDENTIFIER) or self.check(token_value="(")):
                    params.append(self.parse_variable_binding())
                
                # Expect equals sign
                self.consume(token_value="=", error_message="Expected '=' in function definition")
                
                # Parse body expression
                body = self.parse_expression()
                
                # Create FCN_FORM node
                fcn_node = ASTNode(NodeType.FCN_FORM, "fcn_form", id_token.line, id_token.column)
                fcn_node.add_children(params)
                fcn_node.add_child(body)
                return fcn_node
            else:
                # If not a function form, reset position and try variable list
                self.current_pos = saved_pos
                
                # Parse variable list
                vars_node = self.parse_variable_list()
                
                # Expect equals sign
                self.consume(token_value="=", error_message="Expected '=' in definition")
                
                # Parse expression
                expr = self.parse_expression()
                
                # Create EQUAL node
                equal_node = ASTNode(NodeType.EQUAL, "=", vars_node.line, vars_node.column)
                equal_node.add_child(vars_node)
                equal_node.add_child(expr)
                return equal_node
        
        # Error if no definition found
        else:
            token = self.peek()
            raise SyntaxError("Expected a definition", 
                             token.line if token else None, 
                             token.column if token else None)
    
    def parse_variable_binding(self):
        """
        Parse a variable binding (Vb in the grammar)
        
        Vb -> <IDENTIFIER>
           -> '(' Vl ')'
           -> '(' ')' => '()'
        """
        # Handle identifiers
        if self.match(TokenType.IDENTIFIER):
            token = self.previous()
            return ASTNode(NodeType.IDENTIFIER, token.value, token.line, token.column)
        
        # Handle parenthesized case
        elif self.match(token_value="("):
            if self.match(token_value=")"):
                # Empty parameter list
                token = self.previous()
                return ASTNode(NodeType.EMPTY, "()", token.line, token.column)
            else:
                # Variable list
                vl = self.parse_variable_list()
                self.consume(token_value=")", error_message="Expected ')' after variable list")
                return vl
        else:
            token = self.peek()
            raise SyntaxError("Expected a variable binding", 
                             token.line if token else None, 
                             token.column if token else None)
    
    def parse_variable_list(self):
        """
        Parse a variable list (Vl in the grammar)
        
        Vl -> <IDENTIFIER> (',' <IDENTIFIER>)* => ','?
        """
        # First identifier
        self.consume(TokenType.IDENTIFIER, error_message="Expected an identifier")
        first_token = self.previous()
        ids = [ASTNode(NodeType.IDENTIFIER, first_token.value, 
                      first_token.line, first_token.column)]
        
        # Additional identifiers
        while self.match(token_value=","):
            self.consume(TokenType.IDENTIFIER, error_message="Expected an identifier after ','")
            token = self.previous()
            ids.append(ASTNode(NodeType.IDENTIFIER, token.value, token.line, token.column))
        
        if len(ids) > 1:
            # Create COMMA node for multiple identifiers
            comma_node = ASTNode(NodeType.COMMA, ",", first_token.line, first_token.column)
            comma_node.add_children(ids)
            return comma_node
        
        return ids[0]