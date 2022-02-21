descriptor = {"static": "static",
              "field": "this",
              "arg": "argument",
              "var": "local"}

class VMWriter:
    """
    Jack to VM writer
    """
    def __init__(self, stream):
        # init
        self.stream = stream
        self.labelCount = 0
        self.text = ""
        print(self.stream)

    def writeIf(self, label):
        """
        Write an if-goto used to jump to label if the condition does not hold
        """
        # Negate to jump if the conditions doesn't hold
        self.stream.write("not\n")
        self.stream.write("if-goto {}\n".format(label))

    def writeGoto(self, label):
        """
        Write a goto for the VM
        """
        self.stream.write("goto {}\n".format(label))
        self.text += "goto {}\n".format(label)

    def writeLabel(self, label):
        """
        Write a label in VM
        """
        self.stream.write("label {}\n".format(label))

    def writeFunction(self, subroutine):
        """
        Write a function header for a Jack subroutine
        """
        className = subroutine.jackClass.name
        name = subroutine.name
        localVars = subroutine.varSymbols
        # it was meant to go somewhere
        subroutineType = subroutine.subroutineType

        self.stream.write("function {}.{} {}\n".format(className, name, localVars))

    def writeReturn(self):
        """
        Write the return statement.
        """
        self.stream.write("return\n")

    def writeCall(self, className, func, args):
        """ 
        Write a call to a function with n args
        """
        self.stream.write("call {0}.{1} {2}\n".format(className, func, args))

    def writePopSymbol(self, symbol):
        """
        Pop the value in the top of the stack to the symbol
        """
        kind = symbol.kind
        # the offset in the segment
        offset = symbol.id 
        segment = descriptor[kind]
        self.writePop(segment, offset)

    def writePushSymbol(self, symbol):
        """Push the value from the symbol to the stack"""
        kind = symbol.kind
        # the offset in the segment
        offset = symbol.id 
        segment = descriptor[kind]
        self.writePush(segment, offset)

    def writePop(self, segment, offset):
        """
        Pop the value in the top of the stack to segment and offset
        """
        self.stream.write("pop " + str(segment) + " " + str(offset))

    def writePush(self, segment, offset):
        """
        Push the value to the stack from segment and offset
        """
        self.stream.write("push {0} {1}\n".format(segment, offset))

    def write(self, action):
        """
        Write something
        """
        self.stream.write('{}\n'.format(action))

    def writeInt(self, n):
        """
        Write an int
        """
        self.writePush("constant", n)

    def writeString(self, s):
        """
        Allocates a new string, and appends all the chars one-by-one
        """
        s = s[1:-1]
        self.writeInt(len(s))
        self.writeCall("String", "new", 1)
        for c in s:
            self.writeInt(ord(c))
            self.writeCall("String","appendChar", 2)
    
    def ret(self):
        return self.text