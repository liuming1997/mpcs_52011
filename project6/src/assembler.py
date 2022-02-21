"""
MPCS 52011
Project 6: The Assembler

Ming Liu
"""

#!/usr/bin/env python

import os.path
import pathlib
import re
import argparse
import sys

# Dictionary of the computation instructions (C-instructions)
# of the form 1,1,1,a,c1,c2,c3,c4,c5,c6,d1,d2,d3,j1,j2,j3

comp = {
    # following the notation in the book
    # a=0 for these, followed by c1, c2, ... c6
    '0' : '0101010',
    '1' : '0111111',
    '-1' : '0111010',
    'D' : '0001100',
    'A' : '0110000',
    '!D' : '0001101',
    '!A' : '0110001',
    '-D' : '0001111',
    '-A' : '0110011',
    'D+1' : '0011111',
    'A+1' : '0110111',
    'D-1' : '0001110',
    'A-1' : '0110010',
    'D+A' : '0000010',
    'D-A' : '0010011',
    'A-D' : '0000111',
    'D&A' : '0000000',
    'D|A' : '0010101',
    # a=1 for these
    'M' : '1110000',
    '!M' : '1110001',
    '-M' : '1110011',
    'M+1' : '1110111',
    'M-1' : '1110010',
    'D+M' : '1000010',
    'D-M' : '1010011',
    'M-D' : '1000111',
    'D&M' : '1000000',
    'D|M' : '1010101'
}

dest = {
    # null: no operation for dest in input
    'null' : '000',
    'M' : '001',
    'D' : '010',
    'MD' : '011',
    'A' : '100',
    'AM' : '101',
    'AD' : '110',
    'AMD' : '111'
}

jump = {
    # null: no operation for jump in input
    'null' : '000',
    'JGT' : '001',
    'JEQ' : '010',
    'JGE' : '011',
    'JLT' : '100',
    'JNE' : '101',
    'JLE' : '110',
    'JMP' : '111'
}

# Dictionary of predefined symobls

symbols = {
    'SP' : '0',
    'LCL' : '1',
    'ARG' : '2',
    'THIS' : '3',
    'THAT' : '4',
    'SCREEN' : '16384',
    'KBD' : '24576',
}

# define the variable RAM space, starting from RAM[16]; we will use this to add to symbols later
variableRAM = 16

# append to symbols the values for R0-R16
for i in range(0,16):
    temp = 'R' + str(i)
    symbols[temp] = i

class Parser:
    def __init__(self, path):
        """
        Initialize the Parser class by taking in a file.
        Still has some trouble with relative paths.
        """
        # copied from whitespace.py in project 0, but fixed (hopefully; relative paths might still be trouble)
        #try:
            
    
        #except:
            # if file path invalid, exits gracefully (we hope)
        #    print("Error: " + path + " is not a valid file path. Please double-check the input and try again.")
        #    sys.exit()
# read file
        p = pathlib.Path(path)
        # convert path to absolute
        p = p.absolute()
        with open(str(p), 'r') as f:
            thing = f.read()
        
        # regex black magic
        pattern = re.compile("^\s+|(//.+)|(/\*(.|\n)*?\*/)|^$|(^\n$)\s*", re.MULTILINE)
        export = re.sub(pattern, "", thing)
        # removes the empty newline at the beginning
        export = export.strip()

        final = ""
        # remove the lines that are just empty space
        exportList = export.splitlines()
        for i in exportList:
            if i != "":
                i = i.strip()
                final += i
                final += "\n"

        # turn Path into string so that we might change the extension
        exportPath = str(p)
        # change the file extension
        exportPath = exportPath.replace(".asm", ".hack")
        # now change it back
        exportPath = pathlib.Path(exportPath)

        self.exportPath = exportPath
        self.contents = final

    def makeVar(self, var):
        """
        Make a variable from the input provided.
        """
        global variableRAM
        symbols[var] = variableRAM
        variableRAM += 1
        return symbols[var]

    def aInstruction(self, line):
        # remove the @ symbol
        global address
        line = line[1:]
        if line[0].isalpha():
            # check if new or existing variable
            if line not in symbols.keys():
                address = Parser.makeVar(self, line)
            address = symbols.get(line)
        else:
            address = line
        # stick zeroes in front of the address as needed by converting to binary
        address = str(format(int(address), "b")).zfill(16)
        return address

    def cInstruction(self, line):
        """
        Takes in a c-instruction line and formats it to DEST=COMP;JUMP as needed.
        This one does the same thing as the CODE module suggested in nand2tetris.
        """
        # add dest and jump if not provided, so that we might split them later
        # adds the null dest
        if "=" not in line:
            line = "null" + "=" + line
        # adds the null jump
        if ";" not in line:
            line = line + ";" + "null"
        # split the line
        firstPart = line.split("=")
        destInst = firstPart[0]
        secondPart = firstPart[1].split(";")
        compInst = secondPart[0]
        jumpInst = secondPart[1]
        # turn dest, comp, jump into binary codes by looking them up
        destInst = dest.get(destInst)
        compInst = comp.get(compInst)
        jumpInst = jump.get(jumpInst)
        instruction = compInst+destInst+jumpInst
        return instruction

    def commandType(self, line):
        if line[0] == "@":
            return Parser.aInstruction(self, line)
        else:
            instruction = Parser.cInstruction(self, line)
            return "111" + instruction

    def translate(self):
        self.out = ""
        lines = self.contents.splitlines()
        index = 0
        # go through once and find all the loops
        for line in lines:
            # pattern matching for loops
            pattern = re.compile("^\(.+\)$")
            if re.match(pattern, line):
                # remove parentheses and assign line number to symbols
                line = line[1:-1]
                symbols[line] = index
                # do NOT increment the line counter, because it isn't technically a line
            else:
                index += 1
        # go through again
        for line in lines:
            # this time around skip the loops, they don't translate to anything
            pattern = re.compile("^\(.+\)$")
            if re.match(pattern, line):
                continue
            else:
                command = Parser.commandType(self, line)
                self.out += command
                self.out += "\n"
        with open(self.exportPath, 'w') as export:
            export.write(self.out)
        print("Successfully wrote to " + str(self.exportPath))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('assemble', help="Assemble target .asm file into .hack machine code.", type=str)
    args = parser.parse_args()

    if args.assemble:
        assembly = Parser(args.assemble)
        assembly = Parser.translate(assembly)

if __name__ == "__main__":
    main()
