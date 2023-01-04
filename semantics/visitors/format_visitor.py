from semantics import visitor
from utils import *
S = '|  '


class FormatVisitor(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(Scene)
    def visit(self, node: Scene, tabs=0):
        ans = S * tabs + f'Scene:'
        draws = '\n'.join(self.visit(draw, tabs + 1) for draw in node.draws)
        return f'{ans}\n{draws}'

    @visitor.when(Draw)
    def visit(self, node: Draw, tabs=0):
        ans = S * tabs + f'Draw:'
        expr = self.visit(node.shape, tabs + 1)
        x_value = self.visit(node.x, tabs + 1, 'X')
        y_value = self.visit(node.y, tabs + 1, 'Y')
        childs = "\n".join([expr, x_value, y_value])
        return f'{ans}\n{childs}'

    @visitor.when(Shape)
    def visit(self, node: Shape, tabs=0):
        ans = S*tabs + f'Shape:'
        name = S*(tabs+1) + f'name: {node.name}'
        pencil = S*(tabs+1) + f'pencil: {node.pencil}'
        rules = '\n'.join(self.visit(rule, tabs + 1) for rule in node.rules)
        axiom = self.visit(node.axiom, tabs + 1)
        properties = "\n".join([name, pencil, rules, axiom])
        return f'{ans}\n{properties}'

    @visitor.when(Rule)
    def visit(self, node: Rule, tabs=0):
        ans = S*tabs + f'Rule:'
        name = S*(tabs+1) + f'name: {node.name}'
        param = S*(tabs+1) + f'param: {node.param}'
        properties = "\n".join([name, param])
        instructions = '\n'.join(self.visit(instruction, tabs + 1)
                                 for instruction in node.instructions)
        return f'{ans}\n{properties}\n{instructions}'

    @visitor.when(Nill)
    def visit(self, node, tabs=0):
        ans = S*tabs + f'nill'
        return f'{ans}'

    @visitor.when(Value)
    def visit(self, node, tabs=0, header=''):
        ans = S*tabs + f'{header}: {node.value}'
        return f'{ans}'

    @visitor.when(Axiom)  # Falta este
    def visit(self, node: Axiom, tabs=0):
        ans = S*tabs + f'Axiom:'
        instructions = '\n'.join(self.visit(instruction, tabs+1)
                                 for instruction in node.instructions)
        return f'{ans}\n{instructions}'

    # ## ++++++++++++++++++++ Instructions ++++++++++++++++++++##
    # @visitor.when(Break)
    # def visit(self, node: Break):
    #     pass

    # @visitor.when(TrueCondition)
    # def visit(self, node: TrueCondition):
    #     pass

    # @visitor.when(FalseCondition)
    # def visit(self, node: FalseCondition):
    #     pass

    # @visitor.when(LeftInstruction)
    # def visit(self, node: LeftInstruction):
    #     pass

    # @visitor.when(RightInstruction)
    # def visit(self, node: RightInstruction):
    #     pass

    # @visitor.when(LineInstruction)
    # def visit(self, node: LineInstruction):
    #     pass

    # @visitor.when(PushInstruction)
    # def visit(self, node: PushInstruction):
    #     pass

    # @visitor.when(PopInstruction)
    # def visit(self, node: PopInstruction):
    #     pass

    # @visitor.when(JumpInstruction)
    # def visit(self, node: JumpInstruction):
    #     pass

    # @visitor.when(Assign)
    # def visit(self, node: Assign):
    #     pass

    # @visitor.when(SetX)
    # def visit(self, node: SetX):
    #     pass

    # @visitor.when(SetY)
    # def visit(self, node: SetY):
    #     pass

    # @visitor.when(GetX)
    # def visit(self, node: GetX):
    #     pass

    # @visitor.when(GetY)
    # def visit(self, node: GetY):
    #     pass

    # @visitor.when(SetPencil)
    # def visit(self, node: SetPencil):
    #     pass

    # @visitor.when(If)
    # def visit(self, node: If):
    #     pass

    # @visitor.when(While)
    # def visit(self, node: While):
    #     pass

    # @visitor.when(AndOperator)
    # def visit(self, node: AndOperator):
    #     pass

    # @visitor.when(OrOperator)
    # def visit(self, node: OrOperator):
    #     pass

    # @visitor.when(NotOperator)
    # def visit(self, node: NotOperator):
    #     pass

    # @visitor.when(GreaterCondition)
    # def visit(self, node: GreaterCondition):
    #     pass

    # @visitor.when(MenorCondition)
    # def visit(self, node: MenorCondition):
    #     pass

    # @visitor.when(EqualCondition)
    # def visit(self, node: EqualCondition):
    #     pass

    # @visitor.when(SumExpression)
    # def visit(self, node: SumExpression):
    #     pass

    # @visitor.when(SubExpression)
    # def visit(self, node: SubExpression):
    #     pass

    # @visitor.when(MulTerm)
    # def visit(self, node: MulTerm):
    #     pass

    # @visitor.when(DivTerm)
    # def visit(self, node: DivTerm):
    #     pass

    # @visitor.when(Pow)
    # def visit(self, node: Pow):
    #     pass

    # @visitor.when(Factor)
    # def visit(self, node: Factor):
    #     pass

    # @visitor.when(Function)
    # def visit(self, node: Function):
    #     pass

    # @visitor.when(CallShapeInstruction)
    # def visit(self, node: CallShapeInstruction):
    #     pass

    # @visitor.when(CallRuleInstruction)
    # def visit(self, node: CallRuleInstruction):
    #     pass

    @visitor.when(ContextNode)
    def visit(self, node: ContextNode, tabs=0):
        ans = S*tabs + f"{node.__class__.__name__}"
        return ans
