import sys
from utils import command  # This line is useful, must keep it!


def print_help():
    print "Usage:"
    print "python manage.py [-h] [func_call]"
    print "    - -h: print help"
    print "    - func_call: command_file_name [arg1] [arg2] ..."
    print "      command_file_name refers to .py under utils/command/"
    print "    - Example1: python manage.py hello_world"
    print "    - Example2: python manage.py hello_world --id=0 --name=hello"


# Help information
if len(sys.argv) <= 1 or sys.argv[1] == "-h":
    print_help()
    sys.exit(0)

command_name = sys.argv[1]

# Call the handle() function according to given command name
try:
    func_call = "command.%s.Command().handle()" % (command_name)
    eval(func_call)
except Exception as err:
    print "Command error: " + str(err)
    print_help()
