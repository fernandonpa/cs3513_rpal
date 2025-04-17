# cs3513_rpal

A Python‑based compiler toolchain for the RPAL (Right‑reference Parallel Applicative Language) programming language. This project includes a handwritten **lexer**, **parser**, **AST→ST normalizer**, and **CSE machine** evaluator.

---

## 📄 Project Description

This repository provides an end‑to‑end implementation of an RPAL compiler in Python, without using external parser/lexer generators. It supports:

- **Lexical analysis**: tokenizes RPAL source.
- **Parsing**: constructs an Abstract Syntax Tree (AST).
- **Standardization**: transforms AST into a standardized tree (ST).
- **Evaluation**: runs the ST on a CSE abstract machine to produce results.

Use the `-ast` flag to print only the AST; otherwise, the result of evaluating the program will be printed.

---

## ⚙️ Setup Environment

1. **Clone the repository**

   ```bash
   git clone <your‑repo‑url> cs3513_rpal
   cd cs3513_rpal
   ```

2. **Create a virtual environment** (using built‑in venv):

   ```bash
   python3 -m venv .venv
   // or after install pip virtualenv
   //virtualenv .venv
   ```

3. **Activate the environment**

   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
   - On Windows (PowerShell):
     ```powershell
     .\.venv\Scripts\Activate.ps1
        or .\.venv\Scripts\activate
     ```

4. **Install development dependencies**

   ```bash
   pip install -r requirements-dev.txt
   ```

5. **Install project dependencies** (if you separate `requirements.txt`):

   ```bash
   pip install -r requirements.txt
   ```

---

## 📂 Project Structure

````text
cs3513_rpal/
├── src/
│   ├── lexer/                         # Tokenizer implementation
│   │   └── __init__.py                # Package init
│   │   └── lexer.py and others        # Lexer class and token definitions
│   ├── parser/                        # Recursive‑descent parser
│   │   └── __init__.py                # Package init
│   │   └── parser.py and others       # Parser class and AST builders
│   ├── normalizer/                    # AST → Standardized Tree (ST)
│   │   └── __init__.py                # Package init
│   │   └── st.py and others           # Normalization logic
│   ├── cse_machine/                   # CSE abstract machine evaluator
│   │   └── __init__.py                # Package init
│   │   └── cse_machine.py and others  # Machine implementation
│   └── myrpal.py                      # Entry point / CLI wrapper
├── tests/                             # Unit tests (pytest)
│   ├── test_lexer.py
│   ├── test_parser.py
│   ├── test_ast_st.py
│   └── test_cse_machine.py
├── examples/            # Sample RPAL programs
├── Makefile             # Build/test/run tasks
├── README.md
├── .gitignore
├── reports/
├── requirements.txt
└── docs/

---

## 🚀 Getting Started

- **Run a sample RPAL program**:

  ```bash
  make run FILE=examples/sample.rpl
````

- **Print the AST**:

  ```bash
  make ast FILE=examples/sample.rpl
  ```

- **Run all tests**:

  ```bash
  make test
  ```

- **Clean build artifacts**:

  ```bash
  make clean
  ```

---

> _This is an initial README. More details—such as detailed usage, contribution guidelines, and examples—will be added as the project evolves._
