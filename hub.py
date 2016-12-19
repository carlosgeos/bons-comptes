
def hubsIdentification(g, k):
	"""
		Returns the hubs that without them we get the
		creation of 2 communities of at least k people.
	"""
	unordered = g.makeUnordered()
	sol = [None]*g.getSize()
	res = []

	for i in range(g.getSize()):
		explore(unordered, sol, [0]*g.getSize(), 0, i)							# Search for all articulation points

	for j in range(g.getSize()):
		if sol[j] != None and sol[j]>=k:										# If articulation point and both communities bigger than k
			res.append(unordered[j].getName())
	return res


def explore(g, sol, val, cid, i):
	cid += 1
	val[i] = cid
	low = cid

	adj = g[i].getNext()
	while adj:
		if val[g.index(adj.getCreditor())] == 0:								# If not visited yet
			m = explore(g, sol, val, cid, g.index(adj.getCreditor()))
			if m < low:
				low = m
			if m >= val[i] and val[i]!= 1 and sol[i]==None:						# If found
				sol[i] = low													# Store size of the smallest community created
				if low > max(val)-low:
					sol[i]=max(val)-low
		else:
			if val[g.index(adj.getCreditor())] < low:
				low = val[g.index(adj.getCreditor())]
		adj = adj.getNext()
	return low