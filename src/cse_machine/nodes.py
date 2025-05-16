class Symbol:
    """Base class for all CSE machine symbols"""
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
    
    def get_data(self):
        return self.name
    
    def set_data(self, data):
        self.name = data

class Rand(Symbol):
    """Base class for operands (data values)"""
    pass

class Rator(Symbol):
    """Base class for operators"""
    pass

class PrimitiveValue(Rand):
    """Base class for primitive values like integers, booleans, strings"""
    def __init__(self, value):
        super().__init__(str(value))
        self.value = value

class Int(PrimitiveValue):
    """Integer value"""
    def __init__(self, value):
        if isinstance(value, str):
            value = int(value)
        super().__init__(value)
        
    def get_value(self):
        return int(self.value)

class Str(PrimitiveValue):
    """String value"""
    def __init__(self, value):
        super().__init__(value)
    
    def get_value(self):
        return str(self.value)

class Bool(PrimitiveValue):
    """Boolean value"""
    def __init__(self, value):
        if isinstance(value, str):
            value = value.lower() == "true"
        super().__init__("true" if value else "false")
        self.value = value
    
    def get_value(self):
        return self.value == "true" or self.value is True

class Id(Rand):
    """Identifier symbol"""
    def __init__(self, name):
        super().__init__(name)

class Dummy(Rand):
    """Dummy symbol"""
    def __init__(self):
        super().__init__("dummy")

class Uop(Rator):
    """Unary operator symbol"""
    def __init__(self, op):
        super().__init__(op)

class Bop(Rator):
    """Binary operator symbol"""
    def __init__(self, op):
        super().__init__(op)

class Gamma(Symbol):
    """Gamma (function application) symbol"""
    def __init__(self):
        super().__init__("gamma")

class Delta(Symbol):
    """Delta (code block) symbol"""
    def __init__(self, index):
        super().__init__("delta")
        self.index = index
        self.symbols = []
    
    def get_index(self):
        return self.index
    
    def set_index(self, index):
        self.index = index

class E(Symbol):
    """Environment symbol"""
    def __init__(self, index):
        super().__init__("e")
        self.index = index
        self.parent = None
        self.bindings = {}
        self.is_removed = False
    
    def get_index(self):
        return self.index
    
    def set_index(self, index):
        self.index = index
    
    def get_parent(self):
        return self.parent
    
    def set_parent(self, parent):
        self.parent = parent
    
    def is_marked_removed(self):
        return self.is_removed
    
    def mark_removed(self, removed=True):
        self.is_removed = removed
    
    def bind(self, identifier, value):
        """Bind a value to an identifier in this environment"""
        self.bindings[identifier.get_data()] = value
    
    def lookup(self, identifier):
        """Look up a value by identifier, searching parent environments if needed"""
        id_name = identifier.get_data()
        if id_name in self.bindings:
            return self.bindings[id_name]
        elif self.parent is not None:
            return self.parent.lookup(identifier)
        return Symbol(id_name)  # Return the identifier itself if not found

class Lambda(Symbol):
    """Lambda (function) symbol"""
    def __init__(self, index):
        super().__init__("lambda")
        self.index = index
        self.environment_index = None
        self.identifiers = []
        self.body = None
    
    def get_index(self):
        return self.index
    
    def set_environment_index(self, env_index):
        self.environment_index = env_index
    
    def get_environment_index(self):
        return self.environment_index
    
    def set_body(self, body):
        self.body = body
    
    def get_body(self):
        return self.body

class Eta(Symbol):
    """Eta (recursive function) symbol"""
    def __init__(self):
        super().__init__("eta")
        self.index = None
        self.environment_index = None
        self.identifier = None
        self.lambda_func = None
    
    def get_index(self):
        return self.index
    
    def set_index(self, index):
        self.index = index
    
    def get_environment_index(self):
        return self.environment_index
    
    def set_environment_index(self, env_index):
        self.environment_index = env_index
    
    def set_identifier(self, identifier):
        self.identifier = identifier
    
    def get_identifier(self):
        return self.identifier
    
    def set_lambda(self, lambda_func):
        self.lambda_func = lambda_func
    
    def get_lambda(self):
        return self.lambda_func

class Ystar(Symbol):
    """Y* (fixed-point combinator) symbol"""
    def __init__(self):
        super().__init__("<Y*>")

class Beta(Symbol):
    """Beta (conditional) symbol"""
    def __init__(self):
        super().__init__("beta")

class Tau(Symbol):
    """Tau (tuple construction) symbol"""
    def __init__(self, size):
        super().__init__("tau")
        self.size = size
    
    def get_size(self):
        return self.size

class Tup(Rand):
    """Tuple value"""
    def __init__(self):
        super().__init__("tup")
        self.elements = []
    
    def add_element(self, element):
        self.elements.append(element)
    
    def get_elements(self):
        return self.elements

class B(Symbol):
    """B (conditional test) symbol"""
    def __init__(self):
        super().__init__("b")
        self.symbols = []