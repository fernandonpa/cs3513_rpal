import re
from .token_types import TokenType
from .token import Token
from .lexer_error import LexicalError

class Tokenizer:
    def __init__(self):
        self.token_patterns = [
            (TokenType.KEYWORD, re.compile(r"\b(let|in|fn|where|aug|or|not|gr|ge|ls|le|eq|ne|true|false|nil|dummy|within|and|rec)\b")),
            (TokenType.STRING, re.compile(r"'(?:\\'|[^'])*'")),
            (TokenType.IDENTIFIER, re.compile(r"[a-zA-Z][a-zA-Z0-9_]*")),
            (TokenType.INTEGER, re.compile(r"\d+")),
            (TokenType.OPERATOR, re.compile(r"[+\-*<>&.@/:=~|$!#%^_\[\]{}\"'?]+")),
            (TokenType.PUNCTUATION, re.compile(r"[();,]")),
        ]
        self.comment_pattern = re.compile(r"//.*")
        self.whitespace_pattern = re.compile(r"\s+")

    def tokenize(self, text):
        tokens = []
        position = 0

        while position < len(text):
            # Skip whitespace
            whitespace = self.whitespace_pattern.match(text, position)
            if whitespace:
                position = whitespace.end()
                continue

            # Skip comments
            comment = self.comment_pattern.match(text, position)
            if comment:
                position = comment.end()
                continue

            matched = False
            for token_type, pattern in self.token_patterns:
                match = pattern.match(text, position)
                if match:
                    value = match.group()
                    tokens.append(Token(token_type, value))
                    position = match.end()
                    matched = True
                    break

            if not matched:
                raise LexicalError(position, text[position])

        tokens.append(Token(TokenType.END_OF_TOKENS, "EOF"))
        return tokens
