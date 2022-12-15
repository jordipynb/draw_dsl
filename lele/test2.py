import turtle

def koch_snowflake():
    axiom = "F"
    rules = {"F":"F+F--F+F"}
    iterations = 3 # TOP: 7
    angle = 60
    y_offset = -300
    main(iterations,axiom,rules,angle,y_offset=y_offset)

def quadratic_koch_island():
    axiom = "F+F+F+F"
    rules = {"F":"F-F+F+FFF-F-F+F"}
    iterations = 2 # TOP: 4
    angle = 90
    main(iterations,axiom,rules,angle)

def quadratic_snowflake():
    axiom = "F--F"
    rules = {"F":"F-F+F+F-F"}
    iterations = 4 # TOP: 6
    angle = 90
    y_offset = -300
    main(iterations,axiom,rules,angle,y_offset=y_offset)

def crystal():
    axiom = "F+F+F+F"
    rules = {"F":"FF+F++F+F"}
    iterations = 3 # TOP: 6
    angle = 90
    main(iterations,axiom,rules,angle)

def box_fractal():
    axiom = "F-F-F-F"
    rules = {"F":"F-F+F+F-F"}
    iterations = 4 # TOP: 6
    angle = 90
    y_offset = -300
    main(iterations,axiom,rules,angle,y_offset=y_offset)

def levy_c_curve():
    axiom = "F"
    rules = {"F":"+F--F+"}
    iterations = 10 # TOP: 16
    angle = 45
    main(iterations,axiom,rules,angle)

def sierpinski_arrowhead():
    axiom = "YF"
    rules = {"X":"YF+XF+Y", "Y":"XF-YF-X"}
    iterations = 5 # TOP: 10
    angle = 60
    main(iterations,axiom,rules,angle)

def sierpinski_curve():
    axiom = "F+XF+F+XF"
    rules = {"X":"XF-F+F-XF+F+XF-F+F-X"}
    iterations = 4 # TOP: 8
    angle = 90
    main(iterations,axiom,rules,angle)

def sierpinski_sieve():
    axiom = "FXF--FF--FF"
    rules = {"F":"FF", "X":"--FXF++FXF++FXF--"}
    iterations = 5 # TOP: 8
    angle = 60
    y_offset = -300
    main(iterations,axiom,rules,angle,y_offset=y_offset)

def board():
    axiom = "F+F+F+F"
    rules = {"F":"FF+F+F+F+FF"}
    iterations = 3 # TOP: 5
    angle = 90
    main(iterations,axiom,rules,angle)

def tiles():
    axiom = "F+F+F+F"
    rules = {"F":"FF+F-F+F+FF"}
    iterations = 3 # TOP: 4
    angle = 90
    main(iterations,axiom,rules,angle)

def rings():
    axiom = "F+F+F+F"
    rules = {"F":"FF+F+F+F+F+F-F"}
    iterations = 2 # TOP: 4
    angle = 90
    main(iterations,axiom,rules,angle)

def cross():
    axiom = "F+F+F+F"
    rules = {"F":"F+FF++F+F"}
    iterations = 3 # TOP: 6
    angle = 90
    main(iterations,axiom,rules,angle)

def cross_2():
    axiom = "F+F+F+F"
    rules = {"F":"F+F-F+F+F"}
    iterations = 3 # TOP: 6
    angle = 90
    main(iterations,axiom,rules,angle)

def pentaplexity():
    axiom = "F++F++F++F++F"
    rules = {"F":"F++F++F+++++F-F++F"}
    iterations = 3 # TOP: 5
    angle = 36
    main(iterations,axiom,rules,angle)

def segment_curve():
    axiom = "F+F+F+F"
    rules = {"F":"-F+F-F-F+F+FF-F+F+FF+F-F-FF+FF-FF+F+F-FF-F-F+FF-F-F+F+F-F+"}
    iterations = 2 # TOP: 3
    angle = 90
    y_offset = -300
    main(iterations,axiom,rules,angle,y_offset=y_offset)

def peano_curve():
    axiom = "F"
    rules = {"F":"F+F-F-F-F+F+F+F-F"}
    iterations = 3 # TOP: 5
    angle = 90
    y_offset = -300
    main(iterations,axiom,rules,angle,y_offset=y_offset)

def peano_gosper_curve():
    axiom = "FX"
    rules = {"X":"X+YF++YF-FX--FXFX-YF+", "Y":"-FX+YFYF++YF+FX--FX-Y"}
    iterations = 4 # TOP: 6
    angle = 60
    main(iterations,axiom,rules,angle)

