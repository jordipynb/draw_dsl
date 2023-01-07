from semantics import visitor
from semantics.scope import Scope
from semantics.visitors.type_collector import RuleShapeCollector
from utils import *


class ContextValidatorVisitor(object):
    def __init__(self):
        self.errors = []
        
    @property
    def show_errors(self):
        print('\n'.join(set(self.errors)))

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(Scene)
    def visit(self, node: Scene, scope: Scope=None):
        scope = RuleShapeCollector(node).scope
        for draw in node.draws:
            self.visit(draw, scope)

    @visitor.when(Draw)
    def visit(self, node: Draw, scope: Scope=None):
        self.visit(node.shape, scope)

    @visitor.when(Shape)
    def visit(self, node: Shape, scope: Scope):
        for rule in node.rules:
            self.visit(rule, scope)
        self.visit(node.axiom, scope)

    # @visitor.when(Nill)
    # def visit(self, node: Nill, scope: Scope):
    #     pass

    @visitor.when(Rule)
    def visit(self, node: Rule, scope: Scope):
        nscope = scope.create_child_scope()
        nscope.define_var(node.param)
        for instruction in node.instructions:
            self.visit(instruction, nscope)

    @visitor.when(Axiom)
    def visit(self, node: Axiom, scope: Scope):
        nscope = scope.create_child_scope()
        for instruction in node.instructions:
            self.visit(instruction, nscope)

    ## ++++++++++++++++++++ Instructions ++++++++++++++++++++##

    @visitor.when(JumpInstruction)
    def visit(self, node: JumpInstruction, scope: Scope):
        self.visit(node.x, scope)
        self.visit(node.y, scope)
        
    @visitor.when(LeftInstruction)
    def visit(self, node: LeftInstruction, scope: Scope):
        self.visit(node.expression, scope)

    @visitor.when(RightInstruction)
    def visit(self, node: RightInstruction, scope: Scope):
        self.visit(node.expression, scope)

    @visitor.when(LineInstruction)
    def visit(self, node: LineInstruction, scope: Scope):
        self.visit(node.expression, scope)

    # @visitor.when(PushInstruction)
    # def visit(self, node: PushInstruction, scope: Scope):
    #     pass

    # @visitor.when(PopInstruction)
    # def visit(self, node: PopInstruction, scope: Scope):
    #     pass

    

    @visitor.when(Assign)
    def visit(self, node: Assign, scope: Scope):
        scope.define_var(node.ID)
        self.visit(node.expression, scope) # Creo que aqui puede haber un posible error semantico

    @visitor.when(SetX)
    def visit(self, node: SetX, scope: Scope):
        self.visit(node.expression, scope)

    @visitor.when(SetY)
    def visit(self, node: SetY, scope: Scope):
        self.visit(node.expression,scope)

    @visitor.when(GetX)
    def visit(self, node: GetX, scope: Scope):
        scope.define_var(node.ID)

    @visitor.when(GetY)
    def visit(self, node: GetY, scope: Scope):
        scope.define_var(node.ID)

    # @visitor.when(SetPencil)
    # def visit(self, node: SetPencil, scope: Scope):
    #     pass

    @visitor.when(If)
    def visit(self, node: If, scope: Scope):
        self.visit(node.condition, scope)  # Aqui pueden haber problemas con la condicion
        nscope = scope.create_child_scope()
        for instruction in node.if_body:
            self.visit(instruction, nscope)
        if node.else_body:
            for instruction in node.else_body:
                self.visit(instruction, nscope)

    @visitor.when(While)
    def visit(self, node: While, scope: Scope):
        self.visit(node.condition, scope)  # Aqui pueden haber problemas con la condicion
        nscope = scope.create_child_scope()
        nscope.define_loop()
        for instruction in node.body:
            self.visit(instruction, nscope)
        nscope.undefine_loop()
    
    @visitor.when(Break)
    def visit(self, node: Break, scope: Scope):
        if not scope.inside_loop:
            self.errors.append("Break no puede usarse fuera de un ciclo")

    @visitor.when(CallShapeInstruction)
    def visit(self, node: CallShapeInstruction, scope: Scope):
        if node.shape:
            name = node.shape.name
            if not scope.exist_shape(name):
                self.errors.append(f"No existe shape con nombre: {name}")

    @visitor.when(CallRuleInstruction)
    def visit(self, node: CallRuleInstruction, scope: Scope):
        if not scope.parent.exist_rule(node.id):
            self.errors.append(f"No existe a regla con nombre {node.id}")
        self.visit(node.expression, scope)

    # @visitor.when(Instruction)
    # def visit(self, node: Instruction, scope: Scope):
    #     raise node

    ## ++++++++++++++++++++ Expressions ++++++++++++++++++++##

    @visitor.when(AndCondition)
    def visit(self, node: AndCondition, scope: Scope):
        self.visit(node.left, scope)
        self.visit(node.right, scope)

    @visitor.when(OrCondition)
    def visit(self, node: OrCondition, scope: Scope):
        self.visit(node.left, scope)
        self.visit(node.right, scope)

    @visitor.when(NotCondition)
    def visit(self, node: NotCondition, scope: Scope):
        self.visit(node.expr, scope)

    @visitor.when(GreaterCondition)
    def visit(self, node: GreaterCondition, scope: Scope):
        self.visit(node.left, scope)
        self.visit(node.right, scope)

    @visitor.when(MenorCondition)
    def visit(self, node: MenorCondition, scope: Scope):
        self.visit(node.left, scope)
        self.visit(node.right, scope)

    @visitor.when(EqualCondition)
    def visit(self, node: EqualCondition, scope: Scope):
        self.visit(node.left, scope)
        self.visit(node.right, scope)

    @visitor.when(SumExpr)
    def visit(self, node: SumExpr, scope: Scope):
        self.visit(node.left, scope)
        self.visit(node.right, scope)

    @visitor.when(SubExpr)
    def visit(self, node: SubExpr, scope: Scope):
        self.visit(node.left, scope)
        self.visit(node.right, scope)

    @visitor.when(MultExpr)
    def visit(self, node: MultExpr, scope: Scope):
        self.visit(node.left, scope)
        self.visit(node.right, scope)

    @visitor.when(DivExpr)
    def visit(self, node: DivExpr, scope: Scope):
        self.visit(node.left, scope)
        self.visit(node.right, scope)

    @visitor.when(PowExpr)
    def visit(self, node: PowExpr, scope: Scope):
        self.visit(node.left, scope)
        self.visit(node.right, scope)

    @visitor.when(Function)
    def visit(self, node: Function, scope: Scope):
        if not scope.check_fun(node.func, 1): # Aqui puede haber un error
            self.errors.append(f"La funcion {node.func} no esta definida")
        self.visit(node.expression, scope)

    @visitor.when(Value)
    def visit(self, node: Value, scope: Scope):
        pass

    @visitor.when(TrueCondition)
    def visit(self, node: TrueCondition, scope: Scope):
        pass

    @visitor.when(FalseCondition)
    def visit(self, node: FalseCondition, scope: Scope):
        pass

    
    @visitor.when(Factor)
    def visit(self, node: Factor, scope: Scope):
        value, line, column = scope.token_info(node.ID)
        if not scope.check_var(value):
            self.errors.append(f'SemanticError: "{value}" en la línea {line}, columna {column} no esta definido')

    
    # @visitor.when(Expression)
    # def visit(self, node: Expression, scope: Scope):
    #     raise node
