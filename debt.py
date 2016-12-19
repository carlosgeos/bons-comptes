class Debt:
	def __init__(self, creditor, amount):
		self.creditor = creditor
		self.amount = amount
		self.next = None

	def setAmount(self, newValue):
		self.amount = newValue

	def setNext(self, node):
		self.next = node

	def getCreditor(self):
		return self.creditor

	def getAmount(self):
		return self.amount

	def getNext(self):
		return self.next
