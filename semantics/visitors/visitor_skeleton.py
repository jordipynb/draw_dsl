from semantics import visitor
from utils import *


class Visitor(object):
    def __init__(self):
        self.errors = []

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(Scene)
    def visit(self, node: Scene):
        pass

    @visitor.when(Draw)
    def visit(self, node: Draw):
        pass

    @visitor.when(Shape)
    def visit(self, node: Shape):
        pass
    
    @visitor.when(Nill)
    def visit(self, node: Nill):
        pass

    @visitor.when(Rule)
    def visit(self, node: Rule):
        pass
    
    @visitor.when(Axiom)
    def visit(self, node:Axiom):
        pass

    ## ++++++++++++++++++++ Instructions ++++++++++++++++++++##
    @visitor.when(Break)
    def visit(self, node: Break):
        pass

    @visitor.when(TrueCondition)
    def visit(self, node: TrueCondition):
        pass

    @visitor.when(FalseCondition)
    def visit(self, node: FalseCondition):
        pass

    @visitor.when(LeftInstruction)
    def visit(self, node: LeftInstruction):
        pass

    @visitor.when(RightInstruction)
    def visit(self, node: RightInstruction):
        pass

    @visitor.when(LineInstruction)
    def visit(self, node: LineInstruction):
        pass

    @visitor.when(PushInstruction)
    def visit(self, node: PushInstruction):
        pass

    @visitor.when(PopInstruction)
    def visit(self, node: PopInstruction):
        pass

    @visitor.when(JumpInstruction)
    def visit(self, node: JumpInstruction):
        pass

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

    @visitor.when(AndOperator)
    def visit(self, node: AndOperator):
        pass

    @visitor.when(OrOperator)
    def visit(self, node: OrOperator):
        pass

    @visitor.when(NotOperator)
    def visit(self, node: NotOperator):
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

    @visitor.when(SumExpression)
    def visit(self, node: SumExpression):
        pass

    @visitor.when(SubExpression)
    def visit(self, node: SubExpression):
        pass

    @visitor.when(MulTerm)
    def visit(self, node: MulTerm):
        pass

    @visitor.when(DivTerm)
    def visit(self, node: DivTerm):
        pass

    @visitor.when(Pow)
    def visit(self, node: Pow):
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