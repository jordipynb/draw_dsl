from semantics import visitor
from semantics.scope import Scope
from semantics.visitors.type_collector import RuleShapeCollector
import utils


class ContextValidatorVisitor(object):
    def __init__(self):
        self.errors = []
        
    @property
    def has_errors(self):
        return len(self.errors) > 0
    
    @property
    def show_errors(self):
        print('\n'.join(set(self.errors)))
        
    @property
    def error(self):
        if len(self.errors) > 0:
            return self.errors[0]

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(utils.Scene)
    def visit(self, node: utils.Scene, scope: Scope=None):
        scope = RuleShapeCollector(node).scope
        for draw in node.draws:
            self.visit(draw, scope)

    @visitor.when(utils.Draw)
    def visit(self, node: utils.Draw, scope: Scope=None):
        return self.visit(node.shape, scope)

    @visitor.when(utils.Shape)
    def visit(self, node: utils.Shape, scope: Scope):
        for rule in node.rules:
            if not self.visit(rule, scope):
                return False
        return self.visit(node.axiom, scope)

    # @visitor.when(utils.Nill)
    # def visit(self, node: utils.Nill, scope: Scope):
    #     pass

    @visitor.when(utils.Rule)
    def visit(self, node: utils.Rule, scope: Scope):
        nscope = scope.create_child_scope()
        nscope.define_var(node.param)
        for instruction in node.instructions:
            if not self.visit(instruction, nscope):
                return False
        return True

    @visitor.when(utils.Axiom)
    def visit(self, node: utils.Axiom, scope: Scope):
        nscope = scope.create_child_scope()
        for instruction in node.instructions:
            if not self.visit(instruction, nscope):
                return False

    ## ++++++++++++++++++++ Instructions ++++++++++++++++++++##

    @visitor.when(utils.JumpInstruction)
    def visit(self, node: utils.JumpInstruction, scope: Scope):
        return self.visit(node.x, scope) and self.visit(node.y, scope)
        
    @visitor.when(utils.LeftInstruction)
    def visit(self, node: utils.LeftInstruction, scope: Scope):
        return self.visit(node.expression, scope)

    @visitor.when(utils.RightInstruction)
    def visit(self, node: utils.RightInstruction, scope: Scope):
        return self.visit(node.expression, scope)

    @visitor.when(utils.LineInstruction)
    def visit(self, node: utils.LineInstruction, scope: Scope):
        return self.visit(node.expression, scope)

    # @visitor.when(utils.PushInstruction)
    # def visit(self, node: utils.PushInstruction, scope: Scope):
    #     pass

    # @visitor.when(utils.PopInstruction)
    # def visit(self, node: utils.PopInstruction, scope: Scope):
    #     pass

    

    @visitor.when(utils.Assign)
    def visit(self, node: utils.Assign, scope: Scope):
        scope.define_var(node.ID)
        return self.visit(node.expression, scope) # Creo que aqui puede haber un posible error semantico

    @visitor.when(utils.SetX)
    def visit(self, node: utils.SetX, scope: Scope):
        return self.visit(node.expression, scope)

    @visitor.when(utils.SetY)
    def visit(self, node: utils.SetY, scope: Scope):
        return self.visit(node.expression,scope)

    @visitor.when(utils.GetX)
    def visit(self, node: utils.GetX, scope: Scope):
        scope.define_var(node.ID)
        return True

    @visitor.when(utils.GetY)
    def visit(self, node: utils.GetY, scope: Scope):
        scope.define_var(node.ID)
        return True

    # @visitor.when(utils.SetPencil)
    # def visit(self, node: utils.SetPencil, scope: Scope):
    #     pass

    @visitor.when(utils.If)
    def visit(self, node: utils.If, scope: Scope):
        if not self.visit(node.condition, scope):  # Aqui pueden haber problemas con la condicion
            return False
        nscope = scope.create_child_scope()
        for instruction in node.if_body:
            if not self.visit(instruction, nscope): return False
        if node.else_body:
            for instruction in node.else_body:
                if not self.visit(instruction, nscope): return False
        return True

    @visitor.when(utils.While)
    def visit(self, node: utils.While, scope: Scope):
        if not self.visit(node.condition, scope):  # Aqui pueden haber problemas con la condicion
            return False
        nscope = scope.create_child_scope()
        nscope.define_loop()
        for instruction in node.body:
            if not self.visit(instruction, nscope): return False
        nscope.undefine_loop()
        return True
    
    @visitor.when(utils.Break)
    def visit(self, node: utils.Break, scope: Scope):
        if not scope.inside_loop:
            self.errors.append("Break no puede usarse fuera de un ciclo")
            return False
        return True

    @visitor.when(utils.CallShapeInstruction)
    def visit(self, node: utils.CallShapeInstruction, scope: Scope):
        if node.shape:
            name = node.shape.name
            if not scope.exist_shape(name):
                self.errors.append(f"No existe shape con nombre: {name}")
                return False
            return True
        return False

    @visitor.when(utils.CallRuleInstruction)
    def visit(self, node: utils.CallRuleInstruction, scope: Scope):
        if not scope.parent.exist_rule(node.id):
            self.errors.append(f"No existe a regla con nombre {node.id}")
            return False
        return self.visit(node.expression, scope)

    # @visitor.when(utils.Instruction)
    # def visit(self, node: utils.Instruction, scope: Scope):
    #     raise node

    ## ++++++++++++++++++++ Expressions ++++++++++++++++++++##

    @visitor.when(utils.BinaryExpr)
    def visit(self, node: utils.AndCondition, scope: Scope):
        return self.visit(node.left, scope) and self.visit(node.right, scope)

    # @visitor.when(utils.OrCondition)
    # def visit(self, node: utils.OrCondition, scope: Scope):
    #     self.visit(node.left, scope)
    #     self.visit(node.right, scope)

    @visitor.when(utils.NotCondition)
    def visit(self, node: utils.NotCondition, scope: Scope):
        self.visit(node.expr, scope)

    # @visitor.when(utils.GreaterCondition)
    # def visit(self, node: utils.GreaterCondition, scope: Scope):
    #     self.visit(node.left, scope)
    #     self.visit(node.right, scope)

    # @visitor.when(utils.MenorCondition)
    # def visit(self, node: utils.MenorCondition, scope: Scope):
    #     self.visit(node.left, scope)
    #     self.visit(node.right, scope)

    # @visitor.when(utils.EqualCondition)
    # def visit(self, node: utils.EqualCondition, scope: Scope):
    #     self.visit(node.left, scope)
    #     self.visit(node.right, scope)

    # @visitor.when(utils.SumExpr)
    # def visit(self, node: utils.SumExpr, scope: Scope):
    #     self.visit(node.left, scope)
    #     self.visit(node.right, scope)

    # @visitor.when(utils.SubExpr)
    # def visit(self, node: utils.SubExpr, scope: Scope):
    #     self.visit(node.left, scope)
    #     self.visit(node.right, scope)

    # @visitor.when(utils.MultExpr)
    # def visit(self, node: utils.MultExpr, scope: Scope):
    #     self.visit(node.left, scope)
    #     self.visit(node.right, scope)

    # @visitor.when(utils.DivExpr)
    # def visit(self, node: utils.DivExpr, scope: Scope):
    #     self.visit(node.left, scope)
    #     self.visit(node.right, scope)

    # @visitor.when(utils.PowExpr)
    # def visit(self, node: utils.PowExpr, scope: Scope):
    #     self.visit(node.left, scope)
    #     self.visit(node.right, scope)

    @visitor.when(utils.Function)
    def visit(self, node: utils.Function, scope: Scope):
        if not scope.check_fun(node.func, 1): # Aqui puede haber un error
            self.errors.append(f"La funcion {node.func} no esta definida")
            return False
        return self.visit(node.expression, scope)

    @visitor.when(utils.Value)
    def visit(self, node: utils.Value, scope: Scope):
        return True

    @visitor.when(utils.TrueCondition)
    def visit(self, node: utils.TrueCondition, scope: Scope):
        return True

    @visitor.when(utils.FalseCondition)
    def visit(self, node: utils.FalseCondition, scope: Scope):
        return True

    
    @visitor.when(utils.Factor)
    def visit(self, node: utils.Factor, scope: Scope):
        value, line, column = scope.token_info(node.ID)
        if not scope.check_var(value):
            self.errors.append(f'SemanticError: "{value}" en la línea {line}, columna {column} no esta definido')
            return False
        return True

    
    # @visitor.when(utils.Expression)
    # def visit(self, node: utils.Expression, scope: Scope):
    #     raise node
