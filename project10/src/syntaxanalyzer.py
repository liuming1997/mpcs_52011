#!/usr/bin/env python

"""
MPCS 52011 Project 10, Part 1
Jack Syntax Analyzer

Ming Liu
"""

import re
import pathlib
import os.path
import argparse

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
        for tokenSet in self.tokenList:
            token = tokenSet[0]
            tokenType = tokenSet[1]
            if tokenType == "strConst":
                # remove the quotation marks
                token = token[1:-1]
                token += " "
                self.tokens += "<stringConstant> " + token + " </stringConstant>\n"
            elif tokenType == "alphanumeric":
                if token in Analysis.keywords:
                    self.tokens += "<keyword> " + token + " </keyword>\n"
                elif token.isnumeric():
                    self.tokens += "<integerConstant> " + token + " </integerConstant>\n"
                else:
                    self.tokens += "<identifier> " + token + " </identifier>\n"
            else:
                self.tokens += "<symbol> " + token + " </symbol>\n"
        self.tokens += "</tokens>\n"
        with open(self.exportPath2, "w") as export:
            export.write(self.tokens)
        print("Successfully wrote token list to " + str(self.exportPath2))
        # return a list of all of the tokens
        return self.tokens

    def isAlphaNumeric(self, token):
        return token.isalnum() or token == "_"
    
    def isStringDelimiter(self, token):
        # is it a quote for a string object
        return token == "\""

