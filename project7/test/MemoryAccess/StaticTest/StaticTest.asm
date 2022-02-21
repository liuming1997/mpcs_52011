// push 
@111
D=A
@SP
A=M
M=D
@SP
M=M+1
// push 
@333
D=A
@SP
A=M
M=D
@SP
M=M+1
// push 
@888
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop 
@SP
AM=M-1
D=M
@8
M=D
// pop 
@SP
AM=M-1
D=M
@3
M=D
// pop 
@SP
AM=M-1
D=M
@1
M=D
// push 
@3
D=M
@SP
A=M
M=D
@SP
M=M+1
// push 
@1
D=M
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
// push 
@8
D=M
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
M=D+M
@SP
M=M+1
