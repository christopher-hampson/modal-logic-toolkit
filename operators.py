class Operator(object):
	modal = False
	quantifier = False

	def __init__(self,symbol,arity,latex_symbol):
		self.symbol = str(symbol)
		self.arity = int(arity)
		self.latex = str(latex_symbol)

	def is_modal(self):
		return self.is_box() or self.is_diamond()

	def is_negation(self):
		return type(self) == OP_NOT

	def is_conjunction(self):
		return type(self) == OP_AND

	def is_disjunction(self):
		return type(self) == OP_OR

	def is_implication(self):
		return type(self) == OP_IMPLIES

	def is_box(self):
		return type(self) == OP_BOX

	def is_diamond(self):
		return type(self) == OP_DIAMOND

	def is_quantifier(self):
		return self.quantifier

	def get_arity(self):
		return self.arity

	def __repr__(self):
		return self.symbol

	def get_latex(self):
		return self.latex

class OP_AND(Operator):
	def __init__(self):
		self.symbol = '^'
		self.arity = 2
		self.latex = '\land'

class OP_OR(Operator):
	def __init__(self):
		self.symbol = 'v'
		self.arity = 2
		self.latex = '\lor'

class OP_IMPLIES(Operator):
	def __init__(self):
		self.symbol = '->'
		self.arity = 2
		self.latex = '\\to'

class OP_NOT(Operator):
	def __init__(self):
		self.symbol = '-'
		self.arity = 1
		self.latex = '\\neg'

class OP_BOX(Operator):
	def __init__(self):
		self.symbol = '[]'
		self.arity = 1
		self.latex = '\B'
		self.modal = True

class OP_DIAMOND(Operator):
	def __init__(self):
		self.symbol = '<>'
		self.arity = 1
		self.latex = '\D'
		self.modal = True

class Quantifier(Operator):
	quantifier = True
	def __init__(self,symbol,arity,latex_symbol,variable):
		self.symbol = str(symbol)
		self.arity = int(arity)
		self.latex = str(latex_symbol)
		self.variable = str(variable)

	def __repr__(self):
		return self.symbol + "{" + self.variable + "}"

	def get_latex(self):
		return self.latex + "{" + self.variable + "}"

class OP_EXISTS(Quantifier):
	def __init__(self,variable):
		self.symbol = 'E'
		self.arity = 1
		self.variable = variable 
		self.latex = '\exists'

class OP_FORALL(Quantifier):
	def __init__(self,variable):
		self.symbol = 'A'
		self.arity = 1
		self.variable = variable 
		self.latex = '\\forall'
