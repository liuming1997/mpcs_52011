// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

// We use D as much as possible to avoid directly changing values of RAM[0] and RAM[1].

@2 // RAM[2]
M=0 // clear RAM[2]

@3 // I've never seen 3 units of RAM as a constraint, and this makes life easy
M=0 // number of times addition has occurred

@0 // jump to end if RAM[0] = 0, no need to compute
D=M
@END
D;JEQ

@1 // jump to end if RAM[1] = 0, no need to compute
D=M
@END
D;JEQ

(LOOP)
    @3
    M=M+1 // increment the number of times we added
    @0
    D=M // send RAM[0] to data register
    @2
    M=M+D // add contents of RAM[2] to data register and store to data
    @3
    D=M // set data register equal to RAM[3] (i.e. number of times we added)
    @1
    D=M-D // set data register equal to RAM[1] (number of times we want to add RAM[0]) minus RAM[3] (how many times we already added RAM[0])
    @LOOP
    D;JGT // jump back to start if we haven't finished adding
    @END
    M;JEQ // jump to end otherwise

(END) // end of program
    0;JMP