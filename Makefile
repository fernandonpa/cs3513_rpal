PYTHON = python3

# Default target: runs the RPAL processor with the specified file
run:
	$(PYTHON) myrpal.py $(file)

# Target to print the AST
ast:
	$(PYTHON) myrpal.py $(file) -ast

# Target to print the standardized AST
sast:
	$(PYTHON) myrpal.py $(file) -sast

clean:
	rm -rf __pycache__ *.pyc

# Phony targets to avoid conflicts with files named 'run', 'ast', or 'sast'
.PHONY: run ast sast
