import sys
import os
import time
import pygame

os.system('clear')
_datatypes = {'int', 'float', 'string'}
_vars = []
class _var:
    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value
        _vars.append(self)

class _window:
    def __init__(self,WIDTH, HEIGHT, name, screen):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.name = name
        self.screen = screen
        
if (len(sys.argv) <= 1):
    filePath = 'server.xs'
    #print("error : missing commandline arguments")
    #sys.exit()
else:
    filePath = sys.argv[1]
sourceCode = open(filePath)
code = sourceCode.read()
value = '\0'
count = '\0'

pygame.init()
globalWindow = _window(0,0,'WINDOW', 0)
def init_window(x,y):
    globalWindow.screen = pygame.display.set_mode((x,y))
    globalWindow.WIDTH = x
    globalWindow.HEIGHT = y

def run_window():
    pygame.display.set_caption(globalWindow.name)
    run = True
    while run:
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()
                    sys.exit()
    

def ticketer(code):
    code = code.replace('\n', '')
    commands = code.split(';')
    #commands = commands.split('{')
    full_commands = []
    #print(commands)
    for comm in range(len(commands)):
        if(commands[comm] != '<!>'):
            executer(commands[comm])
            """if('{' in commands[comm]):
                executer(commands[comm])
                sub_commands = commands[comm].split('{')
                for sub_comm in sub_commands:
                    full_commands.append(sub_comm)
            else:
                full_commands.append(commands[comm])
        else: break"""
    #print(full_commands)

"""
if { is in command, split command by { into sub_commands;
"""

def call(var_name):
    var_name = var_name.replace(',', '')
    for var in _vars:
        if(var_name == var.name):
            if(var.type == 'int'):
                return int(var.value)
            return var.value
    return int(var_name)

def get_var(var_name):
    for var in _vars:
        if(var_name == var.name):
            return var

def exists(var_name):
    for var in _vars:
        if(var_name == var.name):
            return True
    return False

def reticket(start, args):
    args[1] = args[1].replace('(', '')
    args[1] = args[1].replace(')', '')
    args[1] = args[1].replace('{', '')

    tempCommands = []
    comm = '\0'
    i = start
    while i < len(args):
        if i+1 == len(args): args[i] += ','
        if(',' in args[i]):
            args[i] = args[i].replace(',', '')
            comm += args[i]
            tempCommands.append(comm)
            comm = '\x00'
        else:
                comm.replace('\x00', '')
                comm += args[i]
                comm += ' '
        i+=1

    tempCommands[-1] = tempCommands[-1].replace('}', '')
    return tempCommands

def eval(condition):
    if(condition == 'true'):
        return True
    if(condition == 'false'):
        return False
    if(condition[1] == '=='):
        if(call(condition[0]) == call(condition[2])):
            return True

    if(condition[1] == '>'):
        if(call(condition[0]) > call(condition[2])):
            return True

    if(condition[1] == '<'):
        if(call(condition[0]) < call(condition[2])):
            return True

    if(condition[1] == '>='):
        if(call(condition[0]) >= call(condition[2])):
            return True

    if(condition[1] == '<='):
        if(call(condition[0]) <= call(condition[2])):
            return True

    return False

def executer(command):
    global _var
    args = command.split(' ')

    if('>/' in args[0]): return #the executer ignores comments

    if(args[0] == 'if'):
        args[1] = args[1].replace('(', '')
        args[1] = args[1].replace(')', '')
        cond = []
        for arg in args[1:]:
            if not ('{' in arg):
                cond.append(arg)
            else:
                cond.append(arg)
                break
        cond[-1] = cond[-1].replace(')', '')
        cond[-1] = cond[-1].replace('{', '')
        cond = eval(cond)
        if(cond):
            tempCommands = reticket(4, args)
            for tempComm in tempCommands:
                executer(tempComm.replace('\x00', ''))

    if (args[0] in _datatypes and args[2] == '='): #declaration of variables
        if(args[0] == 'string'):
            full_value = ''
            i = 3
            while i < (len(args)):
                if(i > 3): full_value += ' '
                full_value += args[i]
                i+=1
            temp = _var(args[1], args[0], full_value)
            return
        elif(args[0] == 'int'):
            if(exists(args[3])):
                temp = _var(args[1], args[0], call(args[3]))
                return

        temp = _var(args[1], args[0], args[3])

    global value
    value = '\0'
    if(exists(args[0])): #if the first argument is a known defined variable
        for var2 in _vars:
            if(args[2] == var2.name):
                value = var2.value
        #Operator selection from math module
        var = get_var(args[0])
        if(value != '\0'):
            if(args[1] == '+=' and (var.type == 'int')):
                var.value = int(var.value) + int(value)
            if(args[1] == '-=' and (var.type == 'int')):
                var.value = int(var.value) - int(value)
            if(args[1] == '*=' and (var.type == 'int')):
                var.value = int(var.value) * int(value)
            if(args[1] == '/=' and (var.type == 'int')):
                var.value = int(var.value) / int(value)
            if(args[1] == '=' and (var.type == 'int')):
                var.value = int(value)
        else:
            if(args[1] == '+=' and (var.type == 'int')):
                var.value = int(var.value) + int(args[2])
            if(args[1] == '-=' and (var.type == 'int')):
                var.value = int(var.value) - int(args[2])
            if(args[1] == '*=' and (var.type == 'int')):
                var.value = int(var.value) * int(args[2])
            if(args[1] == '/=' and (var.type == 'int')):
                var.value = int(var.value) / int(args[2])

    if(args[0]=='disp'): #display function
        args[1] = args[1].replace('(', '')
        args[1] = args[1].replace(')', '')
        if(exists(args[1])): #if variable is associated with a value, display it
            var = get_var(args[1])
            if(len(args)<3):
                if(var.type == 'string'):
                    stripped = var.value.replace('"', '')
                    print(stripped)
            if(var.type == 'int'):
                print(var.value)
        else:
            if('"' in args[1]):
                tempString = args[1] + ' '
                for arg in args[2:]:
                    if not ('"' in arg):
                        tempString += arg
                        tempString += ' '
                    else:
                        tempString += arg
                        break
                tempString = tempString.replace(')', '')
                stripped = tempString.replace('"', '')
                print(stripped)
                return
            print(args[1])

    if(args[0] == 'repeat'):
        args[1] = args[1].replace('(', '')
        args[1] = args[1].replace(')', '')
        args[1] = args[1].replace('{', '')
        global count
        if not exists(args[1]):
            count = args[1]
        else:
            var = get_var(args[1])
            count = var.value

        tempCommands = reticket(2, args)
        for iter in range(int(count)):
            for tempComm in tempCommands:
                executer(tempComm.replace('\x00', ''))

    if(args[0] == 'wait'):
        args[1] = args[1].replace('(', '')
        args[1] = args[1].replace(')', '')
        delay = int(call(args[1]))
        time.sleep(delay)

    if('clear' in args[0]): os.system('clear')

    if('window' == args[0]):
        args[1] = args[1].replace('(', '')
        args[1] = args[1].replace(')', '')
        x, y = args[1].split(',')
        x = int(x)
        y = int(y)
        init_window(x,y)

    if('window.run'== args[0]):
        run_window()
        print('ran')

    if('window.name' == args[0]):
        full_value = ''
        i = 2
        while i < (len(args)):
            if(i > 2): full_value += ' '
            full_value += args[i]
            i+=1
        full_value = full_value.replace('"', '')
        globalWindow.name = full_value


ticketer(code)