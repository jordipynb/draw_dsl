# DRAW: A DSL for Fractals and Pattern-Based Graphics

## Description
The goal of the implemented DSL (Domain-Specific Language) is to provide a language that allows for the design and drawing of flat figures, particularly figures that follow specific patterns, such as fractals, with a special focus on trees. This project is developed as part of the Compilation course and is designed to facilitate the creation of graphics through a set of rules and axioms.

### Authors
* **Dianelys Cruz Mengana** (C-311)
* **Jordan Pla González** (C-311)
* **Leandro Hernández Nuñez** (C-312)

## Language Features
To define figures, it is necessary to specify their identifier `<name>` and the color that will be used to draw them (if not defined, they are drawn in black). The definition of a figure is divided into two sections:

- **Set of Rules (optional)**: Instructions that allow for recursion and the creation of figures.
- **Axiom**: The execution body of the figure from which rules can be accessed.

### Language Instructions
- `left <expression>`: Changes the cursor's direction to the left.
- `right <expression>`: Changes the cursor's direction to the right.
- `line <expression>`: Draws a line with the resulting length.
- `jump <expression1>,<expression2>`: Changes the cursor's coordinates to (**expression1**, **expression2**).
- `push`: Saves the current coordinates onto a stack.
- `pop`: Returns the cursor to the coordinates at the top of the stack.
- `call_shape <shape_name>`: Draws the specified shape in **shape_name**.
- `call_rule <rule_name> (expression)`: Executes the specified rule.
- `<variable> = <expression>`: Assigns the result to a variable.
- `<variable> = get_x`: Assigns the current x-coordinate to a variable.
- `<variable> = get_y`: Assigns the current y-coordinate to a variable.
- `set_x <expression>`: Changes the current x-coordinate.
- `set_y <expression>`: Changes the current y-coordinate.

> The grammar used is unambiguous, allowing for a unique left derivation for each valid string. An LALR algorithm has been used to resolve it.

## Compiler Architecture
* **Lexer**: The lexer is implemented using the `ply` library for ease of use.
* **Parser**: Similarly, it uses `ply`, leveraging its efficiency with LALR parsers.
* **AST**: An abstract syntax tree is constructed using a hierarchy of classes found in `utils.py`.
* **Semantic Analysis**: The semantic analysis utilizes the visitor pattern to validate contexts and collect types, located in the `semantics.visitors` directory.
* **Interpreter**: The interpreter relies on Python's class hierarchy that defines the AST.

## Installation
To install the required packages, run:
```bash
pip install -r requirements.txt
```

## Running the Project
To execute the project, use:
```bash
python main.py
```

## Conclusion
This project provides a DSL for creating complex graphic figures through a rule-based system. It allows users to explore concepts such as fractals and trees through graphic programming.
