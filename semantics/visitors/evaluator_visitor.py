import turtle
import _tkinter
import exceptions
from ply.lex import LexToken
from lexer import *

from semantics import visitor
from utils import *

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

class EvalVisitor:
    def __init__(self):
        self.errors = []
        
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(Rule)
    def visit(self, node: Rule, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        for elem in node.instructions:
            self.visit(elem, ttle, context, scope)
            
    @visitor.when(Axiom)
    def visit(self, node: Axiom, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        context = Context()
        for elem in node.instructions:
            self.visit(elem, ttle, context, scope)
            
    @visitor.when(Factor)
    def visit(self, node: Factor, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        return context.search(node.ID)
    
    @visitor.when(Value)
    def visit(self, node: Value, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        return node.value
    
    @visitor.when(Shape)
    def visit(self, node: Shape, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        if node.rules:
            for rule in node.rules:
                node.scope[rule.name] = rule
        try:
            ttle.pencolor(node.pencil)
        except turtle.TurtleGraphicsError:

            print(exceptions.ColorNotDefined(node.pencil).runtime_error)
            raise exceptions.EmptyError()
        self.visit(node.axiom, ttle, scope=node.scope)

    @visitor.when(Nill)
    def visit(self, node: Nill, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        pass
    
    @visitor.when(Rule)
    def visit(self, node: Rule, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        for elem in node.instructions:
            self.visit(elem, ttle, context, scope)
            
    @visitor.when(Axiom)
    def visit(self, node: Axiom, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        context = Context()
        for elem in node.instructions:
            self.visit(elem, ttle, context, scope)
            
    @visitor.when(Break)
    def visit(self, node: Break, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        return node
    
    @visitor.when(Draw)
    def visit(self, node: Draw, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        ttle = turtle.Turtle()
        ttle.left(90)
        ttle.up()
        ttle.goto(self.visit(node.x, ttle), self.visit(node.y, ttle))
        ttle.down()
        ttle.speed(0)
        ttle.pensize(2)
        if isinstance(node.shape, LexToken):
            print(exceptions.ShapeNotDefined(node.shape))
            raise exceptions.EmptyError("")
        self.visit(node.shape, ttle)
        ttle.hideturtle()
        
    @visitor.when(Scene)
    def visit(self, node: Scene, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        try:
            for draw in node.draws:
                self.visit(draw, ttle)
            turtle.done()
        except turtle.Terminator:
            pass
        except _tkinter.TclError:
            pass
        except exceptions.EmptyError:
            pass
        
    @visitor.when(LeftInstruction)
    def visit(self, node: LeftInstruction, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        angle = self.visit(node.expression, ttle, context, scope)
        ttle.left(angle)
        
    @visitor.when(RightInstruction)
    def visit(self, node: RightInstruction, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        angle = self.visit(node.expression, ttle, context, scope)
        ttle.right(angle)
        
    @visitor.when(LineInstruction)
    def visit(self, node: LineInstruction, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        distance = self.visit(node.expression, ttle, context, scope)
        ttle.forward(distance)
        
    @visitor.when(PushInstruction)
    def visit(self, node: PushInstruction, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        stack.append((ttle.xcor(), ttle.ycor(), ttle.heading()))
    
    @visitor.when(PopInstruction)
    def visit(self, node: PopInstruction, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        pos_x, pos_y, angle = stack.pop()
        ttle.up()
        ttle.goto(pos_x, pos_y)
        ttle.setheading(angle)
        ttle.down()
        
    @visitor.when(JumpInstruction)
    def visit(self, node: JumpInstruction, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        ttle.up()
        x = self.visit(node.exp1, ttle, context, scope)
        y = self.visit(node.exp2, ttle, context, scope)
        ttle.goto(x, y)
        ttle.down()
        
    @visitor.when(Assign)
    def visit(self, node: Assign, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        name = node.ID
        value = self.visit(node.expression, ttle, context, scope)
        if not context.set_value(name, value):
            context.locals[name] = value
            
    @visitor.when(SetX)
    def visit(self, node: SetX, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        ttle.setx(self.visit(node.expression, ttle, context, scope))

    @visitor.when(SetY)
    def visit(self, node: SetY, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        ttle.sety(self.visit(node.expression, ttle, context, scope))

    @visitor.when(GetX)
    def visit(self, node: GetX, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        name = node.ID
        value = ttle.xcor()
        if not context.set_value(name, value):
            context.locals[name] = value

    @visitor.when(GetY)
    def visit(self, node: GetY, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        name = node.ID
        value = ttle.ycor()
        if not context.set_value(name, value):
            context.locals[name] = value
            
    @visitor.when(SetPencil)
    def visit(self, node: SetPencil, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        try:
            ttle.pencolor(node.ID)
        except turtle.TurtleGraphicsError:
            print(exceptions.ColorNotDefined(node.pencil).runtime_error)
            raise exceptions.EmptyError()
        
    @visitor.when(If)
    def visit(self, node: If, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        context = context.create_children()
        if self.visit(node.condition, ttle, context, scope):
            for instruction in node.if_body:
                result = self.visit(instruction, ttle, context, scope)
                if isinstance(result, Break):
                    return result
        elif node.else_body:
            for instruction in node.else_body:
                result = self.visit(instruction, ttle, context, scope)
                if isinstance(result, Break):
                    return result

    @visitor.when(While)
    def visit(self, node: While, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        context = context.create_children()
        while self.visit(node.condition, ttle, context, scope):
            for instruction in node.body:
                if isinstance(instruction, Break) or isinstance(self.visit(instruction, ttle, context, scope), Break):
                    return
                
    @visitor.when(TrueCondition)
    def visit(self, node: TrueCondition, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        return True
    
    @visitor.when(FalseCondition)
    def visit(self, node: FalseCondition, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        return False

    @visitor.when(AndCondition)
    def visit(self, node: AndCondition, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        return self.visit(node.left, ttle, context, scope) and self.visit(node.right, ttle, context, scope)

    @visitor.when(OrCondition)
    def visit(self, node: OrCondition, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        return self.visit(node.left, ttle, context, scope) or self.visit(node.right, ttle, context, scope)

    @visitor.when(NotCondition)
    def visit(self, node: NotCondition, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        return not self.visit(node.expr, ttle, context, scope)

    @visitor.when(GreaterCondition)
    def visit(self, node: GreaterCondition, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        return self.visit(node.left, ttle, context, scope) > self.visit(node.right, ttle, context, scope)

    @visitor.when(MenorCondition)
    def visit(self, node: MenorCondition, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        return self.visit(node.left, ttle, context, scope) < self.visit(node.right, ttle, context, scope)

    @visitor.when(EqualCondition)
    def visit(self, node: EqualCondition, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        return self.visit(node.left, ttle, context, scope) == self.visit(node.right, ttle, context, scope)

    @visitor.when(SumExpr)
    def visit(self, node: SumExpr, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        return self.visit(node.left, ttle, context, scope) + self.visit(node.right, ttle, context, scope)

    @visitor.when(SubExpr)
    def visit(self, node: SubExpr, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        return self.visit(node.left, ttle, context, scope) - self.visit(node.right, ttle, context, scope)

    @visitor.when(MultExpr)
    def visit(self, node: MultExpr, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        return self.visit(node.left, ttle, context, scope) * self.visit(node.right, ttle, context, scope)

    @visitor.when(DivExpr)
    def visit(self, node: DivExpr, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        return self.visit(node.left, ttle, context, scope) / self.visit(node.right, ttle, context, scope)

    @visitor.when(PowExpr)
    def visit(self, node: PowExpr, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        return math.pow(self.visit(node.left, ttle, context, scope), self.visit(node.right, ttle, context, scope))

    @visitor.when(Function)
    def visit(self, node: Function, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        expresion = self.visit(node.expression, ttle, context, scope)
        return node.func(expresion)
    
    @visitor.when(CallShapeInstruction)
    def visit(self, node: CallShapeInstruction, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        self.visit(node.shape, ttle)
        
    @visitor.when(CallRuleInstruction)
    def visit(self, node: CallRuleInstruction, ttle: turtle.Turtle, context: Context = None, scope: dict = None):
        depth = self.visit(node.expression, ttle, context)
        try:
            rule = scope[node.id]
        except KeyError:
            print(exceptions.RuleNotDefined(node.token))
            raise exceptions.EmptyError()
        new_context = Context()
        new_context.locals[rule.param] = depth
        self.visit(rule, ttle, new_context, scope)