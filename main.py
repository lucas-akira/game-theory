from tools import Graph, Node
import sys
sys.setrecursionlimit(5000)


def main():

    # player 0: circular
    # player 1: rectangular

    # creating the graph from this webpage: https://en.wikipedia.org/wiki/Parity_game
    G = Graph()

    n1 = Node(1, 1)
    n2 = Node(2, 1)
    n3 = Node(0, 1)
    n4 = Node(8, 1)
    n5 = Node(4, 0)
    n6 = Node(3, 0)
    n7 = Node(5, 0)
    n8 = Node(6, 0)

    odd_nodes = [n1.get_uuid(), n2.get_uuid(), n3.get_uuid(), n4.get_uuid()]
    even_nodes = [n5.get_uuid(), n6.get_uuid(), n7.get_uuid(), n8.get_uuid()]

    G.insert_node(n1)
    G.insert_node(n2)
    G.insert_node(n3)
    G.insert_node(n4)
    G.insert_node(n5)
    G.insert_node(n6)
    G.insert_node(n7)
    G.insert_node(n8)

    G.insert_edge(n1.get_uuid(), n5.get_uuid())
    G.insert_edge(n1.get_uuid(), n8.get_uuid())

    G.insert_edge(n5.get_uuid(), n1.get_uuid())
    G.insert_edge(n5.get_uuid(), n3.get_uuid())

    G.insert_edge(n3.get_uuid(), n1.get_uuid())
    G.insert_edge(n3.get_uuid(), n6.get_uuid())

    G.insert_edge(n6.get_uuid(), n2.get_uuid())

    G.insert_edge(n2.get_uuid(), n3.get_uuid())
    G.insert_edge(n2.get_uuid(), n7.get_uuid())

    G.insert_edge(n7.get_uuid(), n4.get_uuid())

    G.insert_edge(n4.get_uuid(), n7.get_uuid())
    G.insert_edge(n4.get_uuid(), n2.get_uuid())

    G.insert_edge(n8.get_uuid(), n1.get_uuid())
    G.insert_edge(n8.get_uuid(), n4.get_uuid())


    uuids = [n1.get_uuid(), n2.get_uuid(), n3.get_uuid(), n4.get_uuid(), n5.get_uuid(), n6.get_uuid(), n7.get_uuid(), n8.get_uuid()]
    WE = solveE(G, even_nodes, odd_nodes, 8)
    for node in WE:
        print(node.get_priority())

    #print(WE)
    #print(uuids)

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
    print("SOLVE_E ", len(all_nodes), h)
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
    print("SOLVE_O ", len(all_nodes), h)
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
    main()
