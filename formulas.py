
from operators import *

class Formula(object):
	operator = None
	arguments = []

	def __init__(self,operator,arguments=[]):
		self.operator = operator
		self.arguments = arguments

	def __eq__(self,other):
		return type(self) == type(other) and self.operator == other.operator and self.arguments == other.arguments

	def is_variable(self):
		return self.get_operator() == None

	def is_quantifed(self):
		quantifier_list = ["\exists","\\forall"]
		if not type(self.get_operator()) == tuple:
			return False

		return self.get_operator()[0] in quantifier_list

	def get_operator(self):
		return self.operator

	def get_arguments(self):
		return self.arguments

	def __repr__(self):
		if type(self) is Predicate or type(self) is Proposition:
			return str(self)

		if self.get_operator().is_quantifier():
			return str(self.get_operator())+ "(" + str(self.arguments[0]) + ")"

		if self.get_operator().get_arity() == 2:
			return "(" + str(self.arguments[0]) + str(self.get_operator()) + str(self.arguments[1]) + ")"

		if self.get_operator().get_arity() == 1:
			return str(self.operator) + str(self.arguments[0])

	def get_latex(self):
		# returns compiled LaTeX string for the formula
		if type(self) is Predicate or type(self) is Proposition:
			return str(self)

		if self.get_operator().is_quantifier():
			return self.get_operator().get_latex() + " (" + self.arguments[0].get_latex() + ")"

		if self.get_operator().get_arity() == 2:
			return "(" + self.arguments[0].get_latex() + " " + self.get_operator().get_latex() + " " + self.arguments[1].get_latex() + ")"

		if self.get_operator().get_arity() == 1:
			return self.operator.get_latex() + " " + self.arguments[0].get_latex()


	def get_variables(self):
		# returns a list of all propositonal variables
		return [var for var in self.subformulas() if type(var)==Proposition]

	def subformulas(self):
		# returns a list of all subformulas
		if not self.operator:
			return [self]
		return sum([F.subformulas() for F in self.get_arguments()],[self])

	def modal_depth(self):
		# returns the modal depth of the formula
		if not self.get_operator():
			return 0
		if self.get_operator().is_modal():
			return 1 + max([F.modal_depth() for F in self.get_arguments()]+[0])
		return max([F.modal_depth() for F in self.get_arguments()]+[0])

	def parity(self,var):
		# returns the parity of the formula
		# +1 = positive, -1 = negative
		# (NOT YET FUNCTIONAL)
		if not self.get_operator():
			if self == var:
				return 1
			else:
				return 2

		if type(self.get_operator()) == OP_NOT:
			return -1 * self.get_arguments()[0].parity(var)

		if type(self.get_operator()) == OP_AND:
			return min([sub.parity(var) for sub in self.get_arguments()])

		if type(self.get_operator()) == OP_OR:
			return min([sub.parity(var) for sub in self.get_arguments()])

		if type(self.get_operator()) == OP_IMPLIES:
			return min(-1*self.get_arguments()[0].parity(var),self.get_arguments()[1].parity(var))
		return self.get_arguments()[0].parity(var)



class Predicate(Formula):
	def __init__(self,symbol,arguments=["x"]):
		self.symbol = symbol
		self.arguments = arguments

	def __repr__(self):
		return self.symbol + "(" + ','.join(self.get_arguments()) + ")"

	def __eq__(self,other):
		return type(self) == type(other) and self.symbol == other.symbol

	def substitute(self,old,new):
		# replaces all instances of old with new
		args = self.arguments
		for i in range(len(args)):
			if args[i] is old:
				args[i] = new
		self.arguments = args


class Proposition(Predicate):
	arity = 0

	def __init__(self,symbol):
		self.symbol = symbol

	def __repr__(self):
		return self.symbol

	def __eq__(self,other):
		return type(self) == type(other) and self.symbol == other.symbol


def AND(left,right):
	# constructor for conjunction
	return Formula(OP_AND(),[left,right])

def OR(left,right):
	# constructor for disjunction
	return Formula(OP_OR(),[left,right])

def IMPLIES(left,right):
	# constructor for imlication
	return Formula(OP_IMPLIES(),[left,right])

def NOT(sub):
	# constructor for conjunction
	return Formula(OP_NOT(),[sub])

def BOX(sub):
	# constructor for conjunction
	return Formula(OP_BOX(),[sub])

def DIAMOND(sub):
	# constructor for conjunction
	return Formula(OP_DIAMOND(),[sub])

def EXISTS(var,sub):
	# constructor for existential quantifier
	return Formula(OP_EXISTS(var),[sub])

def FORALL(var,sub):
	# constructor for universal quantifier
	return Formula(OP_FORALL(var),[sub])


if __name__ == "__main__":
	p = Proposition("p")
	q = Predicate("Q")
	r = Proposition("r")
	s = Proposition("s")

	Q = DIAMOND(q)
	F = OR(p,FORALL('y',Q))
	G = IMPLIES(F,r)
	H = BOX(DIAMOND(G))

	print F
	print H

	print H.get_latex()

	print len(H.subformulas()), H.modal_depth()


	print ""
	#print standard_translation(H)