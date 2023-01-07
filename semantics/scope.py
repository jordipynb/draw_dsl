from ply.lex import LexToken

def find_column(t):
    last_cr = t.lexer.lexdata.rfind('\n', 0, t.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (t.lexpos - last_cr)
    return column

class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.children = []
        self.local_rules = {}
        self.local_vars = []
        self.local_shapes = []
        self.local_funcs = {}
        self.inside_loop = False
        

    def create_child_scope(self):
        child_scope = Scope(self)
        self.children.append(child_scope)
        return child_scope
    
    def token_info(self, token: LexToken):
        value = token.value
        line = token.lineno
        column = find_column(token)
        return value, line, column

    def exist_var(self, name):
        return name in self.local_vars

    def exist_var(self, var: str) -> bool:
        return var in self.local_vars

    def exist_fun(self, fun: str) -> bool:
        return fun in self.local_funcs

    def exist_rule(self, rule: str) -> bool:
        return rule in self.local_rules
    
    def exist_shape(self, shape:str):
        return shape in self.local_shapes

    def check_var(self, var: str) -> bool:
        return self.exist_var(var)

    def check_fun(self, fun: str, len_args: int) -> bool:
        if self.exist_fun(fun):
            return any(len_args == len(args) for args in self.local_funcs.values())
        return False

    def check_rule(self, rule: str) -> bool:
        return self.exist_rule(rule)
    
    def check_shape(self, shape: str) -> bool:
        return self.exist_rule(shape)

    def define_var(self, var: str) -> bool:
        if self.exist_var(var):
            return False
        else:
            self.local_vars.append(var)
            return True

    def define_fun(self, fun: str, args: list[str]) -> bool:
        if self.exist_fun(fun):
            return False
        else:
            self.local_funcs[fun] = args
            return True

    def define_rule(self, rule: str, param: str) -> bool:
        if self.exist_rule(rule):
            return False
        else:
            self.local_rules[rule] = param
            return True

    def define_shape(self, shape: str) -> bool:
        if self.exist_shape(shape):
            return False
        else:
            self.local_shapes.append(shape)
            return True
        
    def define_loop(self):
        self.inside_loop = True
        
    def undefine_loop(self):
        self.inside_loop = False
