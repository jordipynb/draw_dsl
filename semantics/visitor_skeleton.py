from semantics.visitor import on, when
from utils import *


class Visitor(object):
    def __init__(self):
        self.errors = []

    @on('node')
    def visit(self, node):
        pass

    @when(Scene)
    def visit(self, node: Scene):
        pass

    @when(Draw)
    def visit(self, node: Draw):
        pass

    @when(Shape)
    def visit(self, node: Shape):
        pass
    
    @when(Nill)
    def visit(self, node: Nill):
        pass

    @when(Rule)
    def visit(self, node: Rule):
        pass
    
    @when(Axiom)
    def visit(self, node:Axiom):
        pass

    ## ++++++++++++++++++++ Instructions ++++++++++++++++++++##
    @when(Break)
    def visit(self, node: Break):
        pass

    @when(TrueCondition)
    def visit(self, node: TrueCondition):
        pass

    @when(FalseCondition)
    def visit(self, node: FalseCondition):
        pass

    @when(LeftInstruction)
    def visit(self, node: LeftInstruction):
        pass

    @when(RightInstruction)
    def visit(self, node: RightInstruction):
        pass

    @when(LineInstruction)
    def visit(self, node: LineInstruction):
        pass

    @when(PushInstruction)
    def visit(self, node: PushInstruction):
        pass

    @when(PopInstruction)
    def visit(self, node: PopInstruction):
        pass

    @when(JumpInstruction)
    def visit(self, node: JumpInstruction):
        pass

    @when(Assign)
    def visit(self, node: Assign):
        pass

    @when(SetX)
    def visit(self, node: SetX):
        pass

    @when(SetY)
    def visit(self, node: SetY):
        pass

    @when(GetX)
    def visit(self, node: GetX):
        pass

    @when(GetY)
    def visit(self, node: GetY):
        pass

    @when(SetPencil)
    def visit(self, node: SetPencil):
        pass

    @when(If)
    def visit(self, node: If):
        pass

    @when(While)
    def visit(self, node: While):
        pass

    @when(AndOperator)
    def visit(self, node: AndOperator):
        pass

    @when(OrOperator)
    def visit(self, node: OrOperator):
        pass

    @when(NotOperator)
    def visit(self, node: NotOperator):
        pass

    @when(GreaterCondition)
    def visit(self, node: GreaterCondition):
        pass

    @when(MenorCondition)
    def visit(self, node: MenorCondition):
        pass

    @when(EqualCondition)
    def visit(self, node: EqualCondition):
        pass

    @when(SumExpression)
    def visit(self, node: SumExpression):
        pass

    @when(SubExpression)
    def visit(self, node: SubExpression):
        pass

    @when(MulTerm)
    def visit(self, node: MulTerm):
        pass

    @when(DivTerm)
    def visit(self, node: DivTerm):
        pass

    @when(Pow)
    def visit(self, node: Pow):
        pass

    @when(Factor)
    def visit(self, node: Factor):
        pass

    @when(Function)
    def visit(self, node: Function):
        pass

    @when(CallShapeInstruction)
    def visit(self, node: CallShapeInstruction):
        pass

    @when(CallRuleInstruction)
    def visit(self, node: CallRuleInstruction):
        pass