@256
D=A
@SP
M=D
// call at line 1 for function Sys.init
@Sys.init_0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(Sys.init_0)
// a function called Main.fibonacci
(Main.fibonacci)
@i
M=0
@0
D=A
@n
M=D
(Main.fibonacci_LOOP)
@n
D=M
@i
D=D-M
@Main.fibonacci_ENDLOOP
D;JEQ
@SP
A=M
M=0
@i
M=M+1
@SP
M=M+1
@Main.fibonacci_LOOP
0;JMP
(Main.fibonacci_ENDLOOP)
// push argument0 
@0
D=A
@ARG
D=D+M
@temp
M=D
@temp
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant2 
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
AM=M-1
D=D-M
@lt0
D;JGT
D=0
@lt_end0
0;JMP
(lt0)
D=-1
(lt_end0)
@SP
A=M
M=D
@SP
M=M+1
// if goto at 2
@SP
M=M-1
A=M
D=M
@IF_TRUE
D;JNE
// goto IF_FALSE
@IF_FALSE
0;JMP
(IF_TRUE)
// push argument0 
@0
D=A
@ARG
D=D+M
@temp
M=D
@temp
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@ends
M=D
@ends
D=M
@5
A=D-A
D=M
@ret
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
M=M+1
D=M
@SP
M=D
@ends
M=M-1
A=M
D=M
@THAT
M=D
@ends
M=M-1
A=M
D=M
@THIS
M=D
@ends
M=M-1
A=M
D=M
@ARG
M=D
@ends
M=M-1
A=M
D=M
@LCL
M=D
@ret
A=M
0;JMP
(IF_FALSE)
// push argument0 
@0
D=A
@ARG
D=D+M
@temp
M=D
@temp
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant2 
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
AM=M-1
M=M-D
@SP
M=M+1
// call at line 3 for function Main.fibonacci
@Main.fibonacci_2
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci_2)
// push argument0 
@0
D=A
@ARG
D=D+M
@temp
M=D
@temp
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant1 
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
AM=M-1
M=M-D
@SP
M=M+1
// call at line 4 for function Main.fibonacci
@Main.fibonacci_3
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci_3)
@SP
AM=M-1
D=M
@SP
AM=M-1
M=D+M
@SP
M=M+1
@LCL
D=M
@ends
M=D
@ends
D=M
@5
A=D-A
D=M
@ret
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
M=M+1
D=M
@SP
M=D
@ends
M=M-1
A=M
D=M
@THAT
M=D
@ends
M=M-1
A=M
D=M
@THIS
M=D
@ends
M=M-1
A=M
D=M
@ARG
M=D
@ends
M=M-1
A=M
D=M
@LCL
M=D
@ret
A=M
0;JMP
// a function called Sys.init
(Sys.init)
@i
M=0
@0
D=A
@n
M=D
(Sys.init_LOOP)
@n
D=M
@i
D=D-M
@Sys.init_ENDLOOP
D;JEQ
@SP
A=M
M=0
@i
M=M+1
@SP
M=M+1
@Sys.init_LOOP
0;JMP
(Sys.init_ENDLOOP)
// push constant4 
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
// call at line 5 for function Main.fibonacci
@Main.fibonacci_5
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci_5)
(WHILE)
// goto WHILE
@WHILE
0;JMP