import abc
from dataclasses import dataclass, field
import enum
import turtle
import _tkinter
import exceptions
from ply.lex import LexToken
from lexer import *

stack: list = []
lexer = lex.lex()


def find_column(token):
    last_cr = token.lexer.lexdata.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos - last_cr)
    return column


def token_info(token: LexToken):
    value = token.value
    line = token.lineno
    column = find_column(token)
    return value, line, column


class Context:
    def __init__(self, parent=None):
        self.locals = {}
        self.parent: Context = parent

    def create_children(self):
        return Context(self)

    def search(self, token: LexToken):
        for vname, value in self.locals.items():
            if vname == token.value:
                return value
        if self.parent is None:
            print(exceptions.IdentifierNotDefined(token))
            raise exceptions.EmptyError("")
        return self.parent.search(token)

    def set_value(self, name, value):
        if name in self.locals.keys():
            self.locals[name] = value
            return True
        if self.parent:
            return self.parent.set_value(name, value)
        return False


@dataclass
class Node(abc.ABC):
    def evaluate(self):
        raise NotImplementedError()


class ContextNode(Node):
    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        raise NotImplementedError()


class Instruction(ContextNode):
    pass


class Expression(ContextNode):
    pass


@dataclass
class Rule(ContextNode):
    name: str
    param: str
    instructions: list[Instruction]

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        for elem in self.instructions:
            elem.evaluate(ttle, context, scope)


@dataclass
class Axiom(ContextNode):
    instructions: list[Instruction]

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        context = Context()
        for elem in self.instructions:
            elem.evaluate(ttle, context, scope)


@dataclass
class Factor(Expression):
    ID: LexToken

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict[str, Rule] = None):
        return context.search(self.ID)


class Value(Factor):
    # value: float
    def __init__(self, value):
        self.value = value

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict[str, Rule] = None):
        return self.value


@dataclass
class Shape(ContextNode):
    name: str
    pencil: str
    rules: list[Rule]
    axiom: Axiom
    stack: list = field(init=False)
    scope: dict = field(init=False)

    def __post_init__(self):
        self.stack = []
        self.scope = {}

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        if self.rules:
            for rule in self.rules:
                self.scope[rule.name] = rule
        try:
            ttle.pencolor(self.pencil)
        except turtle.TurtleGraphicsError:

            print(exceptions.ColorNotDefined(self.pencil).runtime_error)
            raise exceptions.EmptyError()
        self.axiom.evaluate(ttle, scope=self.scope)


@dataclass
class Nill(ContextNode):
    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict[str, Rule] = None):
        pass


@dataclass
class Rule(ContextNode):
    name: str
    param: str
    instructions: list[Instruction]
    token: LexToken = None

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        for elem in self.instructions:
            elem.evaluate(ttle, context, scope)


@dataclass
class Axiom(ContextNode):
    instructions: list[Instruction]

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        context = Context()
        for elem in self.instructions:
            elem.evaluate(ttle, context, scope)


@dataclass
class Break(Instruction):
    token: LexToken

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict[str, Rule] = None):
        return self


@dataclass
class Draw(Node):
    shape: Shape
    x: Value
    y: Value

    def evaluate(self):
        ttle = turtle.Turtle()
        ttle.left(90)
        ttle.up()
        ttle.goto(self.x.evaluate(ttle), self.y.evaluate(ttle))
        ttle.down()
        ttle.speed(0)
        ttle.pensize(2)
        if isinstance(self.shape, LexToken):
            # print(f'SemanticError: "{self.shape.value}" no es una figura definida')
            print(exceptions.ShapeNotDefined(self.shape))
            raise exceptions.EmptyError("")
        self.shape.evaluate(ttle)
        ttle.hideturtle()


@dataclass
class Scene(Node):
    draws: list[Draw]

    def evaluate(self):
        try:
            for draw in self.draws:
                draw.evaluate()
            turtle.done()
        except turtle.Terminator:
            pass
        except _tkinter.TclError:
            pass
        except exceptions.EmptyError:
            pass


@dataclass
class LeftInstruction(Instruction):
    expression: Expression

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict[str, Rule] = None):
        angle = self.expression.evaluate(ttle, context, scope)
        ttle.left(angle)


@dataclass
class RightInstruction(Instruction):
    expression: Expression

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        angle = self.expression.evaluate(ttle, context, scope)
        ttle.right(angle)


@dataclass
class LineInstruction(Instruction):
    expression: Expression

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        distance = self.expression.evaluate(ttle, context, scope)
        ttle.forward(distance)


@dataclass
class PushInstruction(Instruction):

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        stack.append((ttle.xcor(), ttle.ycor(), ttle.heading()))


@dataclass
class PopInstruction(Instruction):

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        pos_x, pos_y, angle = stack.pop()
        ttle.up()
        ttle.goto(pos_x, pos_y)
        ttle.setheading(angle)
        ttle.down()


@dataclass
class JumpInstruction(Instruction):
    exp1: Expression
    exp2: Expression

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict[str, Rule] = None):
        ttle.up()
        x = self.x.evaluate(ttle, context, scope)
        y = self.y.evaluate(ttle, context, scope)
        ttle.goto(x, y)
        ttle.down()


@dataclass
class Assign(Instruction):
    ID: str
    expression: Expression

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict[str, Rule] = None):
        name = self.ID
        value = self.expression.evaluate(ttle, context, scope)
        if not context.set_value(name, value):
            context.locals[name] = value


