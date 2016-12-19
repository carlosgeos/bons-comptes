from collections import defaultdict
from copy import deepcopy

from tarjan import Tarjan

class Simplifier:
    def __init__(self, graph):
        self.graph = graph
        self._graph = deepcopy(graph) # Keep a clean copy for our 3rd step (minim())
        self.cycles = set()
        self.blocked = defaultdict(bool) # blocked paths (it optimises the algorithm)
        self.b_map = defaultdict(list) # "if X is unblocked, then unblock Y"
        self.stack = []

    def find_cycles(self, current, start):
        found_cycle = False

        # Add current to stack and block it
        self.stack.append(current)
        self.blocked[current] = True

        # start DFS with node's neighbours
        next_node = current.getNext()
        while next_node is not None:
            # case 1: next node is the start node so we found a cycle
            if next_node.getCreditor() == start:
                self.cycles.add(tuple(self.stack))
                found_cycle = True
            # case 2:
            elif not self.blocked[next_node.getCreditor()]:
                if self.find_cycles(next_node.getCreditor(), start):
                    found_cycle = True
            # done with this node
            next_node = next_node.getNext()

        # If current is part of a found cycle, unblock it, so we can
        # find more through that node.
        if found_cycle:
            self.unblock(current)
        else: # Otherwise add relation to blocked map: neighbour -> me
            next_node = current.getNext()
            while next_node is not None:
                if current not in self.b_map[next_node.getCreditor()]:
                    self.b_map[next_node.getCreditor()].append(current)
                next_node = next_node.getNext()

        # Finish by removing 'current' from stack since we're done.
        self.stack.remove(current)
        return found_cycle

    def unblock(self, node):
        """Unblocks the path recursively, checking the blocked map.

        """

        self.blocked[node] = False
        Bnode = self.b_map[node]
        while Bnode:
            next_node = Bnode.pop(0)
            if self.blocked[next_node]:
                self.unblock(next_node)

    def get_elementary_cycles(self):
        """Returns all elementary cycles in a graph

        """
        tarjan = Tarjan(self.graph)
        for ssc in tarjan.ssc():
            for start_node in ssc:
                least_node = min(ssc)     # Some kind of ordering
                self.find_cycles(least_node, least_node)
                # ssc changes at each iteration, since we remove the
                # least node to avoid unnecesary DFSs
                ssc = tarjan.remove_useless_edges(ssc, least_node)
        return self.cycles

    def minim(self):
        """handles the simplification process

        Not optimal, but gives a good result.

        """
        cycles = self.get_elementary_cycles()

        for cycle in cycles:
            # take back our clean graph (self._graph) and operate on it
            nodes_concerned = []
            for node in self._graph.node_list:
                possible_names = [check_node.getName() for check_node in cycle]
                if node.getName() in possible_names:
                    nodes_concerned.append(node)
            possible_debts = []

            # inspect what the minimum debt is
            for node in nodes_concerned:
                next_node = node.getNext()
                while next_node is not None:
                    if next_node.getCreditor() in nodes_concerned:
                        if int(next_node.getAmount()) != 0:
                            possible_debts.append(int(next_node.getAmount()))
                            break   # Only once
                    next_node = next_node.getNext()

            # subtract that debt from all the debts in the cycle
            least_debt = min(possible_debts)
            for node in nodes_concerned:
                next_node = node.getNext()
                while next_node is not None:
                    if next_node.getCreditor() in nodes_concerned:
                        if int(next_node.getAmount()) != 0:
                            next_node.setAmount(str(int(next_node.getAmount()) - int(least_debt)))
                            break   # Only once
                    next_node = next_node.getNext()
        return self._graph
