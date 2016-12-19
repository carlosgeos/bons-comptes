class Person:

    def __init__(self, name):
        self.name = name
        self.next = None

    def setNext(self, node):
        self.next = node

    def getName(self):
        return self.name

    def getNext(self):
        return self.next

    def __str__(self):
        res = ""
        res += self.getName()

        if self.getNext() != None:                                                # If person has any dept
            debt = self.getNext()

            while debt != None:
                res += " --> | " + debt.getAmount() + " | " + debt.getCreditor().getName() + " |"
                debt = debt.getNext()
        res += "\n"
        return res

    def __lt__(self, other):
        """Some ordering for nodes. Based on their letter. A < B and B < C.
        """
        return self.name < other.getName()
