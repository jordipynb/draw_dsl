from semantics import visitor
from semantics.scope import Scope
from utils import *

class RuleShapeCollector:
    def __init__(self, scene) -> None:
        self.scope = Scope()
        self.visit(scene)
        
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(Scene)
    def visit(self, node: Scene):
        for draw in node.draws:
            self.visit(draw)

    @visitor.when(Draw)
    def visit(self, node: Draw):
        self.visit(node.shape)

    @visitor.when(Shape)
    def visit(self, node: Shape):
        self.scope.define_shape(node.name)
        for rule in node.rules:
            self.visit(rule)
        
    @visitor.when(Rule)
    def visit(self, node: Rule):
        self.scope.define_rule(node.name, node.param)


class TypeCollector:
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(Scene)
    def visit(self, node: Scene, scope: Scope):
        scope = Scope(scope)
        for draw in node.draws:
            self.visit(draw, scope)

    @visitor.when(Draw)
    def visit(self, node: Draw, scope:Scope):
        # new_scope = scope.create_child_scope()
        self.visit(node.shape, scope)
        self.visit(node.x, scope)
        self.visit(node.y, scope)

    @visitor.when(Shape)
    def visit(self, node: Shape, scope:Scope):
        for rule in node.rules:
            self.visit(rule, scope)
        self.visit(node.axiom, scope)
    
    @visitor.when(Nill)
    def visit(self, node: Nill, scope:Scope):
        pass

    @visitor.when(Rule)
    def visit(self, node: Rule, scope:Scope):
        scope.create_type(node.name)
        for instruction in node.instructions:
            self.visit(instruction, scope)
    
    @visitor.when(Axiom)
    def visit(self, node:Axiom, scope:Scope):
        for instruction in node.instructions:
            self.visit(instruction, scope)
    
    @visitor.when(Value)
    def visit(self, node:Value, scope:Scope):
        pass

    ## ++++++++++++++++++++ Instructions ++++++++++++++++++++##
    @visitor.when(Break)
    def visit(self, node: Break, scope):
        pass

    @visitor.when(TrueCondition)
    def visit(self, node: TrueCondition, scope):
        pass

    @visitor.when(FalseCondition)
    def visit(self, node: FalseCondition, scope):
        pass

    @visitor.when(LeftInstruction)
    def visit(self, node: LeftInstruction, scope):
        self.visit(node.expression, scope)

    @visitor.when(RightInstruction)
    def visit(self, node: RightInstruction, scope):
        self.visit(node.expression, scope)

    @visitor.when(LineInstruction)
    def visit(self, node: LineInstruction, scope):
        self.visit(node.expression, scope)

    @visitor.when(PushInstruction)
    def visit(self, node: PushInstruction):
        pass

    @visitor.when(PopInstruction)
    def visit(self, node: PopInstruction):
        pass

    @visitor.when(JumpInstruction)
    def visit(self, node: JumpInstruction, scope):
        self.visit(node.x, scope)
        self.visit(node.y, scope)

    @visitor.when(Assign)
    def visit(self, node: Assign):
        pass

    @visitor.when(SetX)
    def visit(self, node: SetX):
        pass

    @visitor.when(SetY)
    def visit(self, node: SetY):
        pass

    @visitor.when(GetX)
    def visit(self, node: GetX):
        pass

    @visitor.when(GetY)
    def visit(self, node: GetY):
        pass

    @visitor.when(SetPencil)
    def visit(self, node: SetPencil):
        pass

    @visitor.when(If)
    def visit(self, node: If):
        pass

    @visitor.when(While)
    def visit(self, node: While):
        pass

    @visitor.when(AndCondition)
    def visit(self, node: AndCondition):
        pass

    @visitor.when(OrCondition)
    def visit(self, node: OrCondition):
        pass

    @visitor.when(NotCondition)
    def visit(self, node: NotCondition):
        pass

    @visitor.when(GreaterCondition)
    def visit(self, node: GreaterCondition):
        pass

    @visitor.when(MenorCondition)
    def visit(self, node: MenorCondition):
        pass

    @visitor.when(EqualCondition)
    def visit(self, node: EqualCondition):
        pass

    @visitor.when(SumExpr)
    def visit(self, node: SumExpr):
        pass

    @visitor.when(SubExpr)
    def visit(self, node: SubExpr):
        pass

    @visitor.when(MultExpr)
    def visit(self, node: MultExpr):
        pass

    @visitor.when(DivExpr)
    def visit(self, node: DivExpr):
        pass

    @visitor.when(PowExpr)
    def visit(self, node: PowExpr):
        pass

    @visitor.when(Factor)
    def visit(self, node: Factor):
        pass

    @visitor.when(Function)
    def visit(self, node: Function):
        pass

    @visitor.when(CallShapeInstruction)
    def visit(self, node: CallShapeInstruction):
        pass

    @visitor.when(CallRuleInstruction)
    def visit(self, node: CallRuleInstruction):
        pass