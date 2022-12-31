from semantics import visitor
from semantics.scope import Scope
from utils import Axiom, Nill, Rule, Scene, Draw, Shape, Value
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
    
    @visitor.when(Nill)
    def visit(self, node, tabs=0):
        ans = S*tabs + f'nill'
        return f'{ans}'

    @visitor.when(Value)
    def visit(self, node, tabs=0, header=''):
        ans = S*tabs + f'{header}: {node.value}'
        return f'{ans}'
    
    @visitor.when(Rule) # Falta una parte de las reglas
    def visit(self, node, tabs=0):
        ans = S*tabs + f'Rule:'
        name = S*(tabs+1) + f'name: {node.name}'
        param = S*(tabs+1) + f'param: {node.param}'
        properties = "\n".join([name, param])
        return f'{ans}\n{properties}'
    
    @visitor.when(Axiom) # Falta este
    def visit(self, node, tabs=0):
        ans = S*tabs + f'axiom'
        return f'{ans}'
    
class SemanticCheckerVisitor(object):
    def __init__(self):
        self.errors = []
    
    @visitor.on('node')
    def visit(self, node, scope):
        pass
    
    @visitor.when(Scene)
    def visit(self, node, scope=None):
        scope = Scope(scope)
        
        for draw in node.draws:
            self.visit(draw, scope)
            
        return self.errors
    
    @visitor.when(Draw)
    def visit(self, node:Draw, scope:Scope=None):
        self.visit(node.shape, scope)
        self.visit(node.x)
        self.visit(node.y)

    @visitor.when(Shape)
    def visit(self, node:Shape, scope:Scope=None):
        if scope.is_shape_defined(node.name):
            self.errors.append("Shape %s is already defined" %(node.name))
        else:
            nscope = scope.define_shape(node.name) 
            # self.visit(node.pencil, nscope) # Definir pencil como una clase
            for rule in node.rules:
                self.visit(rule, nscope)
            self.visit(node.axiom, nscope)
    
    @visitor.when(Rule)
    def visit(self, node:Rule, scope:Scope=None):
        if scope.is_rule_defined(node.name):
            self.errors.append("Shape %s is already defined" %(node.name))
        else:
            for rule in node.rules:
                self.visit(rule, None) # No es necesario definir scope
            self.visit(node.axiom, None) # No es necesario definit scope
    