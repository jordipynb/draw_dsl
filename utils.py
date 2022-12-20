import turtle
import _tkinter

from ply.lex import LexToken

stack:list = []
class Node:
    def evaluate(self):
        raise NotImplementedError()

class NodeContext(Node):
    def evaluate(self, ttle:turtle.Turtle):
        raise NotImplementedError()

class NodeInstruction(Node):
    def evaluate(self, ttle:turtle.Turtle, depth:int):
        raise NotImplementedError()

class Scene(Node):
    def __init__(self, draws, error_list):
        self.draws:list[Draw] = draws
        self.error_list:list = error_list

    def evaluate(self):
        try:
            for draw in self.draws:
                draw.evaluate()
            turtle.done()
        except turtle.Terminator: pass
        except _tkinter.TclError: pass

class Axiom(NodeContext):
    def __init__(self, instructions:list[NodeInstruction]):
        self.instructions = instructions

    def evaluate(self, ttle):
        for elem in self.instructions:
            elem.evaluate(ttle, 0)

class Rule(NodeInstruction):
    def __init__(self, name:str, base:list[NodeInstruction], instructions:list[NodeContext], loop:int):
        self.name = name
        self.base = base
        self.instructions = instructions
        self.loop = loop

    def evaluate(self, ttle:turtle.Turtle, depth:int):
        if depth == 0:
            for elem in self.base:
                elem.evaluate(ttle, depth)
        else:
            for i in range(self.loop+1):
                for elem in self.instructions:
                    elem.evaluate(ttle, depth - 1)

class Shape(NodeContext):
    def __init__(self, name:str, pencil:str, axiom:Axiom):
        self.stack = []
        self.name = name
        self.pencil = pencil
        self.axiom = axiom

    def evaluate(self, ttle):
        ttle.pencolor(self.pencil)
        self.axiom.evaluate(ttle)

class Draw(Node):
    def __init__(self, shape:Shape, x=0, y=0):
        self.shape = shape
        self.x = x
        self.y = y 

    def evaluate(self):
        ttle = turtle.Turtle()
        ttle.left(90)
        ttle.up()
        ttle.goto(self.x, self.y)
        ttle.down()
        ttle.speed(0)
        ttle.pensize(2)
        self.shape.evaluate(ttle)
        ttle.hideturtle()

class LeftInstruction(NodeInstruction):
    def __init__(self, angle:int):
        self.angle = angle

    def evaluate(self, ttle, depth):
        ttle.left(self.angle)

class RightInstruction(NodeInstruction):
    def __init__(self, angle:int):
        self.angle = angle

    def evaluate(self, ttle, depth):
        ttle.right(self.angle)

class LineInstruction(NodeInstruction):
    def __init__(self, distance:int):
        self.distance = distance

    def evaluate(self, ttle, depth):
        ttle.forward(self.distance)

class PushInstruction(NodeInstruction):
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

    def evaluate(self, ttle, depth):
        stack.append((self.x, self.y))

class PopInstruction(NodeInstruction):
    def __init__(self):
        pass

    def evaluate(self, ttle, depth):
        x,y = stack.pop()
        jmp = JumpInstruction(x, y)
        jmp.evaluate(ttle, depth)

class JumpInstruction(NodeInstruction):
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

    def evaluate(self, ttle, depth):
        ttle.up()
        ttle.goto(self.x, self.y)
        ttle.down()

class Nill(NodeInstruction):
    def __init__(self):
        pass

    def evaluate(self, ttle, depth=0):
        pass

class CallShapeInstruction(NodeInstruction):
    def __init__(self, shape:Shape):
        self.shape = shape

    def evaluate(self, ttle, depth):
        self.shape.evaluate(ttle)

class CallRuleInstruction(NodeInstruction):
    def __init__(self, rule:Rule, depth=-1):
        self.rule =  rule
        self.depth = depth

    def evaluate(self, ttle, depth):
        if self.depth == -1: # instruccion recursiva
            self.rule.evaluate(ttle, depth + 1)
        else: # primera llamada a la instruccion
            self.rule.evaluate(ttle, self.depth)

class CallableRule(Node):
    def __init__(self, token:LexToken):
        self.token = token

    def search_rule(self, locals_rule:list[Rule]):
        for rule in locals_rule:
            if self.token.value == rule.name:
                return rule
        return self.token