// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// Probably not the most efficient program ever written in the history of ASM, but it works, and more importantly won't exceed memory.

// start the screen
// sets 'color' to the current RAM address of the screen
@SCREEN // variable for the current RAM address of the screen
D=A
@color // set a variable name for the current RAM address of the screen
M=D

(MAIN)
    // main loop
    @KBD // base address of keyboard, you could use 24576 if you wanted to
    D=M
    @press // set 'press' equal to the keyboard RAM value
    M=D
    
    // I wasn't sure which one I wanted to write first, but I wrote FILL first
    @press // strictly speaking you could just call KBD, but I wanted to get practice using variables
    D=M
    @FILL
    D;JNE // jump if 'press' != 0 (I don't think it can't be negative, but just in case)
    @ERASE
    D;JEQ // otherwise jump to erase (0 and not 0 cover the set of all possible values in RAM)

(FILL)
    // decrement the address if address is greater than memory that exists
    // this code will be repeated a ton later on
    @color
    D=M
    @KBD
    D=D-A
    @DEC
    D;JGT

    @color // call up the current RAM address of the screen
    // since we want to fill it, change the value in memory
    A=M
    M=-1 // fill black
    @INC
    0;JMP

(INC)
    @color
    D=M
    D=D+1 // increment the address register
    @color
    M=D
    @MAIN
    0;JMP // go back to main

(ERASE)
    // decrement if address is greater than memory that exists
    // not sure if strictly necessary here, but it exists to remove any possibility of a memory overflow
    @color
    D=M
    @KBD
    D=D-A
    @DEC
    D;JGT

    @color // call up the current RAM address of the screen
    // since we want to fill it, change the value in memory
    A=M // set A to the current RAM address
    M=0 // fill white
    @DEC
    0;JMP // go to decrement

(DEC)
    // decrement the memory address of 'color'
    @color
    A=M
    D=A
    @SCREEN
    D=D-A
    @MAIN
    D;JLT // if you can't go any lower in screen address skip this part to avoid overwriting other RAM
    @color
    A=M
    D=A-1 // decrement the address register
    @color
    M=D
    @MAIN
    0;JMP // go back to main