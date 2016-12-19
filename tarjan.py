class Tarjan:
    MAX_SIZE_GRAPH = 10000
    def __init__(self, graph):
        self.graph = graph.node_list
        self.temp_cycle = []
        self.cycles = []

    def tarjan_main(self):
        self.iden = 0; self.sid = 0;
        self.pre = [-1 for node in self.graph]
        self.low = [0 for node in self.graph]
        self.comp = [0 for node in self.graph]

        self.stack = []

        for node in self.graph:
            k = self.graph.index(node)
            if self.pre[k] == -1:
                self.tarjan_explore(k)

    def tarjan_explore(self, k):
        t = 0; minim = 0;
        self.iden += 1

        self.pre[k] = self.iden
        self.low[k] = self.iden
        minim = self.iden

        self.stack.append(k)
        next_node = self.graph[k].getNext()
        while next_node is not None:
            t = self.graph.index(next_node.getCreditor())
            if self.pre[t] == -1: self.tarjan_explore(t)
            if self.low[t] < minim: minim = self.low[t]
            next_node = next_node.getNext()

        if minim < self.low[k]:
            self.low[k] = minim
        else:
            while True:
                t = self.stack.pop()
                self.comp[t] = self.sid
                self.low[t] = Tarjan.MAX_SIZE_GRAPH
                if t == k:
                    break;
            self.sid += 1

    def remove_useless_edges(self, some_ssc, remove_node=None):
        """very useful: DFS is optimised by not having to inspect nodes for
        which we already found all its cycles (through johnson's
        algorithm)

        """
        if remove_node is not None:
            some_ssc.remove(remove_node) #
        for node in some_ssc:
            current = node
            while current is not None:
                next_debt = current.getNext()
                if next_debt is not None and next_debt.getCreditor() not in some_ssc:
                    # our edge goes to a node not in our ssc -> jump over it
                    current.setNext(next_debt.getNext())
                else:
                    current = current.getNext()

        return some_ssc


    def ssc(self):
        """Gets all the strongly connected components with more than one node
            in them.  It checks the vector self.comp to guess which
            nodes are strongly connected.

        """
        self.tarjan_main()
        sscomps = []
        mapper = {}
        for i in range(0, len(self.comp)):
            if self.comp[i] not in mapper:
                sscomps.append([self.graph[i]])
                mapper[self.comp[i]] = len(sscomps) - 1 # save where last item appended is
            else:
                sscomps[mapper[self.comp[i]]].append(self.graph[i])
        # clean our list to remove single nodes
        clean_sscomps = [ssc for ssc in sscomps if len(ssc) > 1]

        # clean edges from this graph
        for some_ssc in clean_sscomps:
            some_ssc = self.remove_useless_edges(some_ssc)

        return clean_sscomps
