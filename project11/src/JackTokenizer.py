#!/usr/bin/env python

"""
MPCS 52011 Project 11

Part 1
Jack Syntax Analyzer: Tokenizer

Ming Liu
"""

import re
import pathlib
import os.path
import argparse
import CompilationEngine
from collections import namedtuple

Token = namedtuple('Token',('type', 'value'))

class Analysis:
    # initialize keywords
    keywords = [
        "class",
        "constructor",
        "function",
        "method",
        "field",
        "static",
        "var",
        "int",
        "char",
        "boolean",
        "void",
        "true",
        "false",
        "null",
        "this",
        "let",
        "do",
        "if",
        "else",
        "while",
        "return"]

    # symbol conversion dictionary
    symbols = {
        "<": "&lt;",
        ">": "&gt;",
        "\"": "&quot;",
        "&": "&amp;"}

    def __init__(self, path):
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
            exportPath2 = exportPath.replace(".jack", "T.xml")
            exportPath2 = pathlib.Path(exportPath2)
            with open(str(p), "r") as f:
                thing = f.read()
        self.exportPath2 = exportPath2
        self.text = thing

    def whitespace(self):
        # regex black magic
        pattern = re.compile("^\s+|(//.+)|(/\*(.|\n)*?\*/)|^$|(^\n$)\s*", re.MULTILINE)
        export = re.sub(pattern, "", self.text)
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
        self.contents = final

    def analyze(self):
        tokenList = []
        index = 0
        while index < len(self.contents):
            token = ""
            # get the next character of the code
            char = self.contents[index]
            # I left newlines in as a relic of reusing old code
            if char == "\n":
                # so we ignore them here
                pass
            else:
                # check if string delimiter
                if self.isStringDelimiter(char):
                    token += char
                    index += 1
                    char = self.contents[index]
                    while not self.isStringDelimiter(char):
                        if self.isStringDelimiter(self.contents[index+1]):
                            token += self.contents[index]
                            index += 1
                            break
                        # maybe the next line is redundant, but who knows
                        char = self.contents[index]
                        token += char
                        index += 1
                    tokenList.append([token, "strConst"])
                # check if alphanumeric, or underscore (allowed in variable names)
                elif self.isAlphaNumeric(char):
                    token += char
                    last_location = index
                    index += 1
                    count = 0
                    char = self.contents[index]
                    while self.isAlphaNumeric(char):
                        # prevent running on into the symbol, we do not really have an overflow issue because everything ends in a symbol
                        if not self.isAlphaNumeric(self.contents[index+1]):
                            token += self.contents[index]
                            count += 1
                            index += 1
                            break
                        char = self.contents[index]
                        token += char
                        index += 1
                        count += 1
                    index = last_location + count
                    tokenList.append([token, "alphanumeric"])
                else:
                    # only symbols are left
                    if char in self.symbols:
                        token += self.symbols[char]
                    else:
                        token += char
                    tokenList.append([token, "symbol"])
            index += 1
        # clean up the token list by removing unneeded whitespace
        tokenList = [x for x in tokenList if x[0].isspace() == False]
        self.tokenList = tokenList

    def tokenize(self):
        self.tokens = ""
        self.tokens += "<tokens>\n"
        # also make a list of the raw tokens
        self.rawTokens = []
        for tokenSet in self.tokenList:
            token = tokenSet[0]
            tokenType = tokenSet[1]
            if tokenType == "strConst":
                # remove the quotation marks
                token = token[1:-1]
                self.rawTokens.append(Token(token, "stringConstant"))
                token += " "
                self.tokens += "<stringConstant> " + token + " </stringConstant>\n"
            elif tokenType == "alphanumeric":
                if token in Analysis.keywords:
                    self.tokens += "<keyword> " + token + " </keyword>\n"
                    self.rawTokens.append(Token(token, "keyword"))
                elif token.isnumeric():
                    self.tokens += "<integerConstant> " + token + " </integerConstant>\n"
                    self.rawTokens.append(Token(token, "integerConstant"))
                else:
                    self.tokens += "<identifier> " + token + " </identifier>\n"
                    self.rawTokens.append(Token(token, "identifier"))
            else:
                self.tokens += "<symbol> " + token + " </symbol>\n"
                self.rawTokens.append(Token(token, "symbol"))
        self.tokens += "</tokens>\n"
        with open(self.exportPath2, "w") as export:
            export.write(self.tokens)
        print("Successfully wrote token list to " + str(self.exportPath2))

    def isAlphaNumeric(self, token):
        return token.isalnum() or token == "_"
    
    def isStringDelimiter(self, token):
        # is it a quote for a string object
        return token == "\""
    
    def getCurrent(self):
        return self.rawTokens[0]

    def advance(self):
        return self.rawTokens.pop(0)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("analyze", help="tokenize target .jack file or directory of files into .xml format", type=str)
    args = parser.parse_args()

    if args.analyze:
        # mostly copied from Project 6
        p = pathlib.Path(args.analyze)
        # list of files to read
        files = []
        # convert path to absolute
        p = p.absolute()
        if os.path.isfile(p):
            files.append(p)
        else:
            for file in os.listdir(p):
                if file[-5:] == ".jack":
                    file = os.path.join(p, file)
                    files.append(pathlib.Path(file))
                    print(file)
            # exportPath2 was originally the tokenizer file path, but the tokenizer was written first
            exportPath2 = os.path.join(p, os.path.basename(p) + "T.xml")
            exportPath2 = pathlib.Path(exportPath2)
            exportPath1 = os.path.join(p, os.path.basename(p) + ".vm")
            exportPath1 = pathlib.Path(exportPath1)
            

        for file in files:
            print(file)
            exportPath1 = os.path.join(str(file)[:-5] + ".vm")
            print(exportPath1)
            jack = Analysis(file)
            jack.whitespace()
            jack.analyze()
            jack.tokenize()
            with open(exportPath1, 'w') as out:
                compile = CompilationEngine.CompilationEngine(jack, out)
                compile.compileClass()
                print(compile.vm.stream)

if __name__ == "__main__":
    main()