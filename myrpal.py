
import argparse
from src.Parser.parser import Parser
from src.tree_normalizer.tree_factory import ASTFactory
from src.cse_machine.machine import CSEMachine
from src.cse_machine.factory import CSEMachineFactory
from src.Lexer.lexer import tokenize

def main():
    """
    Main function to process RPAL files.

    Command-line Arguments:
        file_name (str): The RPAL program input file.
        -ast: Print the abstract syntax tree (AST).
        -sast: Print the standardized abstract syntax tree (SAST).

    Raises:
        Exception: If any error occurs during processing.
    """
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Process some RPAL files.')
    parser.add_argument('file_name', type=str, help='The RPAL program input file')
    parser.add_argument('-ast', action='store_true', help='Print the abstract syntax tree')
    parser.add_argument('-sast', action='store_true', help='Print the standardized abstract syntax tree')
    parser.add_argument('-pretty', action='store_true', help='Format tuple output as a clean list')

    args = parser.parse_args()

    # Read the input file
    with open(args.file_name, "r") as input_file:
        input_text = input_file.read()

    try:
        # Phase 1: Lexical Analysis (Tokenization)
        # Convert the input text into a stream of tokens
        tokens = tokenize(input_text)

        # Phase 2: Syntactic Analysis (Parsing)
        # Parse the tokens into an Abstract Syntax Tree (AST)
        parser = Parser(tokens)
        ast_nodes = parser.parse()
        if ast_nodes is None:
            return  # Parsing failed, exit early

        # Convert internal AST representation to string format
        string_ast = parser.convert_ast_to_string_ast()
        if args.ast:
            # If -ast flag is provided, print the AST and exit
            for string in string_ast:
                print(string)
            return

        # Phase 3: Standardization
        # Convert the string AST to a standardized AST
        # (Standardization transforms the AST into a form suitable for execution)
        ast_factory = ASTFactory()
        ast = ast_factory.get_abstract_syntax_tree(string_ast)
        ast.standardize()
        if args.sast:
            # If -sast flag is provided, print the standardized AST and exit
            ast.print_ast()
            return

        # Phase 4: Execution
        # Create a CSE Machine and execute the standardized AST
        cse_machine_factory = CSEMachineFactory()
        cse_machine = cse_machine_factory.get_cse_machine(ast)

        # Default action: execute the program and print its output
        print("Output of the above program is:")
        result = cse_machine.get_answer()

        if args.pretty and '(' in result:
            # Extract all numbers from the tuple structure
            import re
            numbers = re.findall(r'\d+', result)
            
            # Convert to integers and sort in ascending order
            numbers = [int(num) for num in numbers]
            numbers.sort()  # Sort in ascending order
            
            # Convert back to strings for joining
            numbers = [str(num) for num in numbers]
            print(", ".join(numbers))
        else:
            print(result)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()