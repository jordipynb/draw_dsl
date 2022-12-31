class VariableInfo:
    def __init__(self, name:str) -> None:
        self.name = name
        
class InstructionInfo:
    def __init__(self) -> None:
        pass

# class RuleInfo:
#     def __init__(self, name:str, param:VariableInfo, instructions:list[InstructionInfo]) -> None:
#         self.name = name
#         self.param = param
#         self.instructions = instructions

class RuleInfo:
    def __init__(self, name:str) -> None:
        self.name = name

class AxiomInfo:
    def __init__(self, instructions:list[InstructionInfo]) -> None:
        self.instructions = instructions

# class ShapeInfo:
#     def __init__(self, name:str, pencil:str, rules:list[RuleInfo], axiom:AxiomInfo) -> None:
#         self.name = name
#         self.pencil = pencil
#         self.rules = rules
#         self.axiom = axiom
class ShapeInfo:
    def __init__(self, name:str) -> None:
        self.name = name

class Scope:
    def __init__(self, parent=None):
        self.shapes = []
        self.local_rules = []
        self.parent = parent
        self.children = []
        self.local_rules_at_parent = 0 if parent is None else len(parent.local_rules)
        
    def create_child_scope(self):
        child_scope = Scope(self)
        self.children.append(child_scope)
        return child_scope
    
    def define_shape(self, name):
        child_scope = self.create_child_scope()
        self.local_shapes.append(ShapeInfo(name))
        return child_scope
    
    def define_rule(self, name):
        child_scope = self.create_child_scope()
        self.local_rules.append(RuleInfo(name))
        child_scope.local_rules.append(RuleInfo(name))
        return child_scope
    
    # def define_shape(self, name, pencil, rules, axiom):
    #     child_scope = self.create_child_scope()
    #     rules = self._get_rule_info_list(rules)
    #     axiom = AxiomInfo(self._get_instruction_info_list(axiom.instructions))
    #     self.local_shapes.append(ShapeInfo(name, pencil, rules, axiom))
    #     return child_scope
    
    # def _get_rule_info_list(self, rules):
    #     rules_info = []
    #     for rule in rules:
    #         rule_info = self._get_rule_info(rule)
    #         rules_info.append(rule_info)
    #     return rules_info
    
    # def _get_rule_info(self, rule):
    #     name = rule.name
    #     param = VariableInfo(rule.param)
    #     instructions = self._get_instruction_info_list(rule.instructions)
    #     return RuleInfo(name, param, instructions)
    
    # def _get_instruction_info_list(self, instructions):
    #     instructions_info = []
    #     for instruction in instructions:
    #         instructions_info.append(InstructionInfo(instruction))
    #     return instructions_info
    
    # def define_rule(self, name:str, param:str, instructions):
    #     child_scope = self.create_child_scope()
    #     param = VariableInfo(param)
    #     instructions = self._get_instruction_info_list(instructions)
    #     rule_info = RuleInfo(name, param, instructions)
    #     self.local_rules.append(rule_info)
    #     child_scope.local_rules.extend(self.local_rules)
    #     return child_scope
    def is_shape_defined(self, name):
        for shape in self.shapes:
            if shape.name == name:
                return True
        return False