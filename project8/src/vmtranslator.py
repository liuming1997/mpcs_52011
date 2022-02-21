"""
MPCS 52011 Project 7: VM translator, Part 1
"""

#!/usr/bin/env python

import pathlib
import re
import argparse
import os

commands = {
    # "if" is "if-goto", but terse
    "push" : "push",
    "pop" : "pop",
    "add" : "math",
    "sub" : "math",
    "neg" : "math",
    "eq"  : "math",
    "gt"  : "math",
    "lt"  : "math",
    "and" : "math",
    "or"  : "math",
    "not" : "math",
    "label" : "label",
    "goto" : "goto",
    "if-goto" : "if",
    "call" : "call",
    "return" : "return",
    "function" : "function"
}

lineNum = 1

class Parser:
    def __init__(self, path):
        """
        Initialize the Parser class by taking in a file.
        Still has some trouble with relative paths.
        Note: This currently DOES NOT work for all files in a directory. It works well enough for Project 7, though.
        """
        # mostly copied from Project 6
        p = pathlib.Path(path)
        # list of files to read
        files = []
        thing = ""
        exportPath = str(p)
        # convert path to absolute
        p = p.absolute()
        if os.path.isfile(p):
            files.append(p)
            exportPath = exportPath.replace(".vm", ".asm")
            exportPath = pathlib.Path(exportPath)
            with open(str(p), "r") as f:
                thing = f.read()
        else:
            for file in os.listdir(p):
                if file[-3:] == ".vm":
                    file = os.path.join(p, file)
                    files.append(pathlib.Path(file))
            exportPath = os.path.join(p, os.path.basename(p) + ".asm")
            exportPath = pathlib.Path(exportPath)
            for file in files:
                with open(file, "r") as f:
                    thing += f.read()
        
        # do .vm files even have comments? remove them anyway, just in case
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
        # change the file extension
        # now change it back
        self.exportPath = exportPath
        self.contents = final

    def translate(self):
        global commands
        self.index = 0
        self.out = ""
        # in the case of repetitions, mostly for FibonacciElement
        self.iter = 0
        lines = self.contents.splitlines()
        # initialize
        self.out += "@256\n"
        self.out += "D=A\n"
        self.out += "@SP\n"
        self.out += "M=D\n"
        # this part is apparently just broken
        Parser.writeCall(self, "Sys.init", 0)
        # now the rest
        for line in lines:
            orders = line.split()
            orderType = commands.get(orders[0], "no command")
            if orderType == "push" or orderType == "pop":
                first = orders[1]
                second = orders[2]
                Parser.writePushPop(self, orderType, first, second)
            elif orderType == "math":
                Parser.writeArithmetic(self, orders[0])
            elif orderType == "label":
                Parser.writeLabel(self, orders[1])
            elif orderType == "goto":
                Parser.writeGoto(self, orders[1])
            elif orderType == "if":
                Parser.writeIf(self, orders[1])
            elif orderType == "call":
                first = orders[1]
                second = orders[2]
                Parser.writeCall(self, first, second)
            elif orderType == "return":
                Parser.writeReturn(self)
            elif orderType == "function":
                first = orders[1]
                second = orders[2]
                Parser.writeFunction(self, first, second)
            else:
                # do nothing, if it can"t figure out what to do instead
                continue
        with open(self.exportPath, "w") as export:
            export.write(self.out)
        print("Successfully wrote to " + str(self.exportPath))

    def loadNumbers(self):
        # Loads the first value into the data register, and puts the second in memory. This happens a lot, so might as well save some lines.
        self.out += "@SP\n"
        self.out += "AM=M-1\n"
        self.out += "D=M\n" 
        self.out += "@SP\n"
        self.out += "AM=M-1\n" 

    def loadNumbers2(self):
        # Like loadNumbers, but with one key difference.
        self.out += "@SP\n"
        self.out += "AM=M-1\n"
        self.out += "D=M\n" 
        self.out += "@SP\n"
        self.out += "AM=M-1\n"
        self.out += "D=D-M\n"

    def writeArithmetic(self, math):
        global lineNum
        # write a line number so I can tell what translates to what
        # used for debugging
        # self.out += "// line number " + str(lineNum) + " math \n"
        if math == "add":
            Parser.loadNumbers(self)
            # write the sum
            self.out += "M=D+M\n" 
            self.out += "@SP\n"
            self.out += "M=M+1\n" 
        elif math == "sub":
            Parser.loadNumbers(self)
            # write difference
            self.out += "M=M-D\n" 
            self.out += "@SP\n"
            self.out += "M=M+1\n" 
        elif math == "neg":
            # get value
            self.out += "@SP\n" 
            self.out += "A=M-1\n"
            # negate said value 
            self.out += "M=-M\n"
        elif math == "eq":
            Parser.loadNumbers2(self)
            self.out += "@eq" + str(self.index) + "\n"
            self.out += "D;JEQ\n"
            self.out += "D=0\n"
            self.out += "@eq_end" + str(self.index) + "\n"
            self.out += "0;JMP\n"
            self.out += "(eq" + str(self.index) + ")\n"
            self.out += "D=-1\n"
            self.out += "(eq_end" + str(self.index) + ")\n"
            self.out += "@SP\n"
            self.out += "A=M\n"
            self.out += "M=D\n"
            self.out += "@SP\n"
            self.out += "M=M+1\n"
            self.index += 1
        elif math == "gt":
            # mostly copied from eq
            Parser.loadNumbers2(self)
            self.out += "@gt" + str(self.index) + "\n"
            self.out += "D;JLT\n"
            self.out += "D=0\n"
            self.out += "@gt_end" + str(self.index) + "\n"
            self.out += "0;JMP\n"
            self.out += "(gt" + str(self.index) + ")\n"
            self.out += "D=-1\n"
            self.out += "(gt_end" + str(self.index) + ")\n"
            self.out += "@SP\n"
            self.out += "A=M\n"
            self.out += "M=D\n"
            self.out += "@SP\n"
            self.out += "M=M+1\n"
            self.index += 1
        elif math == "lt":
            # also mostly copied from eq
            Parser.loadNumbers2(self)
            self.out += "@lt" + str(self.index) + "\n"
            self.out += "D;JGT\n"
            self.out += "D=0\n"
            self.out += "@lt_end" + str(self.index) + "\n"
            self.out += "0;JMP\n"
            self.out += "(lt" + str(self.index) + ")\n"
            self.out += "D=-1\n"
            self.out += "(lt_end" + str(self.index) + ")\n"
            self.out += "@SP\n"
            self.out += "A=M\n"
            self.out += "M=D\n"
            self.out += "@SP\n"
            self.out += "M=M+1\n"
            self.index += 1
        elif math == "and":
            Parser.loadNumbers2(self)
            # put result into stack
            self.out += "M=D&M\n" 
        elif math == "or":
            Parser.loadNumbers2(self)
            # put result into stack
            self.out += "M=D|M\n" 
        elif math == "not":
            # get value
            self.out += "@SP\n" 
            self.out += "A=M-1\n" 
            # NOT said value
            self.out += "M=!M\n" 
        else:
            # do nothing if not otherwise covered
            pass

    def putOnStack(self):
        # puts something to the stack
        self.out += "@SP\n"
        self.out += "A=M\n"
        self.out += "M=D\n"

    def incrementStackPointer(self):
        # Increments the stack pointer since it comes up so much.
        self.out += "@SP\n" 
        self.out += "M=M+1\n"

    def commonInst(self):
        # I don't know what else to call it
        # populate value into D
        self.out += "@SP\n" 
        self.out += "AM=M-1\n"
        self.out += "D=M\n"
        # just R13 address things
        self.out += "@R13\n"
        self.out += "A=M\n"
        self.out += "M=D\n"

    def writePushPop(self, order, seg, value):
        global lineNum
        # write a line number so I can tell what translates to what
        # used for debugging
        # self.out += "// line number " + str(lineNum) + "\n"
        if order == "push":
            self.out += "// push " + seg + str(value) + " \n"
            if seg == "constant":
                # load value, move to D
                self.out += "@" + value + "\n" 
                self.out += "D=A\n" 
                # laod stack pointer, put on stack
                self.out += "@SP\n" 
                self.out += "A=M\n" 
                self.out += "M=D\n" 
                Parser.incrementStackPointer(self)
            elif seg == "static":
                # load value, get contents of memory
                self.out += "@" + value + "\n"
                self.out += "D=M\n"
                # load stack pointer, put on stack
                self.out += "@SP\n" 
                self.out += "A=M\n" 
                self.out += "M=D\n"
                Parser.incrementStackPointer(self)
            elif seg == "this":
                # load value into D
                self.out += "@" + value + "\n"
                self.out += "D=A\n"
                self.out += "@THIS\n"
                self.out += "A=M+D\n" 
                self.out += "D=M\n"
                Parser.putOnStack(self)
                Parser.incrementStackPointer(self)
            elif seg == "that":
                # load value into D
                self.out += "@" + value + "\n" 
                self.out += "D=A\n"
                self.out += "@THAT\n"
                self.out += "A=M+D\n" 
                self.out += "D=M\n"
                Parser.putOnStack(self)
                Parser.incrementStackPointer(self)
            elif seg == "argument":
                # load value into D
                self.out += "@" + value + "\n"
                self.out += "D=A\n"
                self.out += "@ARG\n"
                self.out += "D=D+M\n"
                self.out += "@temp\n"
                self.out += "M=D\n"
                self.out += "@temp\n"
                self.out += "A=M\n"
                self.out += "D=M\n"
                Parser.putOnStack(self)
                Parser.incrementStackPointer(self)
            elif seg == "local":
                # load value into D
                self.out += "@" + value + "\n"
                self.out += "D=A\n"
                self.out += "@LCL\n"
                self.out += "D=D+M\n"
                self.out += "@temp\n"
                self.out += "M=D\n"
                self.out += "@temp\n"
                self.out += "A=M\n"
                self.out += "D=M\n"
                Parser.putOnStack(self)
                Parser.incrementStackPointer(self)
            elif seg == "temp":
                # load value into D
                self.out += "@" + value + "\n" 
                self.out += "D=A\n"
                self.out += "@5\n"
                self.out += "A=A+D\n" 
                self.out += "D=M\n"
                Parser.putOnStack(self)
                Parser.incrementStackPointer(self)
            elif seg == "pointer":
                # load value into D
                self.out += "@" + value + "\n" 
                self.out += "D=A\n"
                self.out += "@3\n"
                self.out += "A=A+D\n" 
                self.out += "D=M\n"
                Parser.putOnStack(self)
                Parser.incrementStackPointer(self)
            else:
                # if it isn't one of the above do nothing
                pass
        elif order == "pop":
            self.out += "// pop \n"
            if seg == "static":
                # populate value into D
                self.out += "@SP\n" 
                self.out += "AM=M-1\n"
                self.out += "D=M\n"
                self.out += "@" + value + "\n"
                self.out += "M=D\n"
            elif seg == "this":
                # get address into R13
                self.out += "@" + value + "\n" 
                self.out += "D=A\n"
                self.out += "@THIS\n"
                self.out += "D=M+D\n" 
                self.out += "@R13\n"
                self.out += "M=D\n"
                Parser.commonInst(self)
            elif seg == "that":
                # get address into R13
                self.out += "@" + value + "\n" 
                self.out += "D=A\n"
                self.out += "@THAT\n"
                self.out += "D=M+D\n" 
                self.out += "@R13\n"
                self.out += "M=D\n"
                Parser.commonInst(self)
            elif seg == "argument":
                self.out += "@" + value + "\n" 
                self.out += "D=A\n"
                self.out += "@ARG\n"
                self.out += "D=M+D\n" 
                self.out += "@temp\n"
                self.out += "M=D\n"
                self.out += "@SP\n"
                self.out += "M=M-1\n"
                self.out += "@SP\n"
                self.out += "A=M\n"
                self.out += "D=M\n"
                self.out += "@temp\n"
                self.out += "A=M\n"
                self.out += "M=D\n"
            elif seg == "local":
                self.out += "@" + value + "\n" 
                self.out += "D=A\n"
                self.out += "@LCL\n"
                self.out += "D=M+D\n" 
                self.out += "@temp\n"
                self.out += "M=D\n"
                self.out += "@SP\n"
                self.out += "M=M-1\n"
                self.out += "@SP\n"
                self.out += "A=M\n"
                self.out += "D=M\n"
                self.out += "@temp\n"
                self.out += "A=M\n"
                self.out += "M=D\n"
            elif seg == "pointer":
                # get address into R13
                self.out += "@" + value + "\n" 
                self.out += "D=A\n"
                self.out += "@3\n"
                self.out += "D=A+D\n" 
                self.out += "@R13\n"
                self.out += "M=D\n"
                Parser.commonInst(self)
            elif seg == "temp":
                # get address into R13
                self.out += "@" + value + "\n" 
                self.out += "D=A\n"
                self.out += "@5\n"
                self.out += "D=A+D\n" 
                self.out += "@R13\n"
                self.out += "M=D\n"
                Parser.commonInst(self)
            else:
                # do nothing if not covered yet (will revise in project 8)
                pass

    def writeLabel(self, label):
        self.out += "(" + label + ")\n"

    def writeGoto(self, jump):
        self.out += "// goto " + jump + "\n"
        self.out += "@" + jump + "\n"
        self.out += "0;JMP\n"

    def incrementSP(self):
        """
        Increment SP, because it happens a lot.
        """
        self.out += "@SP\n"
        self.out += "M=M+1\n"
    
    def manipulateSP(self):
        """
        This command just happens a bunch.
        """
        self.out += "@SP\n"
        self.out += "A=M\n"
        self.out += "M=D\n"

    def endEffector(self):
        """
        Also happens a lot in writeReturn.
        """
        self.out += "@ends\n"
        self.out += "M=M-1\n"
        self.out += "A=M\n"
        self.out += "D=M\n"

    def writeIf(self, conditional):
        global lineNum
        self.out += "// if goto at " + str(lineNum) + "\n"
        self.out += "@SP\n"
        self.out += "M=M-1\n"
        self.out += "A=M\n"
        self.out += "D=M\n"
        self.out += "@" + conditional + "\n"
        self.out += "D;JNE\n"
        lineNum += 1

    def writeCall(self, func, args):
        global lineNum
        self.out += "// call at line " + str(lineNum) + " for function " + func + "\n"
        self.out += "@" + func + "_" + str(self.iter) + "\n"
        self.out += "D=A\n"
        Parser.manipulateSP(self)
        Parser.incrementSP(self)
        # push the frame
        self.out += "@LCL\n"
        self.out += "D=M\n"
        Parser.manipulateSP(self)
        Parser.incrementSP(self)
        self.out += "@ARG\n"
        self.out += "D=M\n"
        Parser.manipulateSP(self)
        Parser.incrementSP(self)
        self.out += "@THIS\n"
        self.out += "D=M\n"
        Parser.manipulateSP(self)
        Parser.incrementSP(self)
        self.out += "@THAT\n"
        self.out += "D=M\n"
        Parser.manipulateSP(self)
        Parser.incrementSP(self)

        # set ARG = SP - 5 - args
        self.out += "@SP\n"
        self.out += "D=M\n"
        self.out += "@5\n"
        self.out += "D=D-A\n"
        self.out += "@" + str(args) + "\n"
        self.out += "D=D-A\n"
        self.out += "@ARG\n"
        self.out += "M=D\n"

        # set LCL = SP
        self.out += "@SP\n"
        self.out += "D=M\n"
        self.out += "@LCL\n"
        self.out += "M=D\n"
            
        # goto function_name
        self.out += "@" + func + "\n"
        self.out += "0;JMP\n"    
        self.out += "(" + func + "_" + str(self.iter)  + ")\n"
        lineNum += 1
        self.iter += 1

    def writeReturn(self):
        # set ends = LCL
        self.out += "@LCL\n"
        self.out += "D=M\n"
        self.out += "@ends\n"
        self.out += "M=D\n"

        # set return address
        self.out += "@ends\n"
        self.out += "D=M\n"
        self.out += "@5\n"
        self.out += "A=D-A\n"
        self.out += "D=M\n"
        self.out += "@ret\n"
        self.out += "M=D\n"
            
        self.out += "@SP\n"
        self.out += "M=M-1\n"
        self.out += "A=M\n"
        self.out += "D=M\n"
        self.out += "@ARG\n"
        self.out += "A=M\n"
        self.out += "M=D\n"
            
        # SP = ARG + 1
        self.out += "@ARG\n"
        self.out += "M=M+1\n"
        self.out += "D=M\n"
        self.out += "@SP\n"
        self.out += "M=D\n"

        # THIS = ends - 1
        # THAT = ends - 2
        # ARG = ends - 3
        # LCL = ends - 4
        Parser.endEffector(self)
        self.out += "@THAT\n"
        self.out += "M=D\n"
        Parser.endEffector(self)
        self.out += "@THIS\n"
        self.out += "M=D\n"
        Parser.endEffector(self)
        self.out += "@ARG\n"
        self.out += "M=D\n"
        Parser.endEffector(self)
        self.out += "@LCL\n"
        self.out += "M=D\n"

        # goto ret
        self.out += "@ret\n"
        self.out += "A=M\n"
        self.out += "0;JMP\n"

    def writeFunction(self, func, intake):
        self.out += "// a function called " + func + "\n"
        self.out += "(" + func + ")\n"
        self.out += "@i\n"
        self.out += "M=0\n"
        self.out += "@" + intake + "\n"
        self.out += "D=A\n"
        self.out += "@n\n"
        self.out += "M=D\n"
        # while (x > y)
        self.out += "(" + func + "_LOOP)\n"
        self.out += "@n\n"
        self.out += "D=M\n"
        self.out += "@i\n"
        self.out += "D=D-M\n"
        self.out += "@" + func + "_ENDLOOP\n"
        self.out += "D;JEQ\n"
        # push 0
        self.out += "@SP\n"
        self.out += "A=M\n"
        self.out += "M=0\n"

        # increment x and SP
        self.out += "@i\n"
        self.out += "M=M+1\n"
        Parser.incrementSP(self)
            
        self.out += "@" + func + "_LOOP\n"
        self.out += "0;JMP\n"
        self.out += "(" + func + "_ENDLOOP)\n"
        self.iter += 1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("translate", help="translate target .vm file into .asm code", type=str)
    args = parser.parse_args()

    if args.translate:
        vm = Parser(args.translate)
        vm = Parser.translate(vm)

if __name__ == "__main__":
    main()
