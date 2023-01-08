
from exceptions import CommandNotDefined
from grammar import *
from semantics.core import check_semantics
import os
from semantics.visitors.evaluator_visitor import EvalVisitor

class System:
    def __init__(self) -> None:
        self.testers = self.get_avaliable_testers()
        self.commands = ['help', 'console', 'run_tester']
        
    def show_help(self):
        print("Usage:")
        print("python main.py # Show this message")
        print("python main.py help # Show this message")
        print("python main.py console # Open console and execute user code")
        
        if len(self.testers) > 0:
            print()
            print("Run testers:")
            for tester in self.testers:
                print(f"python main.py run_tester {tester}")
                
    def exist_command(self, command):
        return command in self.commands
    
    def check_command(self, command):
        if not self.exist_command(command):
            print("==================Error=================")
            print(CommandNotDefined(command))
            print("========================================")
            self.show_help()
        
    def run_command(self, command, arg = None):
        self.check_command(command)
        if arg:
            self.run_tester(arg)
        elif command == 'help':
            self.show_help()
        elif command == 'console':
            self.start_console()
            
    def start_console(self):
        os.system('cls')
        print("****************************************************")
        print("Draw DSL Console")
        print("Type exit to finish")
        print("****************************************************")
        result = ""
        line_char = "> "
        bracket_number = 0
        TAB = '\t'
        while True:
            line = input(line_char if bracket_number == 0 else '{>' + TAB * (bracket_number - 1))
            if line == "": continue
            if line == "exit": break
            if line[-1:] == "{": bracket_number += 1
            if line[-1:] == "}": bracket_number -= 1
            result += "\n" + line
        if result != "":
            try:
                self.run(result)
            except:
                print("Bad execution")
            option = input("Do you want to save code?[Y/N]: ")
            if option == "Y":
                print("Type filename")
                filename = input("Filename: usertester_")
                open(f"tester/usertester_{filename}.txt", '+w').write(result)
            
    
    def get_avaliable_testers(self):
        try:
            return [ file[:-4] for file in os.listdir('tester') if file[-4:] == ".txt"]
        except:
            return []
    
    def run_tester(self, tester_name):
        input = open(f"tester/{tester_name}.txt").read()
        self.run(input)
        
    def run(self, input):
        ast:Scene = parser.parse(input,lexer=lexer)
        if not ast:
            raise RuntimeError("AST Incomplete")
        if check_semantics(ast):
            EvalVisitor().visit(ast)