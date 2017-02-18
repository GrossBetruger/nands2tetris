import re
from commands import *
import sys


# aux VM code
INITIALIZE_LOCAL_VAR = "push constant 0"
POP_ARG_0 = "pop argument 0"

RETURN = "return"
FUNCTION = "function"
GOTO = "goto"
IF_GOTO = "if-goto"
LABEL = "label"
OFFSET_ZERO = "0"
BOOLEAN_OPERATIONS = {'eq', 'gt', 'lt', 'or', 'and', 'not'}
BOOL_COUNT = 0


# Arithmetic operations
ADD, SUB, NEG, EQ, GT, LT, AND, OR, NOT = 0, 1, 2, 3, 4, 5, 6, 7, 8
ARITHMETIC_COMMANDS = {'add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not'}

# Memory operations
PUSH, POP = 9, 10

# VM memory segments
SP, LCL, ARG, THIS, THAT, TEMP = 0, 1, 2, 3, 4, 5

DEST_DICT = {"local": "LCL", "argument" : "ARG", "this": "THIS", "that": "THAT",
             "temp": "TEMP", "static": "STATIC", "pointer": "POINTER"}

# Command types
# C_ARITHMETIC, C_PUSH, C_POP, C_LABEL, \
# C_GOTO, C_IF, C_FUNCTION, C_RETURN, C_CALL = \
# 0, 1, 2, 3, 4, 5, 6, 7, 8

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


def command_wrapper(lexems, filename):
    cmd_type = lexems[0]
    command_counter(cmd_type)
    if cmd_type in ARITHMETIC_COMMANDS:
        return arithmetic_wrapper(cmd_type)

    elif cmd_type == LABEL:
        label = lexems[1]
        return label_wrapper(label)

    elif cmd_type == IF_GOTO:
        label = lexems[1]
        return if_wrapper(label)

    elif cmd_type == GOTO:
        label = lexems[1]
        return goto_wrapper(label)

    elif cmd_type == FUNCTION:
        func_name = lexems[1]
        num_of_locals = int(lexems[2])
        return function_wrapper(func_name, num_of_locals)

    elif cmd_type == RETURN:
        return return_wrapper()

    else:
        dest, offset = lexems[1], lexems[2]
        return memory_wrapper(cmd_type, dest, offset, filename)


def glue_commands(cmd_lst):
    return "\n".join(cmd_lst)


def command_counter(cmd_type):
    global BOOL_COUNT
    if cmd_type in BOOLEAN_OPERATIONS:
        BOOL_COUNT += 1


def arithmetic_wrapper(cmd_type):
    global BOOL_COUNT
    bool_cmd = BOOL_RESULT_CMD.format(BOOL_COUNT)
    bool_jmp_dict = {'and': 'JGT',
                     'eq': 'JEQ',
                     'gt': 'JGT',
                     'lt': 'JLT',
                     'not': 'JEQ',
                     'or': 'JGT'}
    tf_jump  = TF_JMP.format(BOOL_COUNT, bool_jmp_dict.get(cmd_type))

    eq = glue_commands([POP_X_Y_CMD, EQ_CMD, tf_jump, bool_cmd])
    gt = glue_commands([POP_X_Y_CMD, GT_CMD, tf_jump, bool_cmd])
    lt = glue_commands([POP_X_Y_CMD, LT_CMD, tf_jump, bool_cmd])

    logical_and = glue_commands([POP_X_Y_CMD, AND_CMD])
    logical_or = glue_commands([POP_X_Y_CMD, OR_CMD])
    logical_not = glue_commands([POP_X_CMD, NOT_CMD])

    add = glue_commands([POP_X_Y_CMD, ADD_CMD])
    sub = glue_commands([POP_X_Y_CMD, SUB_CMD])
    neg = glue_commands([POP_X_CMD, NEG_CMD])


    ARITHMETIC_DICT = {'eq' : eq, 'sub': sub, 'add': add, 'gt': gt, \
                       'lt': lt, 'neg': neg, 'and': logical_and, \
                       'or' : logical_or, 'not': logical_not}

    return ARITHMETIC_DICT[cmd_type]


def memory_wrapper(cmd_type, dest, offset, filename):
    dest = DEST_DICT.get(dest)
    if cmd_type == C_PUSH:
        return write_push_code(dest, offset, filename)
    elif cmd_type == C_POP:
        return write_pop_code(dest, offset, filename)


def label_wrapper(label):
    return LABEL_CMD.format(label)


def goto_wrapper(label):
    return GOTO_CMD.format(label)


def if_wrapper(label):
    goto = IF_GOTO_CMD.format(label)
    return glue_commands([POP_X_CMD, goto])


def function_wrapper(function_name, num_local_vars):
    label = LABEL_CMD.format(function_name)
    init_local = command_wrapper(lexer(INITIALIZE_LOCAL_VAR), None)
    local_vars_push = glue_commands([init_local] * num_local_vars)
    return glue_commands([label, local_vars_push])


def call_wrapper(function_name, arity):
    pass


def return_wrapper():
    prepare_for_return = PREPARE_TO_RETURN
    return_value_to_return_address = command_wrapper(lexer(POP_ARG_0), None)
    return_sp_to_caller_prepare = SP_TO_CALLER_PREPARE

    segments_and_offsets = (("THAT", 1), ("THIS", 2), ("ARG", 3), ("LCL", 4))
    restore_memory_segments = \
        glue_commands([RESTORE_SEGMENT.format(offset, segment) for segment, offset in segments_and_offsets])
    goto_return = GOTO_RETURN_ADDRESS
    # sp_to_caller = SP_TO_CALLER_CMD

    return glue_commands([prepare_for_return, return_value_to_return_address,
                          return_sp_to_caller_prepare, restore_memory_segments, goto_return])


def prepend_init():
    pass


def set_file_name():
    pass


def write_push_code(stack_base, offset, filename):
    if stack_base == "TEMP":
        return PUSH_CMD_TEMP.format(5 + int(offset))
    elif stack_base == "STATIC":
        return PUSH_STATIC.format(filename, offset)
    elif stack_base == "POINTER":
        address = THIS if offset == OFFSET_ZERO else THAT
        return PUSH_POINTER.format(address)
    if stack_base is None:
        return PUSH_CMD_CONST.format(offset)

    return PUSH_CMD.format(offset, stack_base)


def write_pop_code(stack_base, offset, filename):
    if stack_base == "TEMP":
        return POP_CMD_CONST.format(5 + int(offset))
    elif stack_base == "STATIC":
        return POP_STATIC.format(filename, offset)
    elif stack_base == "POINTER":
        address = THIS if offset == OFFSET_ZERO else THAT
        return POP_POINTER.format(address)

    return POP_CMD.format(offset, stack_base)


def parser(lines_of_code, filename):
    for line in lines_of_code:
        print r"//", line
        print command_wrapper(lexer(line), filename)


def main(filename):
    code = read_vm_file(filename)
    classname = filename.split(".")[0]
    parser(code, classname)


example_lbl  = "label LOOP_START"
example_func_dec = "function SimpleFunction.test 2"

if __name__ == "__main__":
    # code = ["return"]
    # parser(code, "file")
    # quit()
    # print POP_ARG_0
    # print command_wrapper(lexer(POP_ARG_0), None)
    # quit()
    main(sys.argv[1])