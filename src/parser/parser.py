from src.lexer.tokenizer import Tokenizer
from src.lexer.token_types import TokenType

class ASTNode:
    def __init__(self, type_, value=None, children=None):
        self.type = type_
        self.value = value
        self.children = children or []

    def _label(self):
        if self.type == 'let_in':
            return "let"
        if self.type == 'defn':
            return ".="
        if self.type == 'addop':
            return ".+"
        if self.type == 'mulop':
            return ".*"
        if self.type == 'fn':
            return "lambda"
        if self.type == 'varlist':
            return "vars"
        if self.type == 'arrow':
            return "->"
        if self.type == 'identifier':
            return f"<IDENTIFIER:{self.value}>"
        if self.type == 'integer':
            return f"<INTEGER:{self.value}>"
        return self.type

    def to_list(self):
        if self.type in ('identifier', 'integer'):
            return [f"<{self.type.upper()}:{self.value}>"]
        label = self._label()
        result = [label]
        for child in self.children:
            if isinstance(child, ASTNode):
                child_list = child.to_list()
                if isinstance(child_list, list) and len(child_list) == 1:
                    result.append(f"..{child_list[0]}")
                else:
                    result.extend(child_list)
            else:
                result.append(child)
        return result

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, source_code):
        self.tokens = Tokenizer(source_code).tokenize()
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.pos += 1
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
            else:
                self.current_token = None
        else:
            raise ParserError(f"Expected {token_type}, got {self.current_token.type}")

    def parse(self):
        return self.expr()

    def expr(self):
        if self.current_token.type == TokenType.LET:
            self.eat(TokenType.LET)
            defn = self.defn()
            self.eat(TokenType.IN)
            expr = self.expr()
            return ASTNode('let_in', children=[defn, expr])
        elif self.current_token.type == TokenType.FN:
            self.eat(TokenType.FN)
            varlist = self.varlist()
            self.eat(TokenType.ARROW)
            expr = self.expr()
            arrow_node = ASTNode('arrow', children=[expr])
            return ASTNode('fn', children=[varlist, arrow_node])
        else:
            return self.expr_add()

    def defn(self):
        id_token = self.current_token
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.EQUALS)
        expr = self.expr()
        return ASTNode('defn', children=[
            ASTNode('identifier', value=id_token.value),
            expr
        ])

    def varlist(self):
        vars_ = []
        while self.current_token and self.current_token.type == TokenType.IDENTIFIER:
            vars_.append(ASTNode('identifier', value=self.current_token.value))
            self.eat(TokenType.IDENTIFIER)
        return ASTNode('varlist', children=vars_)

    def expr_add(self):
        node = self.expr_atom()
        while self.current_token and self.current_token.type == TokenType.PLUS:
            self.eat(TokenType.PLUS)
            right = self.expr_atom()
            node = ASTNode('addop', children=[node, right])
        return node

    def expr_atom(self):
        tok = self.current_token
        if tok.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return ASTNode('integer', value=tok.value)
        elif tok.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            return ASTNode('identifier', value=tok.value)
        elif tok.type == TokenType.LEFT_PAREN:
            self.eat(TokenType.LEFT_PAREN)
            node = self.expr()
            self.eat(TokenType.RIGHT_PAREN)
            return node
        else:
            raise ParserError(f"Unexpected token: {tok}")