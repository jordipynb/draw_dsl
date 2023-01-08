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
        if node.draws:
            for draw in node.draws:
                self.visit(draw)

    @visitor.when(Draw)
    def visit(self, node: Draw):
        self.visit(node.shape)

    @visitor.when(Shape)
    def visit(self, node: Shape):
        if node.rules:
            for rule in node.rules:
                self.visit(rule)

    @visitor.when(Rule)
    def visit(self, node: Rule):
        self.scope.define_rule(node.name, node.param)