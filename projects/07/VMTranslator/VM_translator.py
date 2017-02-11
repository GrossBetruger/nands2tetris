import re
from commands import *
import sys

# Arithmetic operations
ADD, SUB, NEG, EQ, GT, LT, AND, OR, NOT = 0, 1, 2, 3, 4, 5, 6, 7, 8
ARITHMETIC_COMMANDS = set(['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not'])

# Memory operations
PUSH, POP = 9, 10

# VM memory segments
SP, LCL, ARG, THIS, THAT, TEMP = 0, 1, 2, 3, 4, 5

DEST_DICT = {"local": "LCL", "argument" : "ARG", "this": "THIS", "that" : "THAT", "temp": "TEMP"}

# Command types
C_ARITHMETIC, C_PUSH, C_POP, C_LABEL, \
C_GOTO, C_IF, C_FUNCTION, C_RETURN, C_CALL = \
0, 1, 2, 3, 4, 5, 6, 7, 8

C_PUSH = 'push'
C_POP = 'pop'


def read_vm_file(vm_file_name):
    with open(vm_file_name) as f:
        return clear_whitespace([row.strip() for row in f.readlines()])


def clear_whitespace(lines):
    return [re.sub("\s+", " ", line) for line in
            [re.sub("//.+", "", line) for line in lines] if line != ""]


def lexer(command):
    delimiter = " "
    return command.split(delimiter)


def command_wrapper(lexems):
    cmd_type = lexems[0]
    if cmd_type in ARITHMETIC_COMMANDS:
        return arithmetic_wrapper(cmd_type)
    else:
        dest, offset = lexems[1], lexems[2]
        return memory_wrapper(cmd_type, dest, offset)


def glue_commands(cmd_lst):
    return "\n".join(cmd_lst)


def arithmetic_wrapper(cmd_type):
    eq = glue_commands([POP_X_Y_CMD, EQ_CMD, BOOL_RESULT_CMD])
    gt = glue_commands([POP_X_Y_CMD, GT_CMD, BOOL_RESULT_CMD])
    lt = glue_commands([POP_X_Y_CMD, LT_CMD, BOOL_RESULT_CMD])
    logical_and = glue_commands([POP_X_Y_CMD, AND_CMD, BOOL_RESULT_CMD])
    logical_or = glue_commands([POP_X_Y_CMD, OR_CMD, BOOL_RESULT_CMD])
    logical_not = glue_commands([POP_X_Y_CMD, NOT_CMD, BOOL_RESULT_CMD])

    add = glue_commands([POP_X_Y_CMD, ADD_CMD])
    sub = glue_commands([POP_X_Y_CMD, SUB_CMD])
    neg = glue_commands([POP_X_CMD, NEG_CMD])


    ARITHMETIC_DICT = {'eq' : eq, 'sub': sub, 'add': add, 'gt': gt, \
                       'lt': lt, 'neg': neg, 'and': logical_and, \
                       'or' : logical_or, 'not': logical_not}

    return ARITHMETIC_DICT[cmd_type]


def memory_wrapper(cmd_type, dest, offset):
    dest = DEST_DICT.get(dest)
    if cmd_type == C_PUSH:
        return write_push_code(dest, offset)
    elif cmd_type == C_POP:
        return write_pop_code(dest, offset)


def write_push_code(stack_base, offset):
    if stack_base == "TEMP":
        return PUSH_CMD_CONST.format(5 + int(offset))
    if stack_base == None:
        return PUSH_CMD_CONST.format(offset)

    return PUSH_CMD.format(offset, stack_base)


def write_pop_code(stack_base, offset):
    if stack_base == "TEMP":
        return POP_CMD_CONST.format(5 + int(offset))
    return POP_CMD.format(offset, stack_base)


def parser(lines_of_code):
    for line in lines_of_code:
        print r"//", line
        print command_wrapper(lexer(line))


pop_exp_1 = "pop argument 2"
pop_exp_2 = "pop argument 1"
pop_exp_3 = "pop local 0"
push_exm1 = "push this 6"

if __name__ == "__main__":

    # print parser(["pop temp 6"])
    # quit()
    code = read_vm_file(sys.argv[1])
    parser(code)
    quit()
    print POP_X_Y_CMD
    print EQ_CMD
    quit()
    code = read_vm_file("../test2.vm")

    parser(code)
    quit()
    print write_push_code(12, SP, 0)
    print write_pop_code(ARG, 3)
    quit()
    # print PUSH_CMD.format(3)
    # print POP_CMD.format(2)
    # for line in read_vm_file("../test2.vm"):
    #     print line