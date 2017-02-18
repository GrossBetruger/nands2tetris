PUSH_CMD = \
"""
@{0}
D=A
@{1}
D=D+M

A=D
D=M
@SP
A=M
M=D

@SP
M=M+1
"""

PUSH_CMD_CONST = \
"""
@{}
D=A

@SP
A=M
M=D

@SP
M=M+1
"""

PUSH_CMD_TEMP = \
"""
@{}
D=M

@SP
A=M
M=D

@SP
M=M+1
"""

PUSH_STATIC = \
"""
@{0}.{1}
D=M

@SP
A=M
M=D

@SP
M=M+1
"""

PUSH_POINTER = \
"""
@{}
D=M

@SP
A=M
M=D

@SP
M=M+1
"""

POP_POINTER = \
"""
@SP
A=M-1
D=M

@{}
M=D

@SP
M=M-1
"""

POP_CMD = \
"""
@{0}
D=A
@{1}
D=D+M
@target_address
M=D

@SP
A=M-1
D=M
@target_address
A=M
M=D

@SP
M=M-1
"""

POP_STATIC = \
"""
@SP
A=M-1
D=M

@{0}.{1}
M=D

@SP
M=M-1
"""

POP_CMD_CONST = \
"""
@{}
D=A
@target_address
M=D

@SP
A=M-1
D=M
@target_address
A=M
M=D

@SP
M=M-1
"""

ADD_CMD = \
"""
@x
D=M
@y
D=D+M

@SP
A=M
M=D

@SP
M=M+1
"""

# NOTE: y is popped before x, y is subtracted from x
SUB_CMD = \
"""
@x
D=M
@y
D=D-M

@SP
A=M
M=D

@SP
M=M+1
"""

POP_X_Y_CMD = \
"""
@SP
A=M-1
D=M
@y
M=D

@SP
M=M-1

@SP
A=M-1
D=M
@x
M=D

@SP
M=M-1
"""

POP_X_CMD = \
"""
@SP
A=M-1
D=M
@x
M=D

@SP
M=M-1
"""


EQ_CMD = \
"""
@x
D=M
@y
D=D-M
"""

TF_JMP = \
"""
@TRUE_{0}
D;{1}
@FALSE_{0}
0;JMP
"""

BOOL_RESULT_CMD= \
"""
(TRUE_{0})
@SP
A=M
M=-1

@TF_END_{0}
0;JMP

(FALSE_{0})
@SP
A=M
M=0

@TF_END_{0}
0;JMP

(TF_END_{0})
@SP
M=M+1
"""

GT_CMD = \
"""
@x
D=M
@y
D=D-M
"""

LT_CMD = \
"""
@x
D=M
@y
D=D-M
"""

NEG_CMD = \
"""
@x
D=M
D=-D

@SP
A=M
M=D

@SP
M=M+1
"""

AND_CMD = \
"""
@x
D=M
@y
D=D&M

@SP
A=M
M=D

@SP
M=M+1
"""

OR_CMD = \
"""
@x
D=M
@y
D=D|M

@SP
A=M
M=D

@SP
M=M+1
"""

NOT_CMD = \
"""
@x
D=M
D=!D

@SP
A=M
M=D

@SP
M=M+1
"""

LABEL_CMD = \
"""
({})
"""

IF_GOTO_CMD = \
"""
@x
D=M
@{}
D;JNE
"""

GOTO_CMD = \
"""
@{}
0;JMP
"""

# save endFrame var (address of LCL)
# dereference 5 addresses less than endFrame and save to retAddr
PREPARE_TO_RETURN = \
"""
@LCL
D=M
@endFrame
M=D

@5
D=A
@endFrame
D=M-D

@retAddr
M=D

"""

SP_TO_CALLER_PREPARE = \
"""
@ARG
A=M+1
D=A

@SP
M=D
"""

# SP_TO_CALLER_CMD = \
# """
# @callerSP
# D=M
# @SP
# M=D
# """

# dereference saved memory segment location
# return memory segment to saved value

RESTORE_SEGMENT = \
"""
@{0}
D=A
@endFrame
D=M-D
A=D
D=M

@{1}
M=D
"""

GOTO_RETURN_ADDRESS = \
"""
@retAddr
A=M
0;JMP
"""