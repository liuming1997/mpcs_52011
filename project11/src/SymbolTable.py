from collections import namedtuple

JackSymbol = namedtuple("Symbol", ["kind", "type", "id"])

class JackClass:
	"""A Jack class representation for the Jack compiler"""

	def __init__(self, name):
		self.name = name
		self.symbols = dict()

		self.staticSymbols = 0
		self.fieldSymbols = 0

	def addField(self, name, varType):
		# add a field variable
		self.symbols[name] = JackSymbol("field", varType, self.fieldSymbols)
		self.fieldSymbols += 1

	def addStatic(self, name, varType):
		# add a static variable
		self.symbols[name] = JackSymbol("static", varType, self.staticSymbols)
		self.staticSymbols += 1

	def getSymbol(self, name):
		"""Get a symbol from the class"""
		return self.symbols.get(name)

class JackSubroutine:
	"""
    Instantiate a subroutine for a Jack class.
    """

	def __init__(self, name, subroutineType, returnType, jackClass):
		self.name = name
		self.jackClass = jackClass
		self.subroutineType = subroutineType
		self.returnType = returnType

		self.symbols = dict()
		self.argSymbols = 0
		self.varSymbols = 0

		if subroutineType == "method":
			self.addArg("this", self.jackClass.name)

	def addArg(self, name, varType):
        # add argument
		self.symbols[name] = JackSymbol("arg", varType, self.argSymbols)
		self.argSymbols += 1

	def addVar(self, name, varType):
        # add variable
		self.symbols[name] = JackSymbol("var", varType, self.varSymbols)
		self.varSymbols += 1

	def getSymbol(self, name):
		"""
        Get a symbol from within the subroutine
        """
		symbol = self.symbols.get(name)
		if symbol is not None:
			return symbol

		return self.jackClass.getSymbol(name)