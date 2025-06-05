import sys
import random

helptxt = '''

# COMMANDS #
out <string> | print string
inp <message> <resultvar> | get user input with prompt message as resultvar
set <varname> <value> | set a new variable
add/sub/mul/div <v1> <v2> <resultvar> | add/subtract/multiply/divide v1 by v2,
put the results in resultvar
vout <var> | print variable value no newline
nl | print a newline
goto <line> | FILE EXEC ONLY: go to a line number
if <op> <v1> <v2> <somecode> | if v1 op v2, execute somecode
inc <var> | increment variable by 1
dec <var> | decrement variable by 1
rnd <c1> <c2> <c3> <resultvar> | get a random choice of c1, c2, and c3
(not variables) and put it in resultvar

# SYNTAX #
use ~ when defining a variable to set to None
use { code # code # code } in an if statement to run multiple commands

'''

# TODO: custom error messages

variables = {}

exline = -1

SHELL_MODE = False

def execute(tokens):

    if tokens[0] == "out":
        for t in tokens[1:len(tokens)]:
            print(t + " ", end="")
        print()
    elif tokens[0] == "set":
        variables[tokens[1]] = None if tokens[2] == "~" else tokens[2]
    elif tokens[0] == "vout":
        print(variables[tokens[1]], end=" ")
        if SHELL_MODE: print()
    elif tokens[0] == "inp":

        inpstr = ""
        for t in tokens[1:len(tokens)-1]:
            inpstr = inpstr + t + " "

        variables[tokens[len(tokens) - 1]] = input(inpstr)
    elif tokens[0] == "goto":
        global exline
        exline = int(tokens[1])
    elif tokens[0] == "if":
        op = tokens[1]
        v1 = variables[tokens[2]]
        v2 = variables[tokens[3]]
        result = False
        if op == "==" and v1 == v2: result = True
        elif op == "<" and v1 < v2: result = True
        elif op == ">" and v1 > v2: result = True
        elif op == "!=" and v1 != v2: result = True
        if result:
            execute(tokens[4:len(tokens)])
    elif tokens[0] == "inc":
        variables[tokens[1]] = str(int(variables[tokens[1]]) + 1)
    elif tokens[0] == "dec":
        variables[tokens[1]] = str(int(variables[tokens[1]]) - 1)
    elif tokens[0] == "rnd":
        variables[tokens[4]] = random.choice([tokens[1], tokens[2], tokens[3]])
    # math
    elif tokens[0] == "add":
        num_a = int(variables[tokens[1]])
        num_b = int(variables[tokens[2]])

        variables[tokens[3]] = str(num_a + num_b)
    elif tokens[0] == "sub":
        num_a = int(variables[tokens[1]])
        num_b = int(variables[tokens[2]])

        variables[tokens[3]] = str(num_a - num_b)
    elif tokens[0] == "mul":
        num_a = int(variables[tokens[1]])
        num_b = int(variables[tokens[2]])

        variables[tokens[3]] = str(num_a * num_b)
    elif tokens[0] == "div":
        num_a = int(variables[tokens[1]])
        num_b = int(variables[tokens[2]])

        if num_a == 0 or num_b == 0:
            print("ERROR: division by zero");return

        variables[tokens[3]] = str(num_a / num_b)
    # special commands
    elif tokens[0] == "end":
        print()
        exit()
    elif tokens[0] == "help":
        print(helptxt)
    elif tokens[0] == "nl":
        print()
    else:
        print("NOT A COMMAND")

if sys.argv.__len__() < 2:
    print("you have ran in shell mode. to execute a file,")
    print("run like this: python3 interp.py <code file path>\n\n")
    SHELL_MODE = True

if (not SHELL_MODE):
    fl = open(sys.argv[1], "r")

    lines = fl.readlines()

    size = lines.__len__()

    while exline < size - 1:
        exline += 1
        line = lines[exline]
        if line == "\n" or line.startswith(";"):
            continue
        execute(line.strip().split(" "))

else:
    print("Welcome to the SnoutScript shell")
    print("Type help for documentation and end to exit")

    while True:
        cmnd = input("snout> ")
        execute(cmnd.split(" "))
