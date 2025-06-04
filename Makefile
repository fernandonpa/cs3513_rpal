# Auto-detect the Python command based on the OS
ifeq ($(OS),Windows_NT)
	PYTHON = python
	RM = del /s /q
else
	PYTHON = python3
	RM = rm -rf
endif

# Set default goal
.DEFAULT_GOAL := help

# Check if file parameter is provided
check_file:
ifndef file
	$(error file parameter is required. Usage: make [target] file=path/to/file.txt)
endif

# Default target: runs the RPAL processor with the specified file
run: check_file
	$(PYTHON) myrpal.py $(file)

# Target to print the AST
ast: check_file
	$(PYTHON) myrpal.py $(file) -ast

# Target to print the standardized AST
sast: check_file
	$(PYTHON) myrpal.py $(file) -sast

# Target to produce pretty-formatted output
pretty: check_file
	$(PYTHON) myrpal.py $(file) -pretty

# Target to clean generated files
clean:
	$(RM) __pycache__ *.pyc

# Target to display help information
help:
	@echo "RPAL Interpreter - Available targets:"
	@echo "  make run file=<file>      - Run the RPAL program"
	@echo "  make ast file=<file>      - Print the abstract syntax tree"
	@echo "  make sast file=<file>     - Print the standardized abstract syntax tree"
	@echo "  make pretty file=<file>   - Print output in prettified format"
	@echo "  make clean                - Remove generated files"
	@echo "  make help                 - Show this help message"

# Phony targets to avoid conflicts with files named 'run', 'ast', 'sast', or 'pretty'
.PHONY: help check_file run ast sast pretty clean