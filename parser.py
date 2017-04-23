import re
from formulas import *
from CNF import *

class Parser:

	def __init__(self,src):
		self.src = src
		self.pos = 0

	def parse_ws(self,min_ws=0):
		# parse whitespace
		r_match = re.match("[\s]*", self.src[self.pos:])
		if r_match:
			if len(r_match.group(0))>=min_ws:
				self.pos += len(r_match.group(0))
			else:
				SyntaxError("Expecting at least {0} whitespace. Got only {1}".format(min_ws,len(r_match.group(0))))
		else:
			SyntaxError("Expecting whitespace. Got {0}'".format(self.src[self.pos:self.pos+15]) + "' instead.")


	def parse_regex(self,regex):
		# parses a given regex
		r_match = re.match(regex, self.src[self.pos:])		# find longest match of regex
		if r_match:
			self.pos += len(r_match.group(0))		# move position to end of match
			return r_match.group(0)					# return match
		else:
			raise SyntaxError("Expecting pattern {0}. Got {1} '".format(regex, self.src[self.pos:self.pos+15]) + "' instead.")

	
	def parse(self):
		# Main parse method

		F = self.parse_formula()
		if self.pos == len(self.src):
			return F
		else:
			# catches syntactically valid proper initial substrings
			raise SyntaxError("Mismatched brackets.")


	def parse_proposition(self):
		# PROPOSITION is a token
		prop = self.parse_regex("[a-z][0-9]*")
		return Proposition(prop)
		
	def parse_and(self):
		# AND :: PROP '^'' AND | PROP '^'' PROP 
		symbol = r"\^"

		self.parse_ws()
		left = self.parse_sub()
		self.parse_ws()
		self.parse_regex(symbol)
		self.parse_ws()

		p = self.pos
		try:
			right = self.parse_and()
		except: 
			self.pos = p
			right = self.parse_sub()

		return AND(left,right)

	def parse_or(self):
		# OR :: SUB 'v' OR | SUB 'v' SUB
		symbol = "v"

		self.parse_ws()
		left = self.parse_sub()
		self.parse_ws()
		self.parse_regex(symbol)
		self.parse_ws()

		p = self.pos
		try:
			right = self.parse_or()
		except: 
			self.pos = p
			right = self.parse_sub()

		return OR(left, right)


	def parse_implies(self):
		# IMPLIES :: SUBFORMULA '->' SUBFORMULA
		symbol = '->'
		self.parse_ws()
		left = self.parse_sub()
		self.parse_ws()
		self.parse_regex(symbol)
		self.parse_ws()
		right = self.parse_sub()
		self.parse_ws()
		return IMPLIES(left,right)

	def parse_sub(self):
		# SUBFORMULA :: BRACKET | UNARY | PROPOSITION
		p = self.pos

		try:
			self.parse_ws()
			sub = self.parse_bracket()
			#self.parse_ws()
			return sub
		except: self.pos = p

		try:
			self.parse_ws()
			sub = self.parse_unary()
			#self.parse_ws()
			return sub
		except: self.pos = p

		try:
			self.parse_ws()
			sub = self.parse_proposition()
			#self.parse_ws()
			return sub
		except: self.pos = p

		raise SyntaxError("Something went wrong!")


	def parse_not(self):
		# NOT :: '-' SUBFORMULA
		self.parse_ws()
		self.parse_regex("-")
		self.parse_ws()
		sub = self.parse_sub()
		return NOT(sub)

	def parse_box(self):
		# BOX :: '[]' SUBFORMULA
		self.parse_ws()
		self.parse_regex("\[\]")
		self.parse_ws()
		sub = self.parse_sub()

		return BOX(sub)

	def parse_diamond(self):
		# DIAMOND :: '<>' SUBFORMULA
		self.parse_ws()
		self.parse_regex("\<\>")
		self.parse_ws()
		sub = self.parse_sub()

		return DIAMOND(sub)

	def parse_unary(self):
		# UNARY :: NOT | BOX | DIAMOND
		p = self.pos

		try:
			self.parse_ws()
			sub = self.parse_not()
			#self.parse_ws()
			return sub
		except: self.pos = p

		try:
			self.parse_ws()
			sub = self.parse_box()
			#self.parse_ws()
			return sub
		except: self.pos = p

		try:
			self.parse_ws()
			sub = self.parse_diamond()
			#self.parse_ws()
			return sub
		except: self.pos = p

		raise SyntaxError("Something went wrong!")


	def parse_binary(self):
		# BINARY :: AND | OR | IMPLIES
		p = self.pos

		try:
			self.parse_ws()
			sub = self.parse_and()
			#self.parse_ws()
			return sub
		except: self.pos = p

		try:
			self.parse_ws()
			sub = self.parse_or()
			#self.parse_ws()
			return sub
		except: self.pos = p

		try:
			self.parse_ws()
			sub = self.parse_implies()
			#self.parse_ws()
			return sub
		except: raise SyntaxError("Something went wrong!")


	def parse_bracket(self):
		# BRACKET :: ( FORMULA )
		self.parse_ws()
		self.parse_regex("\(")
		self.parse_ws()
		sub = self.parse_formula()
		self.parse_ws()
		self.parse_regex("\)")
		self.parse_ws()
		return sub



	def parse_formula(self):
		# FORMULA :: BINARY | UNARY | BRACKETR | PROP

		p = self.pos
		try:
			self.parse_ws()
			sub = self.parse_binary()
			#self.parse_ws()
			return sub
		except: self.pos = p

		try:
			self.parse_ws()
			sub = self.parse_unary()
			#self.parse_ws()
			return sub
		except: self.pos = p

		try:
			self.parse_ws()
			sub = self.parse_bracket()
			#self.parse_ws()
			return sub
		except: self.pos = p
		
		
		prop = self.parse_proposition()
		return prop
	




if __name__ == "__main__":
		
	src = "[](p -> q) -> ([]p -> []q)"
	src = "-<>(-(p v []q v -r) -> (q ^ []r ^ -q))"

	print src

	P = Parser(src)

	F = P.parse()

	print F.get_latex()
	print len(F.subformulas())
	print F.modal_depth()
	p = F.get_variables()[3]
	print NNF(F)

	#print P.parse_binary(brackets=False)
	#print P.parse_formula()