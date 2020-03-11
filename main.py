from tools import Graph, Node
import argparse
import sys
sys.setrecursionlimit(5000)

def main(input_file, output_file):

    # player 0: circular - even
    # player 1: rectangular - odd

    # creating the graph from this webpage: https://en.wikipedia.org/wiki/Parity_game

    even_nodes = []
    odd_nodes = []
    G = Graph()
    higher = -1
    number = None
    with open(input_file) as reader:
        data = reader.read().splitlines(True)
        number = data[0].split()
        number = number[1]
        number = number.replace(";", "")
        data = data[1:]
        for line in data:
            uuid, p, owner, edges, name = line.split()

            uuid = int(uuid)
            p = int(p)
            owner = int(owner)
            name = name.replace("\"", "")
            name = name.replace(";", "")
            node = Node(p, owner, uuid, name)

            edges = edges.split(',')
            G.insert_node(node)

            for edge in edges:
                edge = int(edge)
                G.insert_edge(uuid, edge)

            if owner % 2 == 0:
                even_nodes.append(uuid)
            else:
                odd_nodes.append(uuid)

            if p > higher:
                higher = p


    if higher % 2 == 1:
        higher = higher + 1

    WE = solveE(G, even_nodes, odd_nodes, higher)

    nodes = G.get_nodes()
    for node in WE:
        node.set_winner(0) # 0 means even player

    for node in nodes:
        if node.get_winner() == -1:
            node.set_winner(1) # 1 means odd player

    with open(output_file, 'w') as writter:

        writter.write("parity " + number + ";\n")
        for node in nodes:
            writter.write(str(node.get_uuid()) + " " + str(node.get_winner()) + "\n")


def atr(G, player_nodes, U, num):

    all_nodes = G.get_nodes()
    not_changed = False

    atr_nodes = [node.get_uuid() for node in U]

    while not not_changed:
        changed = False
        for node in all_nodes:
            successors = G.get_edges(node.get_uuid())
            if node.get_uuid() in player_nodes:
                for succ in successors:
                    if succ in atr_nodes:
                        if node.get_uuid() not in atr_nodes:
                            changed = True
                            atr_nodes.append(node.get_uuid())
                            break

            else:
                all_of_them = True

                for succ in successors:
                    if succ not in atr_nodes:
                        all_of_them = False
                        break

                if all_of_them:

                    if node.get_uuid() not in atr_nodes:
                        changed = True
                        atr_nodes.append(node.get_uuid())

        not_changed = not(changed)

    return atr_nodes


def solveE(G, even_nodes, odd_nodes, h):

    all_nodes = G.get_nodes()
    if len(all_nodes) == 0 or h < 0:
        return []

    while True:
        Nh = [node for node in G.get_nodes() if node.get_priority() == h]
        ATRE = atr(G, even_nodes, Nh, 0)
        nodes, edges = G.remove_nodes(ATRE)

        H = Graph(nodes, edges)
        WO = solveO(H, even_nodes, odd_nodes, h-1)
        ATRO = atr(G, odd_nodes, WO, 1)
        nodes, edges = G.remove_nodes(ATRO)
        G = Graph(nodes, edges)

        if len(WO) == 0:
            # testing W0 emptiness
            break

    WE = G.get_nodes()
    return WE

def solveO(G, even_nodes, odd_nodes, h):

    all_nodes = G.get_nodes()
    if len(all_nodes) == 0 or h < 0:
        return []

    while True:
        Nh = [node for node in G.get_nodes() if node.get_priority() == h]
        ATRO = atr(G, odd_nodes, Nh, 1)
        nodes, edges = G.remove_nodes(ATRO)
        H = Graph(nodes, edges)
        WE = solveE(H, even_nodes, odd_nodes, h-1)
        ATRE = atr(G, even_nodes, WE, 0)
        nodes, edges = G.remove_nodes(ATRE)
        G = Graph(nodes, edges)

        if len(WE) == 0:
            # testing W0 emptiness
            break

    WO = G.get_nodes()
    return WO


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="input file to run over the algorithm", nargs='+', required=True)
    parser.add_argument("--output", help="output file to put the answer of the algorithm", nargs='+', required=True)

    try:
        args = parser.parse_args()
    except:
        parser.print_help(sys.stderr)
        exit(1)

    main(args.input[0], args.output[0])
