import turtle
import _tkinter

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

class Axiom(NodeContext):
    def __init__(self, instructions:list[NodeContext], rules:list[NodeContext], depth:int = 0):
        self.instructions = instructions
        self.rules = rules
        self.depth = depth

    def evaluate(self, ttle):
        # evaluar en el depth
        for elem in self.instructions:
            pass

class Rule(NodeInstruction):
    def __init__(self, name:str, base:list[NodeContext], instructions:list[NodeContext], loop:int):
        self.name = name
        self.base = base
        self.instructions = instructions
        self.loop = loop

    def evaluate(self, ttle:turtle.Turtle, depth:int):
        for i in range(self.loop+1):
            for elem in self.instructions:
                elem.evaluate(ttle)
        

class Scene(Node):
    def __init__(self, draws):
        self.draws:list[Draw] = draws

    def evaluate(self):
        try:
            for draw in self.draws:
                draw.evaluate()
            turtle.done()
        except turtle.Terminator: pass
        except _tkinter.TclError: pass

class Shape(NodeContext):
    def __init__(self, name:str, pencil:str, fill:str, axiom:Axiom):
        self.stack = []
        self.name = name
        self.pencil = pencil
        self.fill = fill
        self.axiom = axiom

    def evaluate(self, ttle):
        ttle.pencolor(self.pencil)
        ttle.fillcolor(self.fill)
        self.axiom.evaluate(ttle)

class Draw(Node):
    def __init__(self, shape:Shape, x=0, y=0):
        self.shape = shape
        self.x = x
        self.y = y 

    def evaluate(self):
        ttle = turtle.Turtle()
        ttle.up()
        ttle.goto(self.x, self.y)
        ttle.down()
        ttle.speed(2)
        ttle.pensize(2)
        self.shape.evaluate(ttle)
        ttle.hideturtle()

class LeftInstruction(NodeContext):
    def __init__(self, angle:int):
        self.angle = angle

    def evaluate(self, ttle):
        ttle.left(self.angle)

class RightInstruction(NodeContext):
    def __init__(self, angle:int):
        self.angle = angle

    def evaluate(self, ttle):
        ttle.right(self.angle)

class LineInstruction(NodeContext):
    def __init__(self, distance:int):
        self.distance = distance

    def evaluate(self, ttle):
        ttle.forward(self.distance)

class PushInstruction(NodeContext):
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

    def evaluate(self, ttle):
        stack.append((self.x, self.y))

class PopInstruction(NodeContext):
    def __init__(self):
        pass

    def evaluate(self, ttle):
        x,y = stack.pop()
        jmp = JumpInstruction(x, y)
        jmp.evaluate(ttle)

class JumpInstruction(NodeContext):
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

    def evaluate(self, ttle):
        ttle.up()
        ttle.goto(self.x, self.y)
        ttle.down()

class Nill(NodeContext):
    def __init__(self):
        pass

    def evaluate(self, ttle):
        pass

class CallShapeInstruction(NodeContext):
    def __init__(self, shape:Shape):
        self.shape = shape

    def evaluate(self, ttle):
        self.shape.evaluate(ttle)

class CallRuleInstruction(NodeContext):
    def __init__(self, rule:Rule|str, pos_line:int = 0, pos_column:int = 0):
        self.rule =  rule

    def evaluate(self, ttle):
        self.rule.evaluate(ttle)