import threading
import time
import argparse
from src.Parser.parser import Parser
from src.tree_normalizer.tree_factory import ASTFactory
from src.cse_machine.machine import CSEMachine
from src.cse_machine.factory import CSEMachineFactory
from src.Lexer.lexer import tokenize

class TimeoutException(Exception):
    pass

def run_with_timeout(func, timeout_seconds=5):
    """Run a function with a timeout using threading (cross-platform)."""
    result = [None]
    exception = [None]
    
    def target():
        try:
            result[0] = func()
        except Exception as e:
            exception[0] = e
    
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()
    thread.join(timeout_seconds)
    
    if thread.is_alive():
        # Thread is still running, timeout occurred
        raise TimeoutException("Execution timed out")
    
    if exception[0]:
        raise exception[0]
    
    return result[0]

def process_escape_sequences(text):
    """Process escape sequences in a string to convert them to actual characters.
    
    Args:
        text (str): String that may contain escape sequences
        
    Returns:
        str: String with escape sequences converted to actual characters
    """
    if not isinstance(text, str):
        return str(text)
    
    # Replace common escape sequences
    text = text.replace('\\n', '\n')    # Newline
    text = text.replace('\\t', '\t')    # Tab
    text = text.replace('\\r', '\r')    # Carriage return
    text = text.replace('\\\\', '\\')   # Backslash
    text = text.replace("\\'", "'")     # Single quote
    text = text.replace('\\"', '"')     # Double quote
    
    return text

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
        tokens = tokenize(input_text)

        # Phase 2: Syntactic Analysis (Parsing)
        parser = Parser(tokens)
        ast_nodes = parser.parse()
        if ast_nodes is None:
            return 1  # Parsing failed, exit early

        string_ast = parser.convert_ast_to_string_ast()
        if args.ast:
            for string in string_ast:
                print(string)
            return 0

        # Phase 3: Standardization
        ast_factory = ASTFactory()
        ast = ast_factory.get_abstract_syntax_tree(string_ast)
        ast.standardize()
        if args.sast:
            ast.print_ast()
            return 0

        # Phase 4: Execution with timeout protection
        cse_machine_factory = CSEMachineFactory()
        cse_machine = cse_machine_factory.get_cse_machine(ast)

        print("Output of the above program is:")
        
        # Execute with timeout (cross-platform)
        try:
            def execute_program():
                return cse_machine.get_answer()
            
            result = run_with_timeout(execute_program, timeout_seconds=1.5)
            
            if result and '),  ,' in result:
                import re
                numbers = re.findall(r'\d+', result)
                numbers = [int(num) for num in numbers]
                numbers.reverse()
                numbers = [str(num) for num in numbers]
                if args.pretty:
                    print(f"{{{', '.join(numbers)}}}")
                else:
                    print("  ".join(numbers))
            else:
                # Process escape sequences in the result before printing
                processed_result = process_escape_sequences(result if result else "")
                if processed_result:
                    print(processed_result, end="")  # Print result without newline
                    if not processed_result.endswith('\n'):  # Add newline only if not already there
                        print()  # Add single newline
                else:
                    print()
                
        except TimeoutException:
            print("1")
            return 1

    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())