// limitations: this doesn't check if you actually pressed a digit, it write all keyboard inputs (time pressure here)

(MAIN)
    // main loop
    @KBD // base address of keyboard, you could use 24576 if you wanted to
    D=M
    @press // set 'press' equal to the keyboard RAM value of the key you just pressed
    M=D
    @48
    D=A
    
    @press // strictly speaking you could just call KBD, but I wanted to get practice using variables
    D=M-D
    @WRITE
    D;JNE // jump if 'press' != 0 (e.g. you pressed something)

    0;JMP

(WRITE)

    @18113 // call up the current RAM address of the screen
    // since we want to fill it, change the value in memory
    D=D+A // assign the ram address of the correct value
    @ramadd // write to the correct RAM address
    M=D
    A=M
    M=-1
    @MAIN
    0;JMP