import sys
import os
import time
_datatypes = {'int', 'float', 'string'}
_vars = []
class _var:
    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value
        _vars.append(self)

print(sys.argv)

if (len(sys.argv) <= 1):
    print("") #error : missing commandline arguments
    #sys.exit()

sourceCode = open('test.xs')
code = sourceCode.read()
value = '\0'
count = '\0'

def ticketer(code):
    code = code.replace('\n', '')
    commands = code.split(';')
    command_index = 0
    for comm in commands:
        if(comm != '<!>'):
            executer(comm)
        command_index += 1

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
ticketer(code)