@dataclass
class SetX(Instruction):
    expression: Expression

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict[str, Rule] = None):
        ttle.setx(self.expression.evaluate(ttle, context, scope))


@dataclass
class SetY(Instruction):
    expression: Expression

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict[str, Rule] = None):
        ttle.sety(self.expression.evaluate(ttle, context, scope))


class GetX(Instruction):
    def __init__(self, ID):
        self.ID = ID

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict[str, Rule] = None):
        name = self.ID
        value = ttle.xcor()
        if not context.set_value(name, value):
            context.locals[name] = value


class GetY(Instruction):
    def __init__(self, ID):
        self.ID = ID

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict[str, Rule] = None):
        name = self.ID
        value = ttle.ycor()
        if not context.set_value(name, value):
            context.locals[name] = value


class SetPencil(Instruction):
    def __init__(self, ID):
        self.ID = ID

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict[str, Rule] = None):
        try:
            ttle.pencolor(self.ID)
        except turtle.TurtleGraphicsError:
            print(exceptions.ColorNotDefined(self.pencil).runtime_error)
            raise exceptions.EmptyError()


@dataclass
class If(Instruction):
    condition: Expression
    if_body: list[Instruction]
    else_body: list[Instruction] = None

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict[str, Rule] = None):
        context = context.create_children()
        if self.condition.evaluate(ttle, context, scope):
            for instruction in self.if_body:
                result = instruction.evaluate(ttle, context, scope)
                if isinstance(result, Break):
                    return result
        elif self.else_body:
            for instruction in self.else_body:
                result = instruction.evaluate(ttle, context, scope)
                if isinstance(result, Break):
                    return result


@dataclass
class While(Instruction):
    condition: Expression
    body: list[Instruction]

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict[str, Rule] = None):
        context = context.create_children()
        while self.condition.evaluate(ttle, context, scope):
            for instruction in self.body:
                if isinstance(instruction, Break) or isinstance(instruction.evaluate(ttle, context, scope), Break):
                    return


class Operator(enum.Enum):
    Add: enum.auto()
    Sub: enum.auto()
    Mult: enum.auto()
    Div: enum.auto()
    Pow: enum.auto()
    And: enum.auto()
    Or: enum.auto()
    Not: enum.auto()
    GreaterThan: enum.auto()
    LessThan: enum.auto()
    EqualEqual: enum.auto()


@dataclass
class BinaryExpr(Expression):
    left: Expression
    right: Expression
    operator: Operator = None


class TrueCondition(Factor):

    def __init__(self):
        pass

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict[str, Rule] = None):
        return True


class FalseCondition(Factor):
    def __init__(self):
        pass

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict[str, Rule] = None):
        return False


class AndCondition(BinaryExpr):
    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict[str, Rule] = None):
        return self.left.evaluate(ttle, context, scope) and self.right.evaluate(ttle, context, scope)


class OrCondition(BinaryExpr):
    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict[str, Rule] = None):
        return self.left.evaluate(ttle, context, scope) or self.right.evaluate(ttle, context, scope)


@dataclass
class NotCondition(Expression):
    expr: Expression

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict[str, Rule] = None):
        return not self.expr.evaluate(ttle, context, scope)


class GreaterCondition(BinaryExpr):
    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict[str, Rule] = None):
        return self.left.evaluate(ttle, context, scope) > self.right.evaluate(ttle, context, scope)


class MenorCondition(BinaryExpr):
    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict[str, Rule] = None):
        return self.left.evaluate(ttle, context, scope) < self.right.evaluate(ttle, context, scope)


class EqualCondition(BinaryExpr):

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict[str, Rule] = None):
        return self.left.evaluate(ttle, context, scope) == self.right.evaluate(ttle, context, scope)


class SumExpr(BinaryExpr):

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict[str, Rule] = None):
        return self.left.evaluate(ttle, context, scope) + self.right.evaluate(ttle, context, scope)


class SubExpr(BinaryExpr):
    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict[str, Rule] = None):
        return self.left.evaluate(ttle, context, scope) - self.right.evaluate(ttle, context, scope)


class MultExpr(BinaryExpr):

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict[str, Rule] = None):
        return self.left.evaluate(ttle, context, scope) * self.right.evaluate(ttle, context, scope)


class DivExpr(BinaryExpr):

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict[str, Rule] = None):
        return self.left.evaluate(ttle, context, scope) / self.right.evaluate(ttle, context, scope)


class PowExpr(BinaryExpr):

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict[str, Rule] = None):
        return math.pow(self.left.evaluate(ttle, context, scope), self.right.evaluate(ttle, context, scope))


@dataclass
class Function(Instruction):
    func: str
    expression: Expression
    token: LexToken

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict[str, Rule] = None):
        return self.func(self.expression.evaluate(ttle, context, scope))


@dataclass
class CallShapeInstruction(Instruction):
    shape: Shape

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict[str, Rule] = None):
        self.shape.evaluate(ttle)


@dataclass
class CallRuleInstruction(Instruction):
    token: LexToken
    expression: Expression
    id: str = field(init=False)

    def __post_init__(self):
        self.id = self.token.value

    def evaluate(self, ttle: turtle.Turtle, context: Context = None, scope: dict[str, Rule] = None):
        depth = self.expression.evaluate(ttle, context)
        try:
            rule = scope[self.id]
        except KeyError:
            print(exceptions.RuleNotDefined(self.token))
            raise exceptions.EmptyError()
        new_context = Context()
        new_context.locals[rule.param] = depth
        rule.evaluate(ttle, new_context, scope)
