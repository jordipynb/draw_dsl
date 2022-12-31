from semantics import visitor
from utils import Axiom, Rule, Scene, Draw, Shape, Value
S = '|  '
class FormatVisitor(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(Scene)
    def visit(self, node, tabs=0):
        ans = S * tabs + f'Scene:'
        draws = '\n'.join(self.visit(draw, tabs + 1) for draw in node.draws)
        return f'{ans}\n{draws}'

    @visitor.when(Draw)
    def visit(self, node, tabs=0):
        ans = S * tabs + f'Draw:'
        expr = self.visit(node.shape, tabs + 1)
        x_value = self.visit(node.x, tabs + 1, 'X')
        y_value = self.visit(node.y, tabs + 1, 'Y')
        childs = "\n".join([expr, x_value, y_value])
        return f'{ans}\n{childs}'

    @visitor.when(Shape)
    def visit(self, node, tabs=0):
        ans = S*tabs + f'Shape:'
        name = S*(tabs+1) + f'name: {node.name}'
        pencil = S*(tabs+1) + f'pencil: {node.pencil}'
        rules = '\n'.join(self.visit(rule, tabs + 1) for rule in node.rules)
        axiom = self.visit(node.axiom, tabs + 1)
        properties = "\n".join([name, pencil, rules, axiom])
        return f'{ans}\n{properties}'

    @visitor.when(Value)
    def visit(self, node, tabs=0, header=''):
        ans = S*tabs + f'{header}: {node.value}'
        return f'{ans}'
    
    @visitor.when(Rule)
    def visit(self, node, tabs=0):
        ans = S*tabs + f'Rule:'
        name = S*(tabs+1) + f'name: {node.name}'
        param = S*(tabs+1) + f'param: {node.param}'
        properties = "\n".join([name, param])
        return f'{ans}\n{properties}'
    
    @visitor.when(Axiom)
    def visit(self, node, tabs=0):
        ans = S*tabs + f'axiom'
        return f'{ans}'