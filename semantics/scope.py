class VariableInfo:
    def __init__(self, name:str) -> None:
        self.name = name
        
class InstructionInfo:
    def __init__(self) -> None:
        pass

class RuleInfo:
    def __init__(self, name:str) -> None:
        self.name = name

class AxiomInfo:
    def __init__(self, instructions:list[InstructionInfo]) -> None:
        self.instructions = instructions

class ShapeInfo:
    def __init__(self, name:str) -> None:
        self.name = name

class Scope:
    def __init__(self, parent=None):
        # self.shapes = []
        # self.local_rules = []
        # self.local_vars = []
        self.parent = parent
        self.children = []
        # self.local_rules_at_parent = 0 if parent is None else len(parent.local_rules)
        
        
    def create_child_scope(self):
        child_scope = Scope(self)
        self.children.append(child_scope)
        return child_scope
    
    # def define_shape(self, name):
    #     # child_scope = self.create_child_scope()
    #     shape = ShapeInfo(name)
    #     self.shapes.append(shape)
    #     return self
    
    # def is_shape_defined(self, name):
    #     for shape in self.shapes:
    #         if shape.name == name:
    #             return True
    #     return False
    
    # def define_rule(self, name, param):
    #     child_scope = self.create_child_scope()
    #     rule = RuleInfo(name)
    #     self.local_rules.append(rule)
        
    #     child_scope.local_rules.append(rule)
    #     child_scope.local_vars.append(VariableInfo(param))
    #     return child_scope
    
    # def is_rule_defined(self, name):
    #     for rule in self.local_rules:
    #         if rule.name == name:
    #             return True
    #     return False