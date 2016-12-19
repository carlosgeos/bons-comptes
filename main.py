import argparse
from graph import *
from community import communitiesIdentification
from hub import hubsIdentification
from simplifier import Simplifier


def main():
    parser = argparse.ArgumentParser(description='Process a list of friends and their debts')
    parser.add_argument('graph', metavar='graph_file', type=argparse.FileType('r'),
                        help='an input file - the graph representation')

    args = parser.parse_args()
    graph = Graph(args.graph)
    print("Initial graph")
    print(graph)

    print("Communities Identification\n", communitiesIdentification(graph))

    print("\nHubs Identification (K=1)\n", hubsIdentification(graph, 1))
    print("\nHubs Identification (K=3)\n", hubsIdentification(graph, 3))
    print("\nHubs Identification (K=5)\n", hubsIdentification(graph, 5))

    cs = Simplifier(graph)
    simplified_graph = cs.minim()

    print(simplified_graph)


if __name__ == '__main__':
    main()
