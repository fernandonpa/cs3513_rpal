from .node_types import NodeType

class ASTPrinter:
    """
    Class to generate a readable string representation of an AST
    """
    
    @staticmethod
    def print(ast_node, format_type="structured"):
        """
        Print an AST in the specified format
        
        Args:
            ast_node: The root node of the AST
            format_type: The format to print ("structured", "linear", or "standardized")
            
        Returns:
            str: String representation of the AST
        """
        if format_type == "structured":
            return ASTPrinter._print_structured(ast_node)
        elif format_type == "linear":
            return ASTPrinter._print_linear(ast_node)
        elif format_type == "standardized":
            return ASTPrinter._print_standardized(ast_node)
        else:
            raise ValueError(f"Unknown format type: {format_type}")
    
    @staticmethod
    def _print_structured(node, indent=0):
        """Print AST with indentation to show structure"""
        if node is None:
            return ""
            
        # Prepare indentation
        spaces = " " * indent
        
        # Print node info
        result = f"{spaces}{node.node_type.name}"
        if node.value is not None:
            result += f"({node.value})"
        result += "\n"
        
        # Print children with increased indentation
        for child in node.children:
            result += ASTPrinter._print_structured(child, indent + 2)
            
        return result
    
    @staticmethod
    def _print_linear(node):
        """Print AST as a single line (for simple viewing)"""
        if node is None:
            return ""
            
        # Start with node info
        if node.value is not None:
            result = f"{node.node_type.name}({node.value})"
        else:
            result = f"{node.node_type.name}"
        
        # Add children if any
        if node.children:
            result += "["
            result += ", ".join(ASTPrinter._print_linear(child) for child in node.children)
            result += "]"
            
        return result
    
    @staticmethod
    def _print_standardized(node, prefix=""):
        """
        Print AST in a standardized format with dot notation
        
        This format is useful for comparing ASTs and for displaying the tree
        structure in a more compact form.
        """
        if node is None:
            return ""
        
        lines = []
        
        # Print current node
        if node.value is not None and node.node_type in [
            NodeType.IDENTIFIER, NodeType.INTEGER, NodeType.STRING, 
            NodeType.TRUE, NodeType.FALSE, NodeType.NIL, NodeType.DUMMY
        ]:
            lines.append(f"{prefix}<{node.node_type.name}:{node.value}>")
        else:
            # For operation nodes, just print the canonical name
            op_name = node.value if node.value else node.node_type.name.lower()
            lines.append(f"{prefix}{op_name}")
        
        # Print children with increased prefix
        for child in node.children:
            lines.extend(ASTPrinter._print_standardized(child, prefix + ".").split("\n"))
        
        return "\n".join(lines)