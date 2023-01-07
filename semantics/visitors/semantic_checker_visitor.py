from semantics import visitor
from semantics.scope import Scope
from utils import *

class SemanticCheckerVisitor(object):
    def __init__(self):
        self.errors = []
        self.colors = ['blue', 'green', 'purple', 'black']

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(Scene)
    def visit(self, node: Scene, scope: Scope = None):
        scope = Scope(scope)
        for draw in node.draws:
            self.visit(draw, scope)

        return self.errors

    @visitor.when(Draw)
    def visit(self, node: Draw, scope: Scope = None):
        self.visit(node.shape, scope)
        self.visit(node.x, scope)
        self.visit(node.y, scope)

    @visitor.when(Shape)
    def visit(self, node: Shape, scope: Scope = None):
        self.check_pencil(node.pencil)
        for rule in node.rules:
            self.visit(rule, scope)
        self.visit(node.axiom, scope)

    def check_pencil(self, pencil_color):
        if pencil_color in self.colors:
            return
        if self.is_hex_color(pencil_color):
            return
        self.errors.append(f"Invalid color '{pencil_color}'")

    def is_hex_color(self, pencil_color):
        NUMERAL = "#"
        len_hex_color = len(pencil_color)
        a_f = ['a', 'b', 'c', 'd', 'e', 'f']
        n_0_9 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if pencil_color[0] != NUMERAL:
            return False
        if len_hex_color != 4 and len_hex_color != 7:
            return False
        for letter in pencil_color[1:]:
            lower_l = letter.lower()
            if lower_l not in a_f and lower_l not in n_0_9:
                return False
        return True

    @visitor.when(Rule)
    def visit(self, node: Rule, scope: Scope = None):
        scope.define_rule(node.name, node.param)
        for instruction in node.instructions:
            self.visit(instruction, scope)

    @visitor.when(Axiom)
    def visit(self, node: Axiom, scope: Scope = None):
        for instruction in node.instructions:
            self.visit(instruction, scope)

    @visitor.when(Value)
    def visit(self, node: Value, scope: Scope = None):
        pass

    @visitor.when(CallRuleInstruction)
    def visit(self, node: CallRuleInstruction, scope: Scope = None):
        if not scope.is_rule_defined(node.id):
            self.errors.append(f"Don't exist's rule '{node.id}'")
        self.visit(node.expression, scope) # Checkear que Value sea entero
        
    @visitor.when(LeftInstruction)
    def visit(self, node: LeftInstruction, scope:Scope=None):
        self.visit(node.expression, scope)
        
    @visitor.when(RightInstruction)
    def visit(self, node: RightInstruction, scope:Scope=None):
        self.visit(node.expression, scope)
        
    @visitor.when(LineInstruction)
    def visit(self, node: LineInstruction, scope:Scope=None):
        self.visit(node.expression, scope)
        
    @visitor.when(PushInstruction)
    def visit(self, node: PushInstruction, scope:Scope=None):
        pass
    
    @visitor.when(PopInstruction)
    def visit(self, node: PopInstruction, scope:Scope=None):
        pass
    
    @visitor.when(JumpInstruction)
    def visit(self, node: JumpInstruction, scope:Scope=None):
        self.visit(node.x, scope)
        self.visit(node.y, scope)
        
    @visitor.when(Assign)
    def visit(self, node: Assign, scope:Scope=None):
        self.visit(node.expression, scope)
        scope.define_var(node.ID, node.expression)
        
    @visitor.when(SetX)
    def visit(self, node: SetX, scope:Scope=None):
        self.visit(node.expression, scope)
        
    @visitor.when(SetY)
    def visit(self, node: SetY, scope:Scope=None):
        self.visit(node.expression, scope)
        
    @visitor.when(GetX)
    def visit(self, node: GetX, scope:Scope=None):
        pass
        
    @visitor.when(GetY)
    def visit(self, node: GetY, scope:Scope=None):
        pass
    
    @visitor.when(SetPencil)
    def visit(self, node: SetPencil, scope:Scope=None):
        self.check_pencil(node.ID)
        
    @visitor.when(If)
    def visit(self, node: If, scope:Scope=None):
        self.visit(node.condition, scope)
        nscope = scope.create_child_scope()
        for instruction in node.if_body:
            self.visit(instruction, nscope)
        if node.else_body:
            for instruction in node.else_body:
                self.visit(instruction, nscope)
    
    @visitor.when(While)
    def visit(self, node: While, scope:Scope=None):
        self.visit(node.condition, scope)
        nscope = scope.create_child_scope(scope)
        for instruction in node.body:
            self.visit(instruction, nscope)
            
    @visitor.when(AndCondition)
    def visit(self, node: AndCondition, scope:Scope=None):
        self.visit(node.left, scope)
        self.visit(node.right, scope)
        
    @visitor.when(OrCondition)
    def visit(self, node: OrCondition, scope:Scope=None):
        self.visit(node.left, scope)
        self.visit(node.right, scope)
        
    @visitor.when(NotCondition)
    def visit(self, node: NotCondition, scope:Scope=None):
        self.visit(node.expr, scope)
        
    @visitor.when(GreaterCondition)
    def visit(self, node: GreaterCondition, scope:Scope=None):
        self.visit(node.left, scope)
        self.visit(node.right, scope)
        
    @visitor.when(MenorCondition)
    def visit(self, node: MenorCondition, scope:Scope=None):
        self.visit(node.left, scope)
        self.visit(node.right, scope)
        
    @visitor.when(EqualCondition)
    def visit(self, node: EqualCondition, scope:Scope=None):
        self.visit(node.left, scope)
        self.visit(node.right, scope)
        
    @visitor.when(SumExpr)
    def visit(self, node: SumExpr, scope:Scope=None):
        self.visit(node.left, scope)
        self.visit(node.right, scope)
        
    @visitor.when(SubExpr)
    def visit(self, node: SubExpr, scope:Scope=None):
        self.visit(node.left, scope)
        self.visit(node.right, scope)
        
    @visitor.when(MultExpr)
    def visit(self, node: MultExpr, scope:Scope=None):
        self.visit(node.left, scope)
        self.visit(node.right, scope)
        
    @visitor.when(DivExpr)
    def visit(self, node: DivExpr, scope:Scope=None):
        self.visit(node.left, scope)
        self.visit(node.right, scope)
        
    @visitor.when(PowExpr)
    def visit(self, node: PowExpr, scope:Scope=None):
        self.visit(node.left, scope)
        self.visit(node.right, scope)
        
    @visitor.when(Factor)
    def visit(self, node: Factor, scope:Scope=None):
        pass
        
    @visitor.when(Function)
    def visit(self, node: Function, scope:Scope=None):
        self.visit(node.expression, scope)
        self.visit(node.func, scope)
        
    @visitor.when(CallShapeInstruction)
    def visit(self, node: CallShapeInstruction, scope:Scope=None):
        self.visit(node.shape, scope)
    
    @visitor.when(ContextNode)
    def visit(self, node: ContextNode, scope: Scope = None):
        pass