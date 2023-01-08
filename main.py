
from system import System
import sys

system = System()

def main(args = []):
    len_args = len(args)
    if len_args == 1:
        system.show_help()
    elif len_args == 2:
        command = args[1]
        system.run_command(command)
    elif len_args == 3:
        command = args[1]
        tester = args[2]
        system.run_command(command, tester)
    
if __name__ == "__main__":
    main(sys.argv)
    pass
    
