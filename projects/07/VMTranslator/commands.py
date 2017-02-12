
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

# ADD_CMD = \
# """
# @SP
# A=M-1
# D=M
# @y
# M=D
#
# @SP
# M=M-1
#
# @SP
# A=M-1
# D=M
# @x
# M=D
#
# @SP
# M=M-1
#
# @x
# D=M
# @y
# D=D+M
#
# @SP
# A=M
# M=D
#
# @SP
# M=M+1
# """

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

# SUB_CMD = \
# """
# @SP
# A=M-1
# D=M
# @y
# M=D
#
# @SP
# M=M-1
#
# @SP
# A=M-1
# D=M
# @x
# M=D
#
# @SP
# M=M-1
#
# @x
# D=M
# @y
# D=D-M
#
# @SP
# A=M
# M=D
#
# @SP
# M=M+1
# """

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
M=1

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