def quadratic_gosper():
    axiom = "YF"
    rules = {"X": "XFX-YF-YF+FX+FX-YF-YFFX+YF+FXFXYF-FX+YF+FXFX+YF-FXYF-YF-FX+FX+YFYF-", 
             "Y": "+FXFX-YF-YF+FX+FXYF+FX-YFYF-FX-YF+FXYFYF-FX-YFFX+FX+YF-YF-FX+FX+YFY"}
    iterations = 2 # TOP: 3
    angle = 90
    main(iterations,axiom,rules,angle)

def krishna_anklets():
    axiom = " -X--X"
    rules = {"X":"XFX--XFX"}
    iterations = 4 # TOP: 9
    angle = 45
    main(iterations,axiom,rules,angle)

def moore_curve():
    axiom = "LFL-F-LFL"
    rules = {"L":"+RF-LFL-FR+", "R":"-LF+RFR+FL-"}
    iterations = 4 # TOP: 8
    angle = 90
    main(iterations,axiom,rules,angle)

def hilberts_curve():
    axiom = "L"
    rules = {"L":"+RF-LFL-FR+", "R":"-LF+RFR+FL-"}
    iterations = 4 # TOP: 9
    angle = 90
    main(iterations,axiom,rules,angle)

def hilberts_curve_2():
    axiom = "X"
    rules = {"X":"XFYFX+F+YFXFY-F-XFYFX", "Y":"YFXFY-F-XFYFX+F+YFXFY"}
    iterations = 3 # TOP: 6
    angle = 90
    y_offset = -300
    main(iterations,axiom,rules,angle,y_offset=y_offset)

def triangle():
    axiom = "F+F+F"
    rules = {"F":"F-F+F"}
    iterations = 5 # TOP: 9
    angle = 120
    main(iterations,axiom,rules,angle)

def dragon_curve():
    axiom = "FX"
    rules = {"X":"X+YF+", "Y":"-FX-Y"}
    iterations = 9 # TOP: 16
    angle = 90
    main(iterations,axiom,rules,angle)

def ter_dragon_curve():
    axiom = "F"
    rules = {"F":"F-F+F"}
    iterations = 5 # TOP: 10
    angle = 120
    main(iterations,axiom,rules,angle)

def twin_dragon_curve():
    axiom = "FX+FX"
    rules = {"X":"X+YF+", "Y":"-FX-Y"}
    iterations = 8 # TOP: 16
    angle = 90
    main(iterations,axiom,rules,angle)

def three_dragon_curve():
    axiom = "FX+FX+FX"
    rules = {"X":"X+YF+", "Y":"-FX-Y"}
    iterations = 1 # TOP: 15
    angle = 90
    main(iterations,axiom,rules,angle)

def autosimilars_boxes():
    axiom = "YFF+YFF+YFF+YFF+"
    rules = {"Y":"YFFF+YFFF+YFFF+YFFF+YFFF"}
    iterations = 1 # TOP: 15
    angle = 90
    main(iterations,axiom,rules,angle,length=20)


def circular_boxes():
    axiom = "F"
    rules = {"F":"F+F+F+F|"}
    iterations = 40 # TOP: 15
    angle = 90
    angle_rule = 10
    main(iterations,axiom,rules,angle,length=100,angle_rule=angle_rule)

##########################################################################################3
def create_l_system(iters, axiom, rules):
    start_string = axiom
    if iters == 0: return axiom
    end_string = ""
    for _ in range(iters):
        end_string = "".join(rules[i] if i in rules else i for i in start_string)
        start_string = end_string
    return end_string

def draw_l_system(t, instructions, angle, distance, angle_rule):
    for cmd in instructions:
        if cmd == 'F':
            t.forward(distance)
        elif cmd == '+':
            t.right(angle)
        elif cmd == '-':
            t.left(angle)
        elif cmd == '|':
            t.left(angle_rule)

def main(iterations, axiom, rules, angle, length=8, size=2, x_offset=0, y_offset=0,  offset_angle=0, width=600, height=600, angle_rule=0):
    inst = create_l_system(iterations, axiom, rules)
    t = turtle.Turtle()
    wn = turtle.Screen()
    wn.setup(width, height)
    t.up()
    t.backward(-x_offset)
    t.left(90)
    t.backward(-y_offset)
    t.left(offset_angle)
    t.down()
    t.speed(0)
    t.pensize(size)
    draw_l_system(t, inst, angle, length, angle_rule)
    t.hideturtle()
    wn.exitonclick()

sierpinski_sieve()