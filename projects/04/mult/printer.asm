(READ_KEYBOARD)
@KBD
D=M
@BLACK
D;JNE
@READ_KEYBOARD
0;JMP

(BLACK)
@16384
D=A
@first_scr
M=D
@24576
D=A
@i
M=D
(LOOP)
@i
A=M
M=-1
@i
M=M-1
@first_scr
D=M
@i
D=M-D
@LOOP
D;JGT

@READ_KEYBOARD
0;JMP