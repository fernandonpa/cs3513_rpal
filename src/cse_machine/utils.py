from .nodes import Tup, Int, Str, Bool, Symbol

def format_tuple(tup):
    """Format a tuple for display"""
    elements = []
    for element in tup.get_elements():
        if isinstance(element, Tup):
            elements.append(format_tuple(element))
        else:
            elements.append(str(element.get_data()))
    
    return f"({', '.join(elements)})"

def debug_print_control(control):
    """Format and print the control stack"""
    result = []
    for symbol in control:
        name = symbol.get_data()
        if hasattr(symbol, 'get_index'):
            name += str(symbol.get_index())
        result.append(name)
    
    return "Control: " + ", ".join(result)

def debug_print_stack(stack):
    """Format and print the value stack"""
    result = []
    for symbol in stack:
        if isinstance(symbol, Tup):
            result.append(format_tuple(symbol))
        else:
            name = symbol.get_data()
            if hasattr(symbol, 'get_index'):
                name += str(symbol.get_index())
            result.append(name)
    
    return "Stack: " + ", ".join(result)

def debug_print_environment(env_list):
    """Format and print the environment structure"""
    result = []
    for env in env_list:
        if env.is_marked_removed():
            continue
            
        parent_info = ""
        if env.get_index() != 0 and env.get_parent() is not None:
            parent_info = f" -> e{env.get_parent().get_index()}"
            
        bindings = []
        for id_name, value in env.bindings.items():
            bindings.append(f"{id_name}: {value.get_data()}")
            
        result.append(f"e{env.get_index()}{parent_info} {{{', '.join(bindings)}}}")
    
    return "Environment:\n  " + "\n  ".join(result)

def write_debug_info(file_path, info):
    """Write debug information to a file"""
    with open(file_path, 'a') as f:
        f.write(f"{info}\n")

def clear_debug_file(file_path):
    """Clear a debug file"""
    with open(file_path, 'w') as f:
        pass