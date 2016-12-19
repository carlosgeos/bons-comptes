def communitiesIdentification(g):
	"""
		Returns all communities in a graph g
	"""
	node_list = g.getNodeList()
	size = g.getSize()
	identifier = [-1]*size
	succ = [0]*size																# nb of debts that each person has
	cid = 0

	for i in range(size):														# Get the number of debts of each person into succ
		node = node_list[i].getNext()											# First debt node of a person
		while node:
			succ[i] += 1
			node = node.getNext()

	while max(succ) != -1:
		cid += 1
		ind = succ.index(max(succ))
		explore(node_list, identifier, succ, cid, ind)

	res = []																	# Getting result into lists
	for i in range(1, cid+1):
		tmp = []
		for j in range(len(identifier)):
			if i == identifier[j]:
				tmp.append(node_list[j].getName())
		if tmp != []:
			res.append(tmp)
	return res



def explore(node_list, identifier, succ, cid, k):

	if succ[k] != -1:															# If not visited yet
		succ[k] = -1															# mark as visited
		identifier[k] = cid														# update id
		des = node_list[k].getNext()
		while des:																# Recursive call for all the "descendants"
			explore(node_list, identifier, succ, cid, node_list.index(des.getCreditor()))
			des = des.getNext()

	elif succ[k] == -1 and identifier[k] != cid:								# Node already visited but id needs to be updated
		oldID = identifier[k]
		for m in range(len(identifier)):
			if identifier[m] == oldID:
				identifier[m] = cid

	# else: if node was already visited and there's no need to update id