class Compile:
    # things that are allowed to end a line
    terminalTokens = ["stringConst", "intConst", "identifier", "symbol"]
    terminalKeywords = ["boolean", "class", "void", "int"]
    classVarDeclaration = ["static", "field"]
    subroutines = ["function", "method", "constructor", "void"]
    statements = ["do", "let", "while", "return", "if"]
    begin = {
        # lists so I can just go "if [x] in [y]"
        "variableDeclare" : ["var"],
        "parameterList" : ["("],
        "subroutineBody" : ["{"],
        "expressionList" : ["("],
        "expressionBody" : ["=", "(", "["]}
    end = {
        "class" : ["}"],
        "classVar" : [";"],
        "subroutine" : ["}"],
        "parameterList": [")"],
        "expressionList": [")"],
        "statements": ["}"],
        "do": [";"],
        "let": [";"],
        "while": ["}"],
        "if": ["}"],
        "variableDeclare": [";"],
        "return": [";"],
        "expression": [";", ")", "]", ","]}
    operators = [
        "+",
        "-",
        "*",
        "/",
        "&amp;",
        "|",
        "&lt;",
        "&gt;",
        "="]
    unary = ["-", "~"]

    def __init__(self, tokenList, path):
        # mostly copied from Project 6 so it's dreary and inefficient
        p = pathlib.Path(path)
        # list of files to read
        files = []
        exportPath = str(p)
        # convert path to absolute
        p = p.absolute()
        if os.path.isfile(p):
            files.append(p)
            exportPath1 = exportPath.replace(".jack", ".xml")
            exportPath1 = pathlib.Path(exportPath1)
        self.exportPath1 = exportPath1
        self.tokenList = tokenList
        self.text = ""
        # depth of tabs
        self.depth = 0

    def compileClass(self):
        # since everything is in a class, we use this as the basic building block
        self.text += "  " * self.depth + "<class>\n"
        self.depth += 1
        while 0 < len(self.tokenList): 
            intake = self.tokenList[0]
            tokenType = re.match("^<[a-zA-Z]*>", intake).group(0)[1:-1]
            token = str(re.sub("^<[a-zA-Z]*> ", "", intake))
            # remove the end
            token = str(re.sub(" </[a-zA-Z]*>$", "", token))
            if token in self.terminalKeywords or tokenType in self.terminalTokens:
                self.text += "  " * self.depth + "<" + tokenType + "> " + token + " </" + tokenType + ">\n"
            elif token in Compile.classVarDeclaration:
                self.writeClassVariable(token, tokenType)
            elif token in Compile.subroutines:
                self.writeSubroutine(token, tokenType)
            self.tokenList = self.tokenList[1:]
        self.depth -= 1
        self.text += "  " * self.depth + "</class>\n"
        with open(self.exportPath1, "w") as out:
            out.write(self.text)
        print("Successfully wrote decompiled XML to " + str(self.exportPath1))
    
    def writeClassVariable(self, token, tokenType):
        # example: field int a;
        self.depth += 1
        self.text += "  " * self.depth + "<classVarDec>\n"
        while token not in Compile.end["classVar"]:
            intake = self.tokenList[0]
            tokenType = re.match("^<[a-zA-Z]*>", intake).group(0)[1:-1]
            token = str(re.sub("^<[a-zA-Z]*> ", "", intake))
            # remove the end
            token = str(re.sub(" </[a-zA-Z]*>$", "", token))
            if token in self.terminalKeywords or tokenType in self.terminalTokens:
                self.text += "  " * self.depth + "<" + tokenType + "> " + token + " </" + tokenType + ">\n"
            self.tokenList = self.tokenList[1:]
        self.text += "  " * self.depth + "</classVarDec>\n"
        self.depth -= 1

    def writeSubroutine(self, token, tokenType):
        self.text += "  " * self.depth + "<subroutineDec>\n"
        if token in self.terminalKeywords or tokenType in self.terminalTokens:
            self.text += "  " * self.depth + "<" + tokenType + "> " + token + " </" + tokenType + ">\n"
        self.depth += 1
        while token not in Compile.end["subroutine"] and 0 < len(self.tokenList):
            intake = self.tokenList[0]
            tokenType = re.match("^<[a-zA-Z]*>", intake).group(0)[1:-1]
            token = str(re.sub("^<[a-zA-Z]*> ", "", intake))
            # remove the end
            token = str(re.sub(" </[a-zA-Z]*>$", "", token))
            if token in self.begin["parameterList"]:
                self.writeParameterList(token, tokenType)
            elif token in self.begin["subroutineBody"]:
                self.writeSubroutineBody(token, tokenType)
            else:
                # it's terminal
                self.text += "  " * self.depth + "<" + tokenType + "> " + token + " </" + tokenType + ">\n"
            self.tokenList = self.tokenList[1:]
        self.depth -= 1
        self.text += "  " * self.depth + "</subroutineDec>\n"

    def writeParameterList(self, token, tokenType):
        # ex: dispose(int a, char b)
        if token in self.terminalKeywords or tokenType in self.terminalTokens:
            self.text += "  " * self.depth + "<" + tokenType + "> " + token + " </" + tokenType + ">\n"
        self.text += "  " * self.depth + "<parameterList>\n"
        nextIntake = self.tokenList[0+1]
        nextToken = str(re.sub("^<[a-zA-Z]*> ", "", nextIntake))
        nextToken = str(re.sub(" </[a-zA-Z]*>$", "", nextToken))
        while nextToken not in Compile.end["parameterList"]:
            intake = self.tokenList[0]
            tokenType = re.match("^<[a-zA-Z]*>", intake).group(0)[1:-1]
            token = str(re.sub("^<[a-zA-Z]*> ", "", intake))
            token = str(re.sub(" </[a-zA-Z]*>$", "", token))
            nextIntake = self.tokenList[0+1]
            nextToken = str(re.sub("^<[a-zA-Z]*> ", "", nextIntake))
            nextToken = str(re.sub(" </[a-zA-Z]*>$", "", nextToken))
            if nextToken in Compile.end["parameterList"]:
                break
            elif token in self.terminalKeywords or tokenType in self.terminalTokens:
                self.text += "  " * self.depth + "<" + tokenType + "> " + token + " </" + tokenType + ">\n"
            self.tokenList = self.tokenList[1:]
        self.text += "  " * self.depth + "</parameterList>\n"
        self.tokenList = self.tokenList[1:]
        intake = self.tokenList[0]
        tokenType = re.match("^<[a-zA-Z]*>", intake).group(0)[1:-1]
        token = str(re.sub("^<[a-zA-Z]*> ", "", intake))
        token = str(re.sub(" </[a-zA-Z]*>$", "", token))
        if token in self.terminalKeywords or tokenType in self.terminalTokens:
            self.text += "  " * self.depth + "<" + tokenType + "> " + token + " </" + tokenType + ">\n"

    def writeSubroutineBody(self, token, tokenType):
        self.text += "  " * self.depth + "<subroutineBody>\n"
        self.depth += 1
        self.text += "  " * self.depth + "<" + tokenType + "> " + token + " </" + tokenType + ">\n"
        while token not in Compile.end["subroutine"]:
            intake = self.tokenList[0]
            tokenType = re.match("^<[a-zA-Z]*>", intake).group(0)[1:-1]
            token = str(re.sub("^<[a-zA-Z]*> ", "", intake))
            token = str(re.sub(" </[a-zA-Z]*>$", "", token))
            if token == "var":
                self.writeVariable(token, tokenType)
            elif token in self.statements:
                self.writeStatement(token, tokenType)
            else:
                if token in self.terminalKeywords or tokenType in self.terminalTokens:
                    self.text += "  " * self.depth + "<" + tokenType + "> " + token + " </" + tokenType + ">\n"
            self.tokenList = self.tokenList[1:]

        if token in self.terminalKeywords or tokenType in self.terminalTokens:
            self.text += "  " * self.depth + "<" + tokenType + "> " + token + " </" + tokenType + ">\n"
        self.depth -= 1
        self.text += "  " * self.depth + "</subroutineBody>\n"
    
    def writeVariable(self, token, tokenType):
        # example: var int a
        self.text += "  " * self.depth + "<varDec>\n"
        self.depth += 1
        if token in self.terminalKeywords or tokenType in self.terminalTokens:
            self.text += "  " * self.depth + "<" + tokenType + "> " + token + " </" + tokenType + ">\n"
        while token not in self.end["variableDeclare"]:
            intake = self.tokenList[0]
            tokenType = re.match("^<[a-zA-Z]*>", intake).group(0)[1:-1]
            token = str(re.sub("^<[a-zA-Z]*> ", "", intake))
            token = str(re.sub(" </[a-zA-Z]*>$", "", token))
            self.text += "  " * self.depth + "<" + tokenType + "> " + token + " </" + tokenType + ">\n"
            self.tokenList = self.tokenList[1:]
        self.depth -= 1
        self.text += "  " * self.depth + "</varDec>\n"

    def writeStatement(self, token, tokenType):
        self.text += "  " * self.depth + "<statements>\n"
        self.depth += 1
        if token == "if":
            self.writeIf(token, tokenType)
        elif token == "do":
            self.writeDo(token, tokenType)
        elif token == "let":
            self.writeLet(token, tokenType)
        elif token == "while":
            self.writeWhile(token, tokenType)
        elif token == "return":
            self.writeReturn(token, tokenType)
        self.tokenList = self.tokenList[1:]
        self.depth -= 1
        self.text += "  " * self.depth + "</statements>\n"
    
    def writeDo(self, token, tokenType):
        # ex: do ship.sink()
        self.text += "  " * self.depth + "<doStatement>\n"
        self.depth += 1
        if token in self.terminalKeywords or tokenType in self.terminalTokens:
            self.text += "  " * self.depth + "<" + tokenType + "> " + token + " </" + tokenType + ">\n"
        while token not in self.end["do"]:
            intake = self.tokenList[0]
            tokenType = re.match("^<[a-zA-Z]*>", intake).group(0)[1:-1]
            token = str(re.sub("^<[a-zA-Z]*> ", "", intake))
            token = str(re.sub(" </[a-zA-Z]*>$", "", token))
            if token in self.begin["expressionBody"]:
                self.writeExpression(token, tokenType)
            else:
                self.text += "  " * self.depth + "<" + tokenType + "> " + token + " </" + tokenType + ">\n"
            self.tokenList = self.tokenList[1:]
        self.depth -= 1
        self.text += "  " * self.depth + "</doStatement>\n"

    def writeLet(self, token, tokenType):
        self.text += "  " * self.depth + "<letStatement>\n"
        self.depth += 1
        if token in self.terminalKeywords or tokenType in self.terminalTokens:
            self.text += "  " * self.depth + "<" + tokenType + "> " + token + " </" + tokenType + ">\n"
        while token not in self.end["let"]:
            intake = self.tokenList[0]
            tokenType = re.match("^<[a-zA-Z]*>", intake).group(0)[1:-1]
            token = str(re.sub("^<[a-zA-Z]*> ", "", intake))
            token = str(re.sub(" </[a-zA-Z]*>$", "", token))
            if token in self.begin["expressionBody"]:
                self.writeExpression(token, tokenType)
            else:
                self.text += "  " * self.depth + "<" + tokenType + "> " + token + " </" + tokenType + ">\n"
            self.tokenList = self.tokenList[1:]
            intake = self.tokenList[0]
            tokenType = re.match("^<[a-zA-Z]*>", intake).group(0)[1:-1]
            token = str(re.sub("^<[a-zA-Z]*> ", "", intake))
            token = str(re.sub(" </[a-zA-Z]*>$", "", token))
        self.depth -= 1
        self.text += "  " * self.depth + "</letStatement>\n"
    
    def writeWhile(self, token, tokenType):
        self.text += "  " * self.depth + "<whileStatement>\n"
        self.depth += 1
        if token in self.terminalKeywords or tokenType in self.terminalTokens:
            self.text += "  " * self.depth + "<" + tokenType + "> " + token + " </" + tokenType + ">\n"
        while token not in self.end["while"]:
            intake = self.tokenList[0]
            tokenType = re.match("^<[a-zA-Z]*>", intake).group(0)[1:-1]
            token = str(re.sub("^<[a-zA-Z]*> ", "", intake))
            token = str(re.sub(" </[a-zA-Z]*>$", "", token))
            if token in self.begin["expressionBody"]:
                self.writeExpression(token, tokenType)
            else:
                self.text += "  " * self.depth + "<" + tokenType + "> " + token + " </" + tokenType + ">\n"
            self.tokenList = self.tokenList[1:]
        self.depth -= 1
        self.text += "  " * self.depth + "</whileStatement>\n"

    def writeReturn(self, token, tokenType):
        self.text += "  " * self.depth + "<returnStatement>\n"
        self.depth += 1
        if token in self.terminalKeywords or tokenType in self.terminalTokens:
            self.text += "  " * self.depth + "<" + tokenType + "> " + token + " </" + tokenType + ">\n"
        while token not in self.end["return"]:
            intake = self.tokenList[0]
            tokenType = re.match("^<[a-zA-Z]*>", intake).group(0)[1:-1]
            token = str(re.sub("^<[a-zA-Z]*> ", "", intake))
            token = str(re.sub(" </[a-zA-Z]*>$", "", token))
            if token in self.begin["expressionBody"]:
                self.writeExpression(token, tokenType)
            else:
                self.text += "  " * self.depth + "<" + tokenType + "> " + token + " </" + tokenType + ">\n"
            self.tokenList = self.tokenList[1:]
        self.depth -= 1
        self.text += "  " * self.depth + "</returnStatement>\n"

    def writeIf(self, token, tokenType):
        self.text += "  " * self.depth + "<ifStatement>\n"
        self.depth += 1
        if token in self.terminalKeywords or tokenType in self.terminalTokens:
            self.text += "  " * self.depth + "<" + tokenType + "> " + token + " </" + tokenType + ">\n"
        while token not in self.end["if"]:
            intake = self.tokenList[0]
            tokenType = re.match("^<[a-zA-Z]*>", intake).group(0)[1:-1]
            token = str(re.sub("^<[a-zA-Z]*> ", "", intake))
            token = str(re.sub(" </[a-zA-Z]*>$", "", token))
            if token in self.begin["expressionBody"]:
                self.writeExpression(token, tokenType)
            else:
                self.text += "  " * self.depth + "<" + tokenType + "> " + token + " </" + tokenType + ">\n"
            self.tokenList = self.tokenList[1:]
        self.depth -= 1
        self.text += "  " * self.depth + "</ifStatement>\n"

    def writeExpression(self, token, tokenType):
        self.text += "  " * self.depth + "<letStatement>\n"
        self.depth += 1
        self.text += "  " * self.depth + "<" + tokenType + "> " + token + " </" + tokenType + ">\n"
        while token not in self.end["expression"]:
            intake = self.tokenList[0]
            tokenType = re.match("^<[a-zA-Z]*>", intake).group(0)[1:-1]
            token = str(re.sub("^<[a-zA-Z]*> ", "", intake))
            token = str(re.sub(" </[a-zA-Z]*>$", "", token))
            self.text += "  " * self.depth + "<" + tokenType + "> " + token + " </" + tokenType + ">\n"
            self.tokenList = self.tokenList[1:]
        self.depth -= 1
        self.text += "  " * self.depth + "</letStatement>\n"

    def writeExpressionList():
        pass

    def writeTerm():
        pass

    

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
            # exportPath2 was originally the tokenizer file path, but the tokenizer was written first
            exportPath2 = os.path.join(p, os.path.basename(p) + "T.xml")
            exportPath2 = pathlib.Path(exportPath2)
            exportPath1 = str(exportPath2).replace("T.xml", ".xml")
            exportPath1 = pathlib.Path(exportPath1)
        for file in files:
            jack = Analysis(file)
            jack.whitespace()
            jack.analyze()
            tokenXML = jack.tokenize().splitlines()[1:-1]
            jack2 = Compile(tokenXML, file)
            jack2.compileClass()

if __name__ == "__main__":
    main()