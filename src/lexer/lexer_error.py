class LexicalError(Exception):
    def __init__(self, position, character):
        self.position = position
        self.character = character
        super().__init__(f"Invalid token at position {position}: '{character}'")
