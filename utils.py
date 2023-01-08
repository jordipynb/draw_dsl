import abc
from dataclasses import dataclass, field
import enum
from lexer import *

from ply.lex import LexToken
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


@dataclass
class Node(abc.ABC):
    pass


class ContextNode(Node):
    pass


class Instruction(ContextNode):
    pass


class Expression(ContextNode):
    pass


@dataclass
class Rule(ContextNode):
    name: str
    param: str
    instructions: list[Instruction]


@dataclass
class Axiom(ContextNode):
    instructions: list[Instruction]


@dataclass
class Factor(Expression):
    ID: LexToken


class Value(Factor):
    # value: float
    def __init__(self, value):
        self.value = value


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


@dataclass
class Nill(ContextNode):
    pass


@dataclass
class Rule(ContextNode):
    name: str
    param: str
    instructions: list[Instruction]
    token: LexToken = None


@dataclass
class Axiom(ContextNode):
    instructions: list[Instruction]


@dataclass
class Break(Instruction):
    token: LexToken


@dataclass
class Draw(Node):
    shape: Shape
    x: Value
    y: Value


@dataclass
class Scene(Node):
    draws: list[Draw]


@dataclass
class LeftInstruction(Instruction):
    expression: Expression


@dataclass
class RightInstruction(Instruction):
    expression: Expression


@dataclass
class LineInstruction(Instruction):
    expression: Expression


@dataclass
class PushInstruction(Instruction):
    pass


@dataclass
class PopInstruction(Instruction):
    pass


@dataclass
class JumpInstruction(Instruction):
    exp1: Expression
    exp2: Expression


@dataclass
class Assign(Instruction):
    ID: str
    expression: Expression


@dataclass
class SetX(Instruction):
    expression: Expression


@dataclass
class SetY(Instruction):
    expression: Expression


class GetX(Instruction):
    def __init__(self, ID):
        self.ID = ID


class GetY(Instruction):
    def __init__(self, ID):
        self.ID = ID


class SetPencil(Instruction):
    def __init__(self, ID):
        self.ID = ID


@dataclass
class If(Instruction):
    condition: Expression
    if_body: list[Instruction]
    else_body: list[Instruction] = None


@dataclass
class While(Instruction):
    condition: Expression
    body: list[Instruction]


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


class FalseCondition(Factor):
    def __init__(self):
        pass


class AndCondition(BinaryExpr):
    pass


class OrCondition(BinaryExpr):
    pass


@dataclass
class NotCondition(Expression):
    expr: Expression


class GreaterCondition(BinaryExpr):
    pass


class MenorCondition(BinaryExpr):
    pass


class EqualCondition(BinaryExpr):
    pass


class SumExpr(BinaryExpr):
    pass


class SubExpr(BinaryExpr):
    pass


class MultExpr(BinaryExpr):
    pass


class DivExpr(BinaryExpr):
    pass


class PowExpr(BinaryExpr):
    pass


@dataclass
class Function(Instruction):
    func: str
    expression: Expression
    token: LexToken


@dataclass
class CallShapeInstruction(Instruction):
    shape: Shape


@dataclass
class CallRuleInstruction(Instruction):
    token: LexToken
    expression: Expression
    id: str = field(init=False)

    def __post_init__(self):
        self.id = self.token.value