from .nodes import *
from .machine import CSEMachine
from .factory import CSEMachineFactory
from .error_handler import CSEError

def create_cse_machine(ast):
    """Create a CSE machine from an AST"""
    factory = CSEMachineFactory()
    return factory.create_machine_from_ast(ast)

def evaluate_ast(ast, debug=False):
    """Evaluate an AST using the CSE machine"""
    machine = create_cse_machine(ast)
    
    if debug:
        machine.enable_debug()
        
    machine.execute()
    return machine.get_result()