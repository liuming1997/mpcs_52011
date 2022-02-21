import VMWriter
import SymbolTable

indent = 2
operations = {"+": "add",
              "-": "sub",
              "*": "call Math.multiply 2",
              "/": "call Math.divide 2",
              "&": "and",
              "|": "or",
              "<": "lt",
              ">": "gt",
              "=": "eq"}

labelCount = 0

class CompilationEngine:
    """
    A compilation engine for Jack
    """

    def __init__(self, tokenizer, output):
        """
        Initialize the compilation engine, taking in a tokenized list and creating the output.
        """
        self.tokenizer = tokenizer
        self.vm = VMWriter.VMWriter(output)

    @staticmethod
    def getLabel():
        """
        Return a label for use
        """
        global labelCount

        label = "L{}".format(labelCount)
        labelCount += 1

        return label

    def compileClass(self):
        """Compile a class block"""
        self.tokenizer.advance() # class

        # class name
        className = self.tokenizer.advance()
        jackClass = SymbolTable.JackClass(className)

        self.tokenizer.advance() 

        self.compileClassVars(jackClass)
        self.compileClassSubroutines(jackClass)

        self.tokenizer.advance() 

    def compileClassVars(self, jackClass):
        """Compile the class variable declarations"""
        
        token = self.tokenizer.getCurrent()
        while token != None and token.type == "keyword" and token.value in ["static", "field"]:
            # Advance here, to avoid eating the token in the condition above
            # and losing the token when needed afterwards
            self.tokenizer.advance()
            
            is_static = token.value == "static"
            # var type
            varType = self.tokenizer.advance().value

            more = True
            while more:
                # var name
                varName = self.tokenizer.advance().value

                if is_static:
                    jackClass.addStatic(varName, varType)
                else:
                    jackClass.addField(varName, varType)

                token = self.tokenizer.advance()
                more = token == ("symbol", ",")

            # load next token, to check if another var declaration
            token = self.tokenizer.getCurrent()

    def compileClassSubroutines(self, jackClass):
        """Compile the class subroutines"""
        
        token = self.tokenizer.getCurrent()
        while token != None and token.type == "keyword" and token.value in ["constructor", "function", "method"]:
            
            # Advance for same reason as in varDec
            subroutineType = self.tokenizer.advance().value
            # get return type
            returnType = self.tokenizer.advance().value
            # name
            name = self.tokenizer.advance().value

            subroute = SymbolTable.JackSubroutine(name, subroutineType, returnType, jackClass)

            self.tokenizer.advance()  
            self.compileParameterList(subroute)
            self.tokenizer.advance()
            self.compileSubroutineBody(subroute)

            # load the next token to check 
            token = self.tokenizer.getCurrent()

    def compileParameterList(self, subroute):
        """Compile a parameter list for a subroutine"""

        token = self.tokenizer.getCurrent()
        # Check if the next token is a valid variable type
        more = token != None and token.type in ["keyword", "identifier"]
        while more:
            # param type
            token = self.tokenizer.advance() # Don"t advance to avoid eating
            param_type = token.value
            # param name
            param_name = self.tokenizer.advance().value

            subroute.add_arg(param_name, param_type)

            token = self.tokenizer.getCurrent()
            # If there are still vars
            if token == ("symbol", ","):
                self.tokenizer.advance() # Throw the "," away
                token = self.tokenizer.getCurrent()
                more = token != None and token.type in ["keyword", "identifier"]
            else:
                more = False


    def compileSubroutineBody(self, subroute):
        """Compile the subroutine body"""

        self.tokenizer.advance() 

        self.compileSubroutineVars(subroute)

        self.vm.writeFunction(subroute)

        if subroute.subroutineType == "constructor":
            field_count = subroute.jackClass.fieldSymbols
            self.vm.writePush("constant", field_count)
            self.vm.writeCall("Memory", "alloc", 1)
            # Set "this" in the function to allow it to return it
            self.vm.writePop("pointer", 0)
        elif subroute.subroutineType == "method":
            self.vm.writePush("argument", 0)
            self.vm.writePop("pointer", 0)

        self.compileStatements(subroute)

        self.tokenizer.advance()

    def compileSubroutineVars(self, subroute):
        """Compile the variable declerations of a subroutine"""

        token = self.tokenizer.getCurrent()
        # Check that a variable declarations starts
        while token != None and token == ("keyword", "var"):
            self.tokenizer.advance()
            # varType
            varType = self.tokenizer.advance().value
            # varName
            varName = self.tokenizer.advance().value

            subroute.addVar(varName, varType)

            # repeat as long as there are parameters, o.w eats the semi-colon
            while self.tokenizer.advance().value == ",":
                # varName
                varName = self.tokenizer.advance().value
                subroute.addVar(varName, varType)

            token = self.tokenizer.getCurrent()

    def compileStatements(self, subroute):
        """
        Compile subroutine
        """

        check_statements = True
        while check_statements:
            token = self.tokenizer.getCurrent()

            if token == ("keyword", "if"):
                self.compileIf(subroute)
            elif token == ("keyword", "while"):
                self.compileWhile(subroute)
            elif token == ("keyword", "let"):
                self.compileLet(subroute)
            elif token == ("keyword", "do"):
                self.compileDo(subroute)
            elif token == ("keyword", "return"):
                self.compileReturn(subroute)
            else:
                check_statements = False

    def compileIf(self, subroute):
        """
        Compile the if statement
        """
        # if
        self.tokenizer.advance() 
        self.tokenizer.advance() 
        
        self.compileExpression(subroute)

        self.tokenizer.advance() 
        self.tokenizer.advance() 

        startLabel = CompilationEngine.getLabel()
        endLabel = CompilationEngine.getLabel()

        self.vm.writeIf(startLabel)

        # Compile inner statements
        self.compileStatements(subroute)

        self.vm.writeGoto(endLabel)
        self.vm.writeLabel(startLabel)

        self.tokenizer.advance() 

        token = self.tokenizer.getCurrent()
        if token == ("keyword", "else"):
            self.tokenizer.advance()
            self.tokenizer.advance()

            # Compile inner statements
            self.compileStatements(subroute)

            self.tokenizer.advance() 

        self.vm.writeLabel(endLabel)

    def compileWhile(self, subroute):
        """
        Compile the while statment
        """
        # while
        self.tokenizer.advance() 
        self.tokenizer.advance() 

        while_label = CompilationEngine.getLabel()
        startLabel = CompilationEngine.getLabel()

        self.vm.writeLabel(while_label)        
        self.compileExpression(subroute)

        self.tokenizer.advance() 
        self.tokenizer.advance() 

        self.vm.writeIf(startLabel)

        # Compile inner statements
        self.compileStatements(subroute)
        
        self.vm.writeGoto(while_label)
        self.vm.writeLabel(startLabel)
        self.tokenizer.advance() 

    def compileLet(self, subroute):
        """Compile the let statment"""

        self.tokenizer.advance() # let
        varName = self.tokenizer.advance().value # var name
        jackSymbol = subroute.getSymbol(varName)

        is_array = self.tokenizer.getCurrent().value == "["
        if is_array:
            self.tokenizer.advance() # [
            self.compileExpression(subroute) # Index
            self.tokenizer.advance() # ]
            self.tokenizer.advance() # =
            # Add the base and index
            self.vm.writePushSymbol(jackSymbol)
            self.vm.write("add")
            # Base "that" at base+index, stored in stack
            # to avoid the expression assigned changing pointer:1, we don"t
            # pop it yet
            self.compileExpression(subroute) # Expression to assign
            self.vm.writePop("temp", 0) # Store assigned value in temp
            self.vm.writePop("pointer", 1) # Restore destination
            self.vm.writePush("temp", 0) # Restore assigned value
            self.vm.writePop("that", 0) # Store in target
        else:
            self.tokenizer.advance() # =
            self.compileExpression(subroute) # Expression to assign
            self.vm.writePopSymbol(jackSymbol)

        self.tokenizer.advance() # ;

    def compileDo(self, subroute):
        """Compile the do statment"""
        self.tokenizer.advance() # do

        self.compileTerm(subroute) # Do options are a subset of terms
        self.vm.writePop("temp", 0) # Pop to avoid filling the stack with garbage

        self.tokenizer.advance() # ;

    def compileReturn(self, subroute):
        """Compile the return statment"""
        self.tokenizer.advance() # return

        # Check if an expression is given
        token = self.tokenizer.getCurrent()
        if token != ("symbol", ";"):
            self.compileExpression(subroute)
        else:
            self.vm.writeInt(0)

        self.vm.writeReturn()
        self.tokenizer.advance() # ;

    def compileExpressionList(self, subroute):
        """Compile a subroutine call expression list"""
        # Handle expression list, so long as there are expressions
        count = 0 # Count expressions
        token = self.tokenizer.getCurrent()
        while token != ("symbol", ")"):

            if token == ("symbol", ","):
                self.tokenizer.advance()

            count += 1
            self.compileExpression(subroute)
            token = self.tokenizer.getCurrent()

        return count

    def compileExpression(self, subroute):
        """
        Compile an expression.
        """
        self.compileTerm(subroute)
        
        token = self.tokenizer.getCurrent()
        while token.value in "+-*/&|<>=":
            binaryOp = self.tokenizer.advance().value
            
            self.compileTerm(subroute)
            self.vm.write(operations[binaryOp])

            token = self.tokenizer.getCurrent()

    def compileTerm(self, subroute):
        """Compile a term as part of an expression"""

        token = self.tokenizer.advance()
        # In case of unary operator, compile the term after the operator
        if token.value in ["-", "~"]:
            self.compileTerm(subroute)
            if token.value == "-":
                self.vm.write("neg")
            elif token.value == "~":
                self.vm.write("not")
        # In case of opening parenthesis for an expression
        elif token.value == "(":
            self.compileExpression(subroute)
            self.tokenizer.advance() 
        elif token.type == "integerConstant":
            self.vm.writeInt(token.value)
        elif token.type == "stringConstant":
            self.vm.writeString(token.value)
        elif token.type == "keyword":
            if token.value == "this":
                self.vm.writePush("pointer", 0)
            else:
                self.vm.writeInt(0) # null / false
                if token.value == "true":
                    self.vm.write("not")

        # In case of a function call or variable name
        elif token.type == "identifier":
            # Save token value as symbol and function in case of both
            tokenValue = token.value
            tokenVar = subroute.getSymbol(tokenValue)

            token = self.tokenizer.getCurrent()
            if token.value == "[": # Array
                self.tokenizer.advance() # [
                self.compileExpression(subroute)
                self.vm.writePushSymbol(tokenVar)
                self.vm.write("add")
                # rebase "that" to point to var+index
                self.vm.writePop("pointer", 1)
                self.vm.writePush("that", 0)
                self.tokenizer.advance() # ]
            else:
                # Default class for function calls is this class
                name = tokenValue
                func_class = subroute.jackClass.name
                # Used to mark whether to use the default call, a method one
                default_call = True
                arg_count = 0

                if token.value == ".":
                    default_call = False
                    self.tokenizer.advance() # .
                    # try to load the object of the method
                    obj = subroute.getSymbol(tokenValue)
                    name = self.tokenizer.advance().value # function name
                    # If this is an object, call as method
                    if obj:
                        func_class = tokenVar.type # Use the class of the object
                        arg_count = 1 # Add "this" to args
                        self.vm.writePushSymbol(tokenVar) # push "this"
                    else:
                        func_class = tokenValue
                    token = self.tokenizer.getCurrent()

                # If a function call
                if token.value == "(":
                    if default_call:
                        # Default call is a method one, push this
                        arg_count = 1
                        self.vm.writePush("pointer", 0)

                    self.tokenizer.advance() 
                    arg_count += self.compileExpressionList(subroute)
                    self.vm.writeCall(func_class, name, arg_count)
                    self.tokenizer.advance() 
                # If a variable instead
                elif tokenVar:
                    self.vm.writePushSymbol(tokenVar)