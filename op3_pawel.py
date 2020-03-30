from tools import Graph, Node
import argparse
import sys
sys.setrecursionlimit(5000)

def main(input_file, output_file):

    # player 0: circular - even
    # player 1: rectangular - odd

    even_nodes = []
    odd_nodes = []
    G = Graph()
    higher = -1
    number_nodes = None
    with open(input_file) as reader:
        data = reader.read().splitlines(True)
        number_nodes = data[0].split()
        number_nodes = number_nodes[1]
        number_nodes = number_nodes.replace(";", "")
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

    # it's number_nodes + 1 because it's index in 0
    WE = solveE(G, even_nodes, odd_nodes, higher, int(number_nodes) + 1, int(number_nodes) + 1)

    nodes = G.get_nodes()
    for node in WE:
        node.set_winner(0) # 0 means even player

    for node in nodes:
        if node.get_winner() == -1:
            node.set_winner(1) # 1 means odd player

    with open(output_file, 'w') as writter:

        writter.write("parity " + number_nodes + ";\n")
        for node in nodes:
            writter.write(str(node.get_uuid()) + " " + str(node.get_winner()) + ";\n")


def atr(G, player_nodes, U, num):

    all_nodes = G.get_nodes()
    not_changed = False

    start_nodes = [node.get_uuid() for node in U]
    atr_nodes = start_nodes

    are_equal = True

    while not not_changed:
        changed = False
        for node in all_nodes:
            successors = G.get_edges(node.get_uuid())
            if node.get_uuid() in player_nodes:
                for succ in successors:
                    if succ in atr_nodes:
                        if node.get_uuid() not in atr_nodes:
                            changed = True
                            are_equal = False
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
                        are_equal = False
                        atr_nodes.append(node.get_uuid())

        not_changed = not(changed)

    return atr_nodes, are_equal


def contain_all(G, ATRE, h):

    all_nodes = G.get_nodes()

    Nh_1 = [node.get_uuid() for node in G.get_nodes() if node.get_priority() == h-1]

    return Nh_1 <= ATRE


def solveE(G, even_nodes, odd_nodes, h, pe, po):

    all_nodes = G.get_nodes()
    amount_nodes = len(all_nodes)
    if amount_nodes == 0 or pe <= 1 or h < 0:
        return []

    pe = min(amount_nodes, pe)
    po = min(amount_nodes, po)

    while True:
        Nh = [node for node in G.get_nodes() if node.get_priority() == h]
        ATRE, _ = atr(G, even_nodes, Nh, 0)

        if contain_all(G, ATRE, h):
            Nh_2 = [node for node in G.get_nodes() if node.get_priority() == h-2]
            Nh += Nh_2
            ATRE, _ = atr(G, even_nodes, Nh, 0)

        nodes, edges = G.remove_nodes(ATRE)

        H = Graph(nodes, edges)
        WO = solveO(H, even_nodes, odd_nodes, h-1, po//2, pe)
        ATRO, equal = atr(G, odd_nodes, WO, 1)
        nodes, edges = G.remove_nodes(ATRO)
        G = Graph(nodes, edges)

        if equal:
            # testing W0 == ATR0
            break

    Nh = [node for node in G.get_nodes() if node.get_priority() == h]
    ATRE, _ = atr(G, even_nodes, Nh, 0)
    nodes, edges = G.remove_nodes(ATRE)
    H = Graph(nodes, edges)

    WO = solveO(H, even_nodes, odd_nodes, h-1, po, pe)
    ATRO, equal = atr(G, odd_nodes, WO, 1)
    nodes, edges = G.remove_nodes(ATRO)
    G = Graph(nodes, edges)

    while not(equal):
        Nh = [node for node in G.get_nodes() if node.get_priority() == h]
        ATRE, _ = atr(G, even_nodes, Nh, 0)
        if contain_all(G, ATRE, h):
            Nh_2 = [node for node in G.get_nodes() if node.get_priority() == h-2]
            Nh += Nh_2
            ATRE, _ = atr(G, even_nodes, Nh, 0)

        nodes, edges = G.remove_nodes(ATRE)

        H = Graph(nodes, edges)
        WO = solveO(H, even_nodes, odd_nodes, h-1, po//2, pe)
        ATRO, equal = atr(G, odd_nodes, WO, 1)
        nodes, edges = G.remove_nodes(ATRO)
        G = Graph(nodes, edges)

    WE = G.get_nodes()
    return WE

def solveO(G, even_nodes, odd_nodes, h, po, pe):

    all_nodes = G.get_nodes()
    amount_nodes = len(all_nodes)
    if amount_nodes == 0 or po <= 1 or h < 0:
        return []

    pe = min(amount_nodes, pe)
    po = min(amount_nodes, po)

    while True:
        Nh = [node for node in G.get_nodes() if node.get_priority() == h]
        ATRO, _ = atr(G, odd_nodes, Nh, 1)
 
        if contain_all(G, ATRO, h):
            Nh_2 = [node for node in G.get_nodes() if node.get_priority() == h-2]
            Nh += Nh_2
            ATRO, _ = atr(G, odd_nodes, Nh, 1)

        nodes, edges = G.remove_nodes(ATRO)
        H = Graph(nodes, edges)
        WE = solveE(H, even_nodes, odd_nodes, h-1, pe//2, po)
        ATRE, equal = atr(G, even_nodes, WE, 0)
        nodes, edges = G.remove_nodes(ATRE)
        G = Graph(nodes, edges)

        if equal:
            # testing WE == ATRE
            break

    Nh = [node for node in G.get_nodes() if node.get_priority() == h]
    ATRO, _ = atr(G, odd_nodes, Nh, 1)
    nodes, edges = G.remove_nodes(ATRO)
    H = Graph(nodes, edges)

    WE = solveE(H, even_nodes, odd_nodes, h-1, pe, po)
    ATRE, equal = atr(G, even_nodes, WE, 0)
    nodes, edges = G.remove_nodes(ATRE)
    G = Graph(nodes, edges)

    while not(equal):
        Nh = [node for node in G.get_nodes() if node.get_priority() == h]
        ATRO, _ = atr(G, odd_nodes, Nh, 1)
 
        if contain_all(G, ATRO, h):
            Nh_2 = [node for node in G.get_nodes() if node.get_priority() == h-2]
            Nh += Nh_2
            ATRO, _ = atr(G, odd_nodes, Nh, 1)

        nodes, edges = G.remove_nodes(ATRO)
        H = Graph(nodes, edges)
        WE = solveE(H, even_nodes, odd_nodes, h-1, pe//2, po)
        ATRE, equal = atr(G, even_nodes, WE, 0)
        nodes, edges = G.remove_nodes(ATRE)
        G = Graph(nodes, edges)

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
