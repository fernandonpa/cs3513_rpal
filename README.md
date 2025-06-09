# RPAL Language Compiler

A Python-based compiler toolchain for the RPAL (Right-reference Parallel Applicative Language) programming language. This project includes a handwritten **lexer**, **parser**, **AST→ST normalizer**, and **CSE machine** evaluator.

## 📄 Project Description

This repository provides an end-to-end implementation of an RPAL compiler in Python, without using external parser/lexer generators. It supports:

- **Lexical analysis**: Tokenizes RPAL source code into a stream of tokens
- **Parsing**: Constructs an Abstract Syntax Tree (AST) using recursive descent parsing
- **Standardization**: Transforms the AST into a standardized tree (ST) for execution
- **Evaluation**: Runs the ST on a CSE (Control-Stack-Environment) abstract machine

## ⚙️ Setup Environment

1. **Clone the repository**

   ```bash
   git clone <your-repo-url> cs3513_rpal
   cd cs3513_rpal
   ```

2. **Create a virtual environment**

   ```bash
   # On Windows
   python -m venv .venv

   # On macOS/Linux
   python3 -m venv .venv
   ```

3. **Activate the environment**

   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
   - On Windows (Command Prompt):
     ```cmd
     .\.venv\Scripts\activate
     ```
   - On Windows (PowerShell):
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

### Using Command Line Interface

Run your RPAL programs using the following commands:

```bash
# Execute an RPAL program
python myrpal.py examples/program.txt

# Print the abstract syntax tree (AST)
python myrpal.py examples/program.txt -ast

# Print the standardized abstract syntax tree (ST)
python myrpal.py examples/program.txt -sast

# Format output tuples as clean, sorted lists
python myrpal.py examples/program.txt -pretty

```

### Using Makefile

The project includes a Makefile that simplifies common tasks:

```bash

# Execute an RPAL program
make run file=examples/program.txt

# Print the abstract syntax tree
make ast file=examples/program.txt

# Print the standardized abstract syntax tree
make sast file=examples/program.txt

# Format output in a pretty, comma separated manner
make pretty file=examples/program.txt

# Clean build artifacts
make clean

# Display help information
make help

```

### Using Windows Subsystem for Linux (WSL)

If you're using Windows, you can use WSL for a Linux-like experience:

1. Navigate to your project directory:

   ```
   cd /mnt/c/Users/your-username/path/to/cs3513_rpal
   ```

2. Use the make commands as shown above.

## 📂 Project Structure

```text

cs3513_rpal/
├── src/
│   ├── Lexer/                         # Tokenizer implementation
│   │   ├── __init__.py
│   │   ├── lexer.py                   # Main lexer logic
│   │   ├── token.py                   # Token class definition
│   │   ├── token_error.py
│   │   └── token_types.py             # Token type definitions
│   ├── Parser/                        # Recursive-descent parser
│   │   ├── __init__.py
│   │   ├── ast_node.py                # AST node implementation
│   │   ├── node_types.py              # Node type definitions
│   │   ├── parser_error.py
│   │   └── parser.py                  # Parser implementation
│   ├── tree_normalizer/               # AST → Standardized Tree (ST)
│   │   ├── __init__.py
│   │   ├── normalizer.py              # Tree standardization logic
│   │   ├── syntax_node.py             # Syntax node definitions
│   │   ├── normalizer_error.py
│   │   ├── tree_builder.py
│   │   └── tree_factory.py            # Factory for tree creation
│   ├── cse_machine/                   # CSE abstract machine evaluator
│   │   ├── __init__.py
│   │   ├── factory.py                 # Factory for CSE machine creation
│   │   ├── error_handler.py
│   │   ├── machine.py                 # CSE machine implementation
│   │   └── nodes/                     # Node types for CSE machine
├── examples/                          # Sample RPAL programs
├── myrpal.py                          # Entry point CLI wrapper
├── Makefile                           # Build/run tasks
└── README.md                          # Project documentation

```

## 🧪 Sample Programs

The examples directory contains several RPAL programs that demonstrate the language features:

- **Q1.txt**: Simple arithmetic operations
- **Q3.txt**: Fibonacci sequence generator
- And more...

## 🔍 Output Formats

The compiler supports various output formats:

- **Default**: Raw execution result
- **Pretty (-pretty)**: Formatted output - especially useful for numeric sequences and tuples

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request with improvements or bug fixes.

## 📝 License

This project is open-source and available under the MIT License.

## 📚 RPAL Language Resources

For more information about the RPAL language syntax and semantics, consult the following resources:

- [RPAL Language Reference](https://rpal-compiler.com) (placeholder)
- [CS3513 Programming Languages Course Materials](https://cs3513.com) (placeholder)

---

> This project was developed as part of the CS3513 Programming Languages course.
