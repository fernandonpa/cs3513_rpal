"""
Manual testing script for the RPAL parser.

This script allows you to test the parser with specific RPAL expressions
and view the resulting AST.
"""
import sys
import os
import argparse

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lexer.tokenizer import Tokenizer
from src.parser.parser import parse_tokens_to_ast


def parse_and_display(source_code: str, show_tokens: bool = False):
    """
    Parse a source code string and display the resulting AST.
    
    Args:
        source_code: The RPAL source code to parse
        show_tokens: Whether to display tokens before parsing
    """
    print(f"Input: {source_code}")
    print("-" * 50)
    
    tokenizer = Tokenizer(source_code)
    tokens = tokenizer.tokenize()
    
    if show_tokens:
        print("Tokens:")
        for token in tokens[:-1]:  # Skip EOF
            print(f"  {token}")
        print("-" * 50)
    
    try:
        ast, string_ast = parse_tokens_to_ast(tokens[:-1])  # Exclude EOF token
        
        print("AST:")
        for line in string_ast:
            print(f"  {line}")
        
        print("-" * 50)
        print("Parsing successful!")
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Main function to run the manual parser test."""
    parser = argparse.ArgumentParser(description="Test the RPAL parser")
    parser.add_argument("--show-tokens", action="store_true", help="Show tokens before parsing")
    args = parser.parse_args()
    
    test_cases = [
        "42",
        "x",
        "'hello world'",
        "1 + 2 * 3",
        "(1 + 2) * 3",
        "-5",
        "true or false & true",
        "let x = 5 in x + 1",
        "fn x . x + 1",
        "1, 2, 3",
        "x + y where x = 1 and y = 2",
        "true -> 1 | 2",
        "f 1 2",
        "list @ index 5",
        "let f () = 42 in f ()",
        "let x, y = 1, 2 in x + y",
        "let f x y = x + y in f 1 2",
        "let rec f n = n eq 0 -> 1 | n * f(n-1) in f 5",
        "let double x = x + x in let map = rec m f l. l eq nil -> nil | f(hd l) aug (m f (tl l)) in map double (1 aug (2 aug nil))",
    ]
    
    for i, test in enumerate(test_cases):
        print(f"\nTest Case {i + 1}:")
        parse_and_display(test, args.show_tokens)
        print("\n")


if __name__ == "__main__":
    main()