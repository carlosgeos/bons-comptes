from person import *
from debt import *

class Graph:
	def __init__(self, f):
		"""
			Creates a graph based on the file received
		"""
		self.node_list = []
		self.size = int(f.readline())											# Not needed
	
		for line in f:
			line = line.split()
			p1_name, p2_name, debt = line[0], line[1], line[2]
			if not any(node.name == p1_name for node in self.node_list):
				p1 = Person(p1_name)
				self.node_list.append(p1)
			else:
				p1 = next((node for node in self.node_list if node.getName() == p1_name), None)
				while p1.getNext() != None:
					p1 = p1.getNext()
			if not any(node.name == p2_name for node in self.node_list):
				p2 = Person(p2_name)
				self.node_list.append(p2)
			else:
				p2 = next((node for node in self.node_list if node.getName() == p2_name), None)
			p1.setNext(Debt(p2, debt))											# set new debt
		
	def __str__(self):
		string = "Graph - adjacency list\n"
		string += "\nKey:\n"
		string += "Person --> | amount owed | to whom | --> | amount owed | to whom | ...\n\n"
		for person in self.node_list:
			string += str(person)
		return string
		
	def getNodeList(self):
		return self.node_list
		
	def getSize(self):
		return self.size
		
		
	def makeUnordered(self):
		newGraph = []
		for person in self.node_list:
			newGraph.append(Person(person.getName()))

		for i in range(len(self.node_list)):
			debt = self.node_list[i].getNext()
			while debt:

				found = False
				cpt = 0
				while not found:
					if newGraph[cpt].getName() == debt.getCreditor().getName():
						found = True
					else:
						cpt += 1

				tmp = Debt(newGraph[cpt], debt.getAmount())
				tmp.setNext(newGraph[i].getNext())
				newGraph[i].setNext(tmp)

				tmp = Debt(newGraph[i], debt.getAmount())
				tmp.setNext(newGraph[cpt].getNext())
				newGraph[cpt].setNext(tmp)

				debt = debt.getNext()

		return newGraph